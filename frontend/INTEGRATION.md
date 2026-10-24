# LabourNearMe frontend integration

The frontend is a collection of static HTML, CSS, and JavaScript files. It has no build step or frontend environment-variable loader. `supabase-config.js` supplies the Supabase project URL and public publishable key to the browser; it must never contain a service-role key. Supabase JS v2 is loaded from its CDN on sign-in, profile-registration, and employer applicant pages.

## Phase 1: authentication and profile registration

`auth.js` creates one Supabase client with persistent sessions, automatic token refresh, and URL session detection. It exposes email/password sign-up, sign-in, session/access-token retrieval, and sign-out through `window.lnmAuth`. The login page has a Sign In/Create Account mode toggle and a Worker/Employer selector. Creating an account uses Supabase email/password, then opens the corresponding profile form when a session is available. If email confirmation is required and no session is returned, the page asks the user to confirm email and sends no protected profile request. The confirmation redirect returns to the selected profile form. Signing in alone does not create or alter a profile. When sign-in was opened from a registration link, a separate, explicit continue button warns the user to continue only if they have not already registered that profile.

`api.js` adds `Authorization: Bearer <current access token>` only when a caller opts in with `authenticated: true`. Existing public job browsing through `GET /jobs/` remains unauthenticated. HTTP errors retain their status and response payload for caller handling.

| Action | Endpoint | Phase 1 request and behavior |
| --- | --- | --- |
| Create worker profile | `POST /workers/` | Authenticated. Sends `full_name`, `phone`, integer `experience_years`, numeric `expected_wage`, device coordinates as `location_lat`/`location_lng`, `category`, and `skills` (skill names). Requires a success response with `status: "success"` and `worker_id`. |
| Create employer profile | `POST /employers/register` | Authenticated. Sends `full_name`, `phone`, `employer_name`, `description`, and device coordinates as `location_lat`/`location_lng`. Requires `status: "success"` and `employer_id`. |
| Create employer job | `POST /jobs/` | Authenticated in the current job-posting form; no browser-supplied employer ID or `x-user-id` is sent. The backend must derive the employer from the token. |

Worker registration keeps the entered location text in the form, while the profile contract receives the current device coordinates only. A whole number of experience years is required and converted to a JavaScript number. Employer job site text is retained in the job description because the existing job form has no separate address field in its request body.

When email confirmation is required, the UI explains that the profile has not yet been registered and does not send the profile request without a session. The confirmation redirect is configured to return to the relevant registration page; Supabase must allow the actual local or hosted redirect URL. Registration failures are shown and the page prevents an immediate repeat after an uncertain profile request. The backend contract supplied for this integration does not define duplicate-profile error responses or recovery, so the UI does not retry, link existing profiles by email, or claim a recovery path. A page reload clears the in-memory repeat guard; duplicate protection across reloads must be provided by the backend or clarified contract.

Profile IDs returned by the API are used only as profile identifiers for existing workflow navigation. They are not authentication credentials. The public `jobs.html` page keeps `GET /jobs/` unauthenticated. Applying from that page requires an active Supabase session and sends `POST /applications/apply` with `Authorization: Bearer <current access token>` and exactly `{"job_id":"<job-id>"}`. It does not send a worker ID or `x-user-id`. Confirmed success is tracked in memory for the current page. If a request times out, loses network connectivity, or returns a server error, the page marks the outcome unknown and blocks another submission for that job during the current page session; the user should verify the application before trying again.

This change does not migrate application history or worker recommendations. Their worker-profile ID lookup remains unresolved, so `jobs.html` does not call the history endpoint to pre-check prior applications. Other pages may still have legacy worker-ID behavior and must not treat such IDs as proof of identity or secure authorization.

`job_workers.html` now loads the Supabase client and opts into Bearer authentication for `GET /applications/job/{job_id}`, `GET /workers/{worker_id}`, and `POST /applications/status-update`. Status updates send `application_id` with `new_status` set to `hired` or `rejected`; the page displays `pending`, `hired`, and `rejected`, and labels historical `accepted` records as legacy. After the existing success check, applicant data is reloaded from the server. This remains an applicants-only view and does not load recommendations. The existing applicants and worker-profile response parsing, and the page's existing `status: "success"` update confirmation check, have been preserved; those response details are not fully specified in the available contract notes and need backend confirmation. No live ownership or authorization check has been performed.

## Workflows not included in Phase 1

Worker recommendations, worker application history, and employer worker recommendations remain outside the authenticated workflows described here. Public open-job browsing remains available without sign-in. The applicant and status-update changes have not been verified end-to-end against the configured Supabase project and backend.

## Backend and deployment prerequisites

- The backend must have `SUPABASE_SERVICE_ROLE_KEY` configured server-side and must validate Supabase access tokens and derive the authenticated profile for protected operations.
- `CORS_ALLOWED_ORIGINS` must include the frontend origin.
- The Supabase email-confirmation redirect allowlist must include the frontend URL(s) used for registration completion. The login-page sign-up flow redirects to `worker.html?complete_profile=worker` or `post-job.html?complete_profile=employer` based on the selected role.
- Legacy profiles without a Supabase Auth link require a deliberate account-linking plan. The frontend does not link them by matching email.
- Duplicate-profile response semantics and safe recovery remain unspecified by the supplied contract.

## Run locally

Serve this directory as static files, for example with `python3 -m http.server 8000`, then open `http://localhost:8000/index.html`. Browser geolocation works only in a secure context; localhost is supported by modern browsers. The API base URL is configured in `api.js`.

## Verification status

Static syntax and local-resource reference checks passed. Mocked login checks cover Worker/Employer sign-up routing, confirmation-required responses with no profile submission, immediate-session signup routing, and existing-user sign-in with explicit profile continuation. These mocks do not prove that Supabase settings, email delivery/confirmation, backend token validation, profile ownership, CORS, or deployed API behavior work. No live Supabase or backend writes were performed.
