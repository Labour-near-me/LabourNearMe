
-- LabourNearMe: atomic worker, employer and job creation.
-- Existing tables and existing hiring/rating RPCs are preserved.
-- Apply this migration once in the Supabase SQL Editor.

CREATE OR REPLACE FUNCTION public.register_worker_atomic(
    p_auth_user_id uuid,
    p_full_name text,
    p_phone text,
    p_experience_years integer,
    p_expected_wage numeric,
    p_location_lat double precision,
    p_location_lng double precision,
    p_category text,
    p_skills jsonb,
    p_embedding_text text
)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
    v_profile_id uuid;
    v_skill jsonb;
    v_skill_name text;
    v_skill_id uuid;
    v_embedding public.vector(384);
BEGIN
    IF p_auth_user_id IS NULL THEN
        RAISE EXCEPTION 'Authentication user ID is required';
    END IF;

    IF p_embedding_text IS NULL OR length(trim(p_embedding_text)) = 0 THEN
        RAISE EXCEPTION 'Worker embedding is required';
    END IF;

    v_embedding := p_embedding_text::public.vector(384);

    INSERT INTO public."Profiles"
        (auth_user_id, full_name, phone, role)
    VALUES
        (p_auth_user_id, p_full_name, p_phone, 'worker')
    RETURNING id INTO v_profile_id;

    INSERT INTO public.workers
        (id, experience_years, expected_wage, location_lat,
         location_lng, worker_embedding, availability_status)
    VALUES
        (v_profile_id, p_experience_years, p_expected_wage,
         p_location_lat, p_location_lng, v_embedding, TRUE);

    -- If no skills were submitted, attach existing skills in the category,
    -- matching the previous service behaviour.
    IF p_skills IS NULL OR jsonb_typeof(p_skills) <> 'array' THEN
        RAISE EXCEPTION 'Skills must be supplied as a JSON array';
    END IF;

    IF jsonb_array_length(p_skills) = 0 THEN
        INSERT INTO public."Worker_skills" (worker_id, skill_id)
        SELECT v_profile_id, sm.id
        FROM public."Skill_master" AS sm
        WHERE lower(sm.category) = lower(p_category)
        ON CONFLICT (worker_id, skill_id) DO NOTHING;
    ELSE
        FOR v_skill IN SELECT value FROM jsonb_array_elements(p_skills)
        LOOP
            v_skill_name := trim(v_skill #>> '{}');

            IF v_skill_name = '' THEN
                RAISE EXCEPTION 'Empty skill is not valid';
            END IF;

            -- Accept either an existing skill UUID or a skill name.
            IF v_skill_name ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
                SELECT sm.id
                INTO v_skill_id
                FROM public."Skill_master" AS sm
                WHERE sm.id = v_skill_name::uuid;

                IF v_skill_id IS NULL THEN
                    RAISE EXCEPTION 'Unknown skill ID';
                END IF;
            ELSE
                SELECT sm.id
                INTO v_skill_id
                FROM public."Skill_master" AS sm
                WHERE lower(trim(sm.skill_name)) = lower(v_skill_name)
                LIMIT 1;

                IF v_skill_id IS NULL THEN
                    INSERT INTO public."Skill_master" (skill_name)
                    VALUES (lower(v_skill_name))
                    ON CONFLICT (skill_name)
                    DO UPDATE SET skill_name = EXCLUDED.skill_name
                    RETURNING id INTO v_skill_id;

                    -- Handle a case-insensitive existing name if the exact
                    -- unique constraint did not resolve it.
                    IF v_skill_id IS NULL THEN
                        SELECT sm.id INTO v_skill_id
                        FROM public."Skill_master" AS sm
                        WHERE lower(trim(sm.skill_name)) = lower(v_skill_name)
                        LIMIT 1;
                    END IF;
                END IF;
            END IF;

            INSERT INTO public."Worker_skills" (worker_id, skill_id)
            VALUES (v_profile_id, v_skill_id)
            ON CONFLICT (worker_id, skill_id) DO NOTHING;
        END LOOP;
    END IF;

    RETURN jsonb_build_object(
        'status', 'success',
        'worker_id', v_profile_id
    );
END;
$$;


CREATE OR REPLACE FUNCTION public.register_employer_atomic(
    p_auth_user_id uuid,
    p_full_name text,
    p_phone text,
    p_employer_name text,
    p_description text,
    p_location_lat double precision,
    p_location_lng double precision
)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
    v_profile_id uuid;
BEGIN
    IF p_auth_user_id IS NULL THEN
        RAISE EXCEPTION 'Authentication user ID is required';
    END IF;

    IF p_employer_name IS NULL OR length(trim(p_employer_name)) = 0 THEN
        RAISE EXCEPTION 'Employer name is required';
    END IF;

    IF p_location_lat IS NULL OR p_location_lng IS NULL THEN
        RAISE EXCEPTION 'Employer location is required';
    END IF;

    INSERT INTO public."Profiles"
        (auth_user_id, full_name, phone, role)
    VALUES
        (p_auth_user_id, p_full_name, p_phone, 'employer')
    RETURNING id INTO v_profile_id;

    INSERT INTO public."Employers"
        (id, employer_name, description, location_lat, location_lng)
    VALUES
        (v_profile_id, trim(p_employer_name), p_description,
         p_location_lat, p_location_lng);

    RETURN jsonb_build_object(
        'status', 'success',
        'employer_id', v_profile_id
    );
END;
$$;


CREATE OR REPLACE FUNCTION public.create_job_atomic(
    p_employer_id uuid,
    p_title text,
    p_description text,
    p_location_text text,
    p_location_lat double precision,
    p_location_lng double precision,
    p_budget numeric,
    p_required_skills jsonb,
    p_embedding_text text
)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
    v_job_id uuid;
    v_skill jsonb;
    v_skill_name text;
    v_skill_id uuid;
    v_embedding public.vector(384);
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM public."Employers"
        WHERE id = p_employer_id
    ) THEN
        RAISE EXCEPTION 'Employer not found';
    END IF;

    IF p_title IS NULL OR length(trim(p_title)) = 0 THEN
        RAISE EXCEPTION 'Job title is required';
    END IF;

    IF p_description IS NULL OR length(trim(p_description)) = 0 THEN
        RAISE EXCEPTION 'Job description is required';
    END IF;

    IF p_embedding_text IS NULL OR length(trim(p_embedding_text)) = 0 THEN
        RAISE EXCEPTION 'Job embedding is required';
    END IF;

    IF p_required_skills IS NULL
       OR jsonb_typeof(p_required_skills) <> 'array' THEN
        RAISE EXCEPTION 'Required skills must be a JSON array';
    END IF;

    v_embedding := p_embedding_text::public.vector(384);

    INSERT INTO public."Jobs"
        (employer_id, title, description, location_text,
         location_lat, location_lng, budget, status, job_embedding)
    VALUES
        (p_employer_id, trim(p_title), trim(p_description), p_location_text,
         p_location_lat, p_location_lng, p_budget, 'open', v_embedding)
    RETURNING id INTO v_job_id;

    FOR v_skill IN SELECT value FROM jsonb_array_elements(p_required_skills)
    LOOP
        v_skill_name := trim(v_skill #>> '{}');

        IF v_skill_name = '' THEN
            RAISE EXCEPTION 'Empty required skill is not valid';
        END IF;

        IF v_skill_name ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
            SELECT sm.id INTO v_skill_id
            FROM public."Skill_master" AS sm
            WHERE sm.id = v_skill_name::uuid;

            IF v_skill_id IS NULL THEN
                RAISE EXCEPTION 'Unknown required skill ID';
            END IF;
        ELSE
            SELECT sm.id INTO v_skill_id
            FROM public."Skill_master" AS sm
            WHERE lower(trim(sm.skill_name)) = lower(v_skill_name)
            LIMIT 1;

            IF v_skill_id IS NULL THEN
                INSERT INTO public."Skill_master" (skill_name)
                VALUES (lower(v_skill_name))
                ON CONFLICT (skill_name)
                DO UPDATE SET skill_name = EXCLUDED.skill_name
                RETURNING id INTO v_skill_id;

                IF v_skill_id IS NULL THEN
                    SELECT sm.id INTO v_skill_id
                    FROM public."Skill_master" AS sm
                    WHERE lower(trim(sm.skill_name)) = lower(v_skill_name)
                    LIMIT 1;
                END IF;
            END IF;
        END IF;

        INSERT INTO public."Job_required_skill" (job_id, skill_id)
        VALUES (v_job_id, v_skill_id)
        ON CONFLICT (job_id, skill_id) DO NOTHING;
    END LOOP;

    RETURN jsonb_build_object(
        'status', 'success',
        'job_id', v_job_id
    );
END;
$$;


-- These functions are intended to be called by the trusted backend only.
REVOKE ALL ON FUNCTION public.register_worker_atomic(
    uuid, text, text, integer, numeric, double precision,
    double precision, text, jsonb, text
) FROM PUBLIC, anon, authenticated;

REVOKE ALL ON FUNCTION public.register_employer_atomic(
    uuid, text, text, text, text, double precision, double precision
) FROM PUBLIC, anon, authenticated;

REVOKE ALL ON FUNCTION public.create_job_atomic(
    uuid, text, text, text, double precision, double precision,
    numeric, jsonb, text
) FROM PUBLIC, anon, authenticated;

GRANT EXECUTE ON FUNCTION public.register_worker_atomic(
    uuid, text, text, integer, numeric, double precision,
    double precision, text, jsonb, text
) TO service_role;

GRANT EXECUTE ON FUNCTION public.register_employer_atomic(
    uuid, text, text, text, text, double precision, double precision
) TO service_role;

GRANT EXECUTE ON FUNCTION public.create_job_atomic(
    uuid, text, text, text, double precision, double precision,
    numeric, jsonb, text
) TO service_role;
