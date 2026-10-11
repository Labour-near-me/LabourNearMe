# LabourNearMe frontend integration

The static frontend uses `api.js` for the deployed API base URL, JSON requests, timeout handling, and browser geolocation. The current backend source is the contract for these requests.

## Connected API workflows

| Workflow | Endpoint | Request/response used by the frontend |
| --- | --- | --- |
| Register worker | `POST /workers/` | `full_name`, `phone`, `experience_years` (integer), `expected_wage` (number), `location_lat`/`location_lng` (numbers), `category`, and `skills` (skill names). Success returns `status: "success"` and `worker_id`. |
| Read worker profile | `GET /workers/{worker_id}` | Returns the `Profiles` row with nested `workers` data when found. The applicant page uses it to add available name and phone details. |
| Register employer | `POST /employers/register` | Frontend sends `full_name`, `employer_name`, `phone`, `description`, and device coordinates. Success returns `employer_id`. |
| Create job | `POST /jobs/` | Requires `x-user-id`; body contains only `title`, `description`, `location_lat`, `location_lng`, `required_skills` (names), and `budget`. Success returns `job_id`. |
| List open jobs | `GET /jobs/` | Returns open jobs with `id`, `employer_id`, `title`, `description`, `budget`, `status`, `created_at`, and coordinates. |
| Recommend jobs | `GET /recommend/jobs/{worker_id}` | Returns `worker_id`, `count`, and `recommendations`. The recommendation entries contain a job ID and matching signals/title, but not the complete card fields; the frontend joins them with `GET /jobs/`. |
| Apply for job | `POST /applications/apply` | JSON body has `worker_id` and `job_id`. Success returns `status`, `message`, and the inserted application. |
| List a worker's applications | `GET /applications/my-applications/{worker_id}` | Returns application rows with joined job title, budget, and status. The recommendations page uses this to mark previously applied jobs. |
| List job applicants | `GET /applications/job/{job_id}` | Returns application rows only. The frontend requests `GET /workers/{worker_id}` for available profile data. Skills and ratings are not guaranteed by this route. |
| Update application status | `POST /applications/status-update` | Body has `application_id` and `new_status`; the frontend sends `accepted` or `rejected`. Success returns the updated row and message. |

The backend also exposes `GET /jobs/{job_id}` and `GET /recommend/workers/{job_id}`. The current pages do not need those routes for the implemented flows.

## Known backend limitations

- There is no login, token, or session authentication. Worker IDs in browser storage are workflow references. Job creation requires an `x-user-id` that the backend checks for an employer profile, but does not prove who is making the request. The application status endpoint also does not authorize the employer against the job.
- The API stores latitude and longitude, not the typed address. The frontend requests browser coordinates; job posters should allow location access while at the work site. It retains the typed location in the job description. Worker typed location text is not stored by the worker endpoint.
- Job creation supports `budget`, not a separate wage, worker-count, urgency, or active-status field. The frontend sends the per-worker daily wage as `budget` and retains site, worker-count, and urgency text in the description. The backend creates jobs with `open` status.
- The job applicant route does not join worker profiles or skill names. Profile lookup can supply available name and phone details; missing fields are shown as unavailable.
- The route implementation for `POST /applications/apply` inserts an application directly. It does not call the duplicate-checking service helper, so frontend duplicate prevention reduces accidental repeats but cannot guarantee uniqueness across clients.
- Backend operations may partially write records if a later database operation fails. The frontend reports only confirmed success responses and does not automatically retry a write after a network error.

## Run locally

From this directory, start Python's static server:

```sh
python3 -m http.server 8000
```

Open [http://localhost:8000/index.html](http://localhost:8000/index.html). Browser geolocation requires a secure context; `localhost` is supported by modern browsers. The API base URL is configured once in `api.js` as `https://labournearme.onrender.com`.

## Verification performed

- JavaScript syntax checks passed for `api.js`, `main.js`, and all inline page scripts.
- Local page asset/navigation references passed a static existence check.
- Mock API success and HTTP error parsing passed.
- No live write endpoints were called. The deployed service and browser geolocation were not verified end to end.
