-- Run this migration in the LabourNearMe Supabase project before deploying
-- the backend changes that use location_text and atomic single-worker hiring.

ALTER TABLE public."Jobs"
    ADD COLUMN IF NOT EXISTS location_text text;

-- Hiring now moves a job from open to closed. Preserve the historical values
-- already stored in this database while allowing the new closed value.
ALTER TABLE public."Jobs"
    DROP CONSTRAINT IF EXISTS jobs_status_check;
ALTER TABLE public."Jobs"
    ADD CONSTRAINT jobs_status_check
    CHECK (status IN ('open', 'closed', 'assigned', 'completed', 'cancelled'));

ALTER TABLE public."Profiles"
    ADD COLUMN IF NOT EXISTS auth_user_id uuid;

CREATE UNIQUE INDEX IF NOT EXISTS profiles_auth_user_id_unique
    ON public."Profiles" (auth_user_id)
    WHERE auth_user_id IS NOT NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
         WHERE conname = 'profiles_auth_user_id_fkey'
           AND conrelid = 'public."Profiles"'::regclass
    ) THEN
        ALTER TABLE public."Profiles"
            ADD CONSTRAINT profiles_auth_user_id_fkey
            FOREIGN KEY (auth_user_id) REFERENCES auth.users(id) ON DELETE SET NULL;
    END IF;
END;
$$;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM public.applications
        GROUP BY job_id, worker_id
        HAVING count(*) > 1
    ) THEN
        RAISE EXCEPTION 'Duplicate applications exist for a job/worker pair; resolve them before applying this migration';
    END IF;
END;
$$;

CREATE UNIQUE INDEX IF NOT EXISTS applications_job_worker_unique
    ON public.applications (job_id, worker_id);

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM public.ratings
        GROUP BY job_id, reviewer_id, reviewee_id
        HAVING count(*) > 1
    ) THEN
        RAISE EXCEPTION 'Duplicate ratings exist for a job/reviewer/worker tuple; resolve them before applying this migration';
    END IF;
END;
$$;

CREATE UNIQUE INDEX IF NOT EXISTS ratings_job_reviewer_worker_unique
    ON public.ratings (job_id, reviewer_id, reviewee_id);

CREATE OR REPLACE FUNCTION public.hire_application_for_job(
    p_application_id uuid,
    p_employer_id uuid
)
RETURNS TABLE (id uuid, job_id uuid, status text)
LANGUAGE plpgsql
AS $$
DECLARE
    v_job_id uuid;
BEGIN
    SELECT a.job_id
      INTO v_job_id
      FROM public.applications AS a
      JOIN public."Jobs" AS j ON j.id = a.job_id
     WHERE a.id = p_application_id
       AND a.status = 'pending'
       AND j.status = 'open'
       AND j.employer_id = p_employer_id
     FOR UPDATE OF a, j;

    IF v_job_id IS NULL THEN
        RAISE EXCEPTION 'Application is not pending, job is closed, or employer does not own the job';
    END IF;

    UPDATE public."Jobs"
       SET status = 'closed'
     WHERE id = v_job_id
       AND status = 'open';

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Job was closed by another request';
    END IF;

    UPDATE public.applications
       SET status = 'rejected'
     WHERE job_id = v_job_id
       AND id <> p_application_id
       AND status = 'pending';

    UPDATE public.applications
       SET status = 'hired'
     WHERE id = p_application_id
       AND status = 'pending';

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Application status changed before hiring completed';
    END IF;

    RETURN QUERY
    SELECT a.id, a.job_id, a.status::text
      FROM public.applications AS a
     WHERE a.id = p_application_id;
END;
$$;

CREATE OR REPLACE FUNCTION public.complete_and_rate_job(
    p_job_id uuid,
    p_employer_id uuid,
    p_worker_id uuid,
    p_rating_value integer,
    p_feedback text DEFAULT ''
)
RETURNS jsonb
LANGUAGE plpgsql
AS $$
DECLARE
    v_rating public.ratings%ROWTYPE;
BEGIN
    IF p_rating_value < 1 OR p_rating_value > 5 THEN
        RAISE EXCEPTION 'Rating must be between 1 and 5';
    END IF;

    PERFORM 1
      FROM public."Jobs" AS j
     WHERE j.id = p_job_id
       AND j.employer_id = p_employer_id
       AND j.status = 'closed'
     FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Job is not closed or employer does not own it';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM public.applications AS a
         WHERE a.job_id = p_job_id
           AND a.worker_id = p_worker_id
           AND a.status = 'hired'
    ) THEN
        RAISE EXCEPTION 'Worker was not hired for this job';
    END IF;

    INSERT INTO public.ratings (
        job_id, reviewer_id, reviewee_id, rating_value, feedbck
    ) VALUES (
        p_job_id, p_employer_id, p_worker_id, p_rating_value, COALESCE(p_feedback, '')
    )
    RETURNING * INTO v_rating;

    UPDATE public.workers
       SET rating = (
           SELECT round(avg(r.rating_value)::numeric, 2)
             FROM public.ratings AS r
            WHERE r.reviewee_id = p_worker_id
       )
     WHERE id = p_worker_id;

    UPDATE public."Jobs"
       SET status = 'completed'
     WHERE id = p_job_id
       AND status = 'closed';

    RETURN to_jsonb(v_rating);
END;
$$;

-- These RPCs trust the employer ID supplied by the backend after token/profile
-- verification. Prevent direct browser RPC calls with caller-chosen IDs.
REVOKE EXECUTE ON FUNCTION public.hire_application_for_job(uuid, uuid)
    FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.hire_application_for_job(uuid, uuid)
    TO service_role;

REVOKE EXECUTE ON FUNCTION public.complete_and_rate_job(uuid, uuid, uuid, integer, text)
    FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.complete_and_rate_job(uuid, uuid, uuid, integer, text)
    TO service_role;
