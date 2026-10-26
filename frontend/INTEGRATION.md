# LabourNearMe frontend integration

The frontend is a collection of static HTML, CSS, and JavaScript files. It has no build step or frontend environment-variable loader. `supabase-config.js` supplies the Supabase project URL and public publishable key to the browser; it must never contain a service-role key. Supabase JS v2 is loaded from its CDN on sign-in, profile-registration, and employer applicant pages.

## Phase 1: authentication and profile registration

`auth.js` creates one Supabase client with persistent sessions, automatic token refresh, and URL session detection. It exposes phone OTP, email/password sign-up and sign-in, session/access-token retrieval, and sign-out through `window.lnmAuth`. The login page preserves phone OTP and offers an email/password fallback with a Worker/Employer selector for new accounts. Creating an email account uses Supabase email/password, then opens the corresponding profile form only when a session is available. If email confirmation is required and no session is returned, the page asks the user to confirm email and sends no protected profile request. The confirmation redirect returns to the selected profile form. Signing in alone does not create or alter a profile. Sign-in profile lookup uses the backend `/auth/me` response and routes complete profiles by the backend role.

`api.js` adds `Authorization: Bearer <current access token>` only when a caller opts in with `authenticated: true`. Existing public job browsing through `GET /jobs/` remains unauthenticated. HTTP errors retain their status and response payload for caller handling.

| Action | Endpoint | Phase 1 request and behavior |
| --- | --- | --- |
| Create worker profile | `POST /workers/` | Authenticated. Sends `full_name`, `phone`, integer `experience_years`, numeric `expected_wage`, device coordinates as `location_lat`/`location_lng`, `category`, and `skills` (skill names). Requires a success response with `status: "success"` and `worker_id`. |
| Create employer profile | `POST /employers/register` | Authenticated. Sends `full_name`, `phone`, `employer_name`, `description`, and device coordinates as `location_lat`/`location_lng`. Requires `status: "success"` and `employer_id`. |
| Create employer job | `POST /jobs/` | Authenticated in the current job-posting form; no browser-supplied employer ID or `x-user-id` is sent. The backend must derive the employer from the token. |

Worker registration keeps the entered location text in the form, while the profile contract receives the current device coordinates only. A whole number of experience years is required and converted to a JavaScript number. Employer job site text is retained in the job description because the existing job form has no separate address field in its request body.

When email confirmation is required, the UI explains that the profile has not yet been registered and does not send the profile request without a session. The confirmation redirect is configured to return to the relevant registration page; Supabase must allow the actual local or hosted redirect URL. Registration failures are shown and the page prevents an immediate repeat after an uncertain profile request. The inspected backend checks `Profiles.auth_user_id` before both worker and employer registration and returns HTTP 409 when a profile already exists. The frontend does not link separate phone and email accounts by matching email.

Profile IDs returned by the API are used only as profile identifiers for existing workflow navigation. They are not authentication credentials. The public `jobs.html` page keeps `GET /jobs/` unauthenticated. Applying from that page requires an active Supabase session and sends `POST /applications/apply` with `Authorization: Bearer <current access token>` and exactly `{"job_id":"<job-id>"}`. It does not send a worker ID or `x-user-id`. Confirmed success is tracked in memory for the current page. If a request times out, loses network connectivity, or returns a server error, the page marks the outcome unknown and blocks another submission for that job during the current page session; the user should verify the application before trying again.

`jobs.html` applies with the current session token and leaves profile identity to the backend. The legacy `worker_jobs.html` page now uses authenticated requests for worker recommendations, application history, and applications; the browser-stored worker ID is only a route/workflow reference because the backend verifies it against the authenticated profile. A live authorization check is still required.

`job_workers.html` uses Bearer authentication for `GET /applications/job/{job_id}`, `GET /workers/{worker_id}`, `POST /applications/status-update`, and the employer-owned job recommendation route `GET /recommend/workers/{job_id}`. Recommendation cards show the fields returned by the backend (name, match score, distance, and rating); this route does not return skills or contact details, and the frontend does not fetch restricted worker contact data for non-applicants. Status updates send `application_id` with `new_status` set to `hired` or `rejected`. After the existing success check, applicant data is reloaded from the server. The backend recommendation service returns an empty list when its engine raises an exception, so an empty result cannot distinguish “no matches” from an engine failure.

## Workflows not included in Phase 1

Public open-job browsing remains available without sign-in. Protected application and recommendation flows depend on an active Supabase session. The frontend cannot verify these live integrations without a running backend and Supabase account.

## Backend and deployment prerequisites

- The backend must have `SUPABASE_SERVICE_ROLE_KEY` configured server-side and must validate Supabase access tokens and derive the authenticated profile for protected operations.
- `CORS_ALLOWED_ORIGINS` must include the frontend origin.
- The Supabase email-confirmation redirect allowlist must include the frontend URL(s) used for registration completion. The login-page sign-up flow redirects to `worker.html?complete_profile=worker` or `post-job.html?complete_profile=employer` based on the selected role.
- Legacy profiles without a Supabase Auth link require a deliberate account-linking plan. The frontend does not link them by matching email.
- Worker and employer registration both check for an existing profile linked to the authenticated Supabase user and return HTTP 409 when one exists. The check/insert sequence has not been stress-tested for simultaneous requests.

## Run locally

Serve this directory as static files, for example with `python3 -m http.server 8000`, then open `http://localhost:8000/index.html`. Browser geolocation works only in a secure context; localhost is supported by modern browsers. The API base URL is configured in `api.js`.

Worker registration includes browser speech dictation for the work-category field when `SpeechRecognition` is available. It uses the selected UI language and only fills a field for review; the normal registration validation and explicit submit action are still required. Unsupported browsers retain the text input.

## Verification status

Static syntax and local-resource reference checks passed. Mocked login checks cover Worker/Employer sign-up routing, confirmation-required responses with no profile submission, immediate-session signup routing, and existing-user sign-in with explicit profile continuation. These mocks do not prove that Supabase settings, email delivery/confirmation, backend token validation, profile ownership, CORS, or deployed API behavior work. No live Supabase or backend writes were performed.

The release-rescue checks additionally include JavaScript syntax, inline HTML script syntax, duplicate-ID checks, and mocked speech-dictation behavior. The Render hostname did not resolve from the test environment, and no local frontend or backend server was listening; no live authentication, profile, job, application, recommendation, or microphone/browser-permission flow was verified.
