# LabourNearMe API contract for frontend integration

This contract matches the current backend implementation on `ml-logic-final`.
The Supabase schema migration has been applied. End-to-end journeys have not
yet been verified.

## Authentication

The frontend signs up and signs in with Supabase Auth. Send the returned access
token on every protected request:

```http
Authorization: Bearer <supabase_access_token>
```

The backend verifies that token with Supabase, then looks up the app profile by
`Profiles.auth_user_id`. Profile registration happens after Supabase signup.
Do not send `worker_id`, `employer_id`, or `x-user-id` as identity proof.

## Endpoints

### Register a worker

`POST /workers/` — signed-in Supabase user; creates a worker profile.

```json
{
  "full_name": "Asha Kumar",
  "phone": "9876543210",
  "experience_years": 3,
  "expected_wage": 700,
  "location_lat": 23.17,
  "location_lng": 75.78,
  "category": "Cleaning",
  "skills": ["Floor cleaning"]
}
```

Success: `{"status":"success","worker_id":"<profile-id>"}`.

### Register an employer

`POST /employers/register` — signed-in Supabase user; creates an employer profile.

```json
{
  "full_name": "Ravi Shah",
  "phone": "9876543210",
  "employer_name": "Shah Services",
  "description": "Local home services",
  "location_lat": 23.17,
  "location_lng": 75.78
}
```

Success: `{"status":"success","employer_id":"<profile-id>"}`.

### Browse jobs

- `GET /jobs/` — public; returns open jobs with coordinates rounded to two
  decimal places. Free-text `location_text` is not returned publicly.
- `GET /jobs/{job_id}` — public; returns job details and required skill IDs,
  with approximate coordinates and no free-text `location_text`.

### Post a job

`POST /jobs/` — employer only. Body fields: `title`, `description`,
`location_text` (optional for now), `location_lat`, `location_lng`,
`required_skills` (skill names or known skill IDs), and `budget`.

Success: `{"status":"success","job_id":"<job-id>"}`.

### Apply and view application status

- `POST /applications/apply` — worker only. Body: `{"job_id":"<job-id>"}`.
  The backend obtains the worker ID from the token. Success includes the created
  application, with status `pending`.
- `GET /applications/my-applications/{worker_id}` — worker only; the ID must
  belong to the signed-in worker.
- `GET /applications/job/{job_id}` — employer owner only; returns applications
  for that employer's job.

Application statuses are `pending`, `hired`, and `rejected`. The frontend's
Accept action must send `hired`.

Some older database rows still have the legacy status `accepted`. They were
preserved because some old jobs have multiple accepted applicants; do not treat
those historical rows as proof that the new one-worker hiring flow ran.

### Hire or reject an applicant

`POST /applications/status-update` — employer who owns the job only.

```json
{"application_id":"<application-id>","new_status":"hired"}
```

`new_status` may be `hired` or `rejected`. Hiring one worker closes the job
and rejects its other pending applications in the same database transaction.
Only pending applications can be changed.

### Worker recommendations for an employer job

`GET /recommend/workers/{job_id}?top_n=5` — employer who owns the job only;
`top_n` must be 1–20 (default 5). Response:

```json
{
  "job_id": "<job-id>",
  "count": 1,
  "recommendations": [
    {
      "worker_id": "<profile-id>",
      "full_name": "Asha Kumar",
      "final_score": 0.91,
      "similarity": 0.88,
      "skill_similarity": 0.9,
      "distance_km": 2.4,
      "rating": 4.7,
      "match_type": "hybrid"
    }
  ]
}
```

The returned worker fields are allowlisted; embeddings and internal model
scores are omitted. Recommendations are separate from applications.

### Worker job recommendations

`GET /recommend/jobs/{worker_id}?top_n=5` — worker only; the ID must belong to
the signed-in worker. Response contains `worker_id`, `count`, and
`recommendations` (including job data and `job_title`).

Both recommendation endpoints return an empty `recommendations` list when the
engine completes successfully but finds no matches. If recommendation
generation or its supporting database lookup fails, the API returns `500` and
records the exception in the backend logs instead of reporting a false empty
result.

## Common errors

- `401`: missing, invalid, or expired Supabase access token.
- `403`: wrong account/role or attempting to access another user's resource.
- `404`: job or application does not exist.
- `409`: duplicate application, profile already registered, stale application,
  or job already closed for hiring.
- `422`: request body or query parameter fails validation.

Other database/service failures may currently return `400` with a `detail`
message. The specific pre-existing backend error is not documented yet because
its route and exact message have not been captured.

## Integration prerequisites

1. Configure `SUPABASE_SERVICE_ROLE_KEY` in the backend environment with the
   Supabase service-role JWT. The backend rejects an anon key. Never put this
   secret in frontend code or share it in chat.
2. Set `CORS_ALLOWED_ORIGINS` to the exact deployed frontend origin(s),
   comma-separated. Local development origins on ports 3000, 5173, and 8000
   are also allowed by the backend.
3. Existing profiles have no Supabase Auth link yet. New accounts must create a
   profile through `POST /workers/` or `POST /employers/register`; old profiles
   need a deliberate account-linking plan before those accounts can sign in.
4. Verify the worker and employer journeys end to end.
