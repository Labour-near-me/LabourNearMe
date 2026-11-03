'use strict';

const otpPhoneInput = document.getElementById('otp-phone');
const otpCodeInput = document.getElementById('otp-code');
const otpCodeField = document.getElementById('otp-code-field');
const otpRequestButton = document.getElementById('request-otp');
const otpVerifyButton = document.getElementById('verify-otp');
const otpMessage = document.getElementById('otp-message');
const otpProfileChoice = document.getElementById('otp-profile-choice');
const otpNewUserConfirm = document.getElementById('otp-new-user-confirm');
const emailAuthForm = document.getElementById('email-auth-form');
const emailInput = document.getElementById('email-auth-email');
const emailPasswordInput = document.getElementById('email-auth-password');
const emailRoleInput = document.getElementById('email-auth-role');
const registrationEntry = new URLSearchParams(window.location.search).get('next');
const registrationRoleHint = registrationEntry === 'worker-registration'
  ? 'worker'
  : registrationEntry === 'employer-registration' ? 'employer' : '';
if (registrationRoleHint && !emailRoleInput.value) emailRoleInput.value = registrationRoleHint;
const emailSignInButton = document.getElementById('email-sign-in');
const emailSignUpButton = document.getElementById('email-sign-up');
const emailAuthMessage = document.getElementById('email-auth-message');
const googleSignInButton = document.getElementById('google-sign-in');
const googleButtonLabel = document.getElementById('google-button-label');
const googleSpinner = document.getElementById('google-spinner');
const googleAuthMessage = document.getElementById('google-auth-message');
const GOOGLE_OAUTH_PENDING_KEY = 'lnm-google-oauth-pending';
let otpRequestedPhone = '';
let otpMessageKey = '';
let otpPhoneErrorKey = '';
let otpCodeErrorKey = '';
let otpRequestErrorDetail = '';
let requestingOtp = false;
let verifyingOtp = false;
let emailAuthBusy = false;
let emailBusyAction = '';
let emailMessageKey = '';
let emailMessageDetail = '';
let googleAuthBusy = false;
let googleAuthMessageKey = '';
let googleCallbackProcessed = false;
let googleRedirectTimer = null;
let googleAttemptId = 0;

function t(key) {
  return window.LNM_I18N ? window.LNM_I18N.t(key) : key;
}

function showOtpMessage(key) {
  otpMessageKey = key;
  const successMessage = key === 'otpSent' && window.LNM_I18N && window.LNM_I18N.getLanguage() === 'en'
    ? 'OTP sent successfully'
    : t(key);
  otpMessage.textContent = key ? `${key === 'otpSent' ? successMessage : t(key)}${key === 'otpRequestError' && otpRequestErrorDetail ? ` ${otpRequestErrorDetail}` : ''}` : '';
  otpMessage.classList.toggle('status-success', key === 'otpSent');
  otpMessage.classList.toggle('status-info', key === 'otpSending');
}

function safeAuthErrorMessage(error) {
  if (!error || typeof error.message !== 'string' || !error.message.trim()) return '';
  return error.message.trim()
    .replace(/\bBearer\s+\S+/gi, 'Bearer [redacted]')
    .replace(/\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b/g, '[redacted]')
    .slice(0, 240);
}

function showEmailMessage(key, detail = '') {
  emailMessageKey = key;
  emailMessageDetail = detail;
  emailAuthMessage.textContent = key ? `${t(key)}${detail ? ` ${detail}` : ''}` : '';
  emailAuthMessage.classList.toggle('status-info', key === 'emailWorking' || key === 'emailConfirmRequired');
  emailAuthMessage.classList.toggle('status-success', false);
}

function updateEmailButtonLabels() {
  emailSignInButton.textContent = t(emailAuthBusy && emailBusyAction === 'signin' ? 'emailWorking' : 'emailSignIn');
  emailSignUpButton.textContent = t(emailAuthBusy && emailBusyAction === 'signup' ? 'emailWorking' : 'emailSignUp');
}

function setEmailAuthBusy(action) {
  emailAuthBusy = Boolean(action);
  emailBusyAction = action || '';
  emailSignInButton.disabled = emailAuthBusy;
  emailSignUpButton.disabled = emailAuthBusy;
  updateEmailButtonLabels();
}

function setOtpFieldError(input, key, field) {
  const error = document.getElementById(`${input.id}-error`);
  input.setAttribute('aria-invalid', key ? 'true' : 'false');
  error.textContent = key ? t(key) : '';
  if (field === 'phone') otpPhoneErrorKey = key;
  else otpCodeErrorKey = key;
}

function updateButtonLabels() {
  otpRequestButton.textContent = t(requestingOtp ? 'otpSending' : 'sendOtp');
  otpVerifyButton.textContent = t(verifyingOtp ? 'otpVerifying' : 'verifyOtp');
}

function profileUrl(role) {
  if (role === 'worker') return 'worker.html?complete_profile=worker';
  if (role === 'employer') return 'post-job.html?complete_profile=employer';
  return null;
}

function routeFromAuthProfile(response, missingRole = '', emailFlow = false) {
  if (!response || typeof response.user_id !== 'string' || !response.user_id) {
    throw new Error('unexpected');
  }

  if (response.profile_status === 'missing' && response.needs_registration === true && response.profile === null) {
    if (missingRole === 'worker' || missingRole === 'employer') {
      const destination = profileUrl(missingRole);
      if (!destination) throw new Error('unexpected');
      window.location.href = destination;
      return;
    }
    otpNewUserConfirm.checked = false;
    otpProfileChoice.querySelectorAll('[data-otp-role]').forEach((button) => { button.disabled = true; });
    otpProfileChoice.hidden = false;
    showOtpMessage('');
    if (emailFlow) showEmailMessage('profileMissingNotice');
    return;
  }

  const profile = response.profile;
  if (response.profile_status !== 'complete' || response.needs_registration !== false || !profile || profile.id == null) {
    throw new Error('unexpected');
  }

  if (profile.role === 'worker') {
    window.location.href = `worker_jobs.html?worker_id=${encodeURIComponent(profile.id)}`;
    return;
  }
  if (profile.role === 'employer') {
    window.location.href = 'post-job.html';
    return;
  }
  throw new Error('unexpected');
}

async function loadOtpProfile() {
  try {
    const response = await window.lnmRequest('/auth/me', { authenticated: true });
    routeFromAuthProfile(response);
  } catch (error) {
    if (error.message === 'unexpected') showOtpMessage('otpUnexpectedResponse');
    else if (error.status === 401) showOtpMessage('otpAuthRequired');
    else if (error.status === 409) showOtpMessage('otpProfileConflict');
    else showOtpMessage('otpProfileLookupError');
  }
}

async function loadEmailProfile(missingRole = '') {
  try {
    const response = await window.lnmRequest('/auth/me', { authenticated: true });
    routeFromAuthProfile(response, missingRole, true);
  } catch (error) {
    if (error.message === 'unexpected') showEmailMessage('otpUnexpectedResponse');
    else if (error.status === 401) showEmailMessage('otpAuthRequired');
    else if (error.status === 409) showEmailMessage('otpProfileConflict');
    else showEmailMessage('otpProfileLookupError');
  }
}

function showGoogleMessage(key) {
  googleAuthMessageKey = key;
  googleAuthMessage.textContent = key ? t(key) : '';
  googleAuthMessage.classList.toggle('status-info', [
    'googleStarting', 'googleCheckingProfile', 'googleCancelled'
  ].includes(key));
}

function updateGoogleButtonLabel() {
  googleButtonLabel.textContent = t(googleAuthBusy ? 'googleWorking' : 'googleSignIn');
}

function setGoogleAuthBusy(busy) {
  googleAuthBusy = Boolean(busy);
  googleSignInButton.disabled = googleAuthBusy;
  googleSignInButton.setAttribute('aria-busy', googleAuthBusy ? 'true' : 'false');
  googleSpinner.hidden = !googleAuthBusy;
  googleSignInButton.classList.toggle('is-loading', googleAuthBusy);
  updateGoogleButtonLabel();
}

function clearGoogleOAuthPending() {
  try {
    window.sessionStorage.removeItem(GOOGLE_OAUTH_PENDING_KEY);
  } catch (_) {
    // Session storage may be unavailable in a restricted browser context.
  }
}

function googleOAuthPending() {
  try {
    return window.sessionStorage.getItem(GOOGLE_OAUTH_PENDING_KEY) === '1';
  } catch (_) {
    return false;
  }
}

function readGoogleOAuthCallback() {
  const query = new URLSearchParams(window.location.search);
  const fragment = new URLSearchParams(window.location.hash.replace(/^#/, ''));
  const get = (key) => query.get(key) || fragment.get(key) || '';
  const error = get('error');
  const errorDescription = get('error_description');
  const errorCode = get('error_code');
  const callbackMarker = Boolean(
    query.get('code') || fragment.get('code') || fragment.get('access_token') ||
    error || errorDescription || errorCode
  );

  return {
    isCallback: callbackMarker || googleOAuthPending(),
    hasCallbackMarker: callbackMarker,
    error,
    errorDescription,
    errorCode
  };
}

function cleanGoogleOAuthCallbackUrl() {
  try {
    const url = new URL(window.location.href);
    [
      'code', 'state', 'error', 'error_code', 'error_description', 'error_uri',
      'provider_token', 'provider_refresh_token'
    ].forEach((key) => url.searchParams.delete(key));

    const fragment = new URLSearchParams(url.hash.replace(/^#/, ''));
    [
      'access_token', 'refresh_token', 'token_type', 'expires_in', 'expires_at',
      'error', 'error_code', 'error_description', 'state', 'provider_token',
      'provider_refresh_token'
    ].forEach((key) => fragment.delete(key));
    url.hash = fragment.toString() ? `#${fragment.toString()}` : '';

    window.history.replaceState(window.history.state, '', `${url.pathname}${url.search}${url.hash}`);
  } catch (_) {
    // A URL cleanup failure must not prevent profile lookup or sign-in feedback.
  }
}

function isGoogleOAuthCancellation(callback) {
  return callback.errorCode === 'access_denied' || callback.error === 'access_denied' ||
    /cancel|denied/i.test(`${callback.error} ${callback.errorDescription}`);
}

function googleAuthFailureKey(error) {
  if (error && error.status === 401) return 'googleAuthRequired';
  if (error && error.status === 503) return 'googleServiceUnavailable';
  return 'googleFailed';
}

async function loadGoogleProfile(session) {
  if (!session || !session.access_token) {
    showGoogleMessage('googleNoSession');
    return;
  }

  try {
    const response = await window.lnmRequest('/auth/me', { authenticated: true });
    routeFromAuthProfile(response);
    showGoogleMessage('');
  } catch (error) {
    if (error.message === 'unexpected') showGoogleMessage('otpUnexpectedResponse');
    else if (error.status === 401) showGoogleMessage('googleAuthRequired');
    else if (error.status === 503) showGoogleMessage('googleServiceUnavailable');
    else if (error.status === 409) showGoogleMessage('otpProfileConflict');
    else showGoogleMessage('googleProfileLookupError');
  }
}

async function startGoogleSignIn() {
  if (googleAuthBusy) return;
  const attemptId = ++googleAttemptId;
  showGoogleMessage('');
  setGoogleAuthBusy(true);
  showGoogleMessage('googleStarting');

  const startingPage = window.location.href;
  try {
    const client = window.lnmSupabase;
    if (!client || !client.auth || typeof client.auth.signInWithOAuth !== 'function') {
      throw new Error('Google sign-in is unavailable.');
    }

    try {
      window.sessionStorage.setItem(GOOGLE_OAUTH_PENDING_KEY, '1');
    } catch (_) {
      // The callback URL markers remain available if session storage is blocked.
    }

    googleRedirectTimer = window.setTimeout(() => {
      if (attemptId !== googleAttemptId || !googleAuthBusy || window.location.href !== startingPage) return;
      googleAttemptId += 1;
      googleRedirectTimer = null;
      clearGoogleOAuthPending();
      setGoogleAuthBusy(false);
      showGoogleMessage('googleRedirectFailed');
    }, 12000);

    const redirectTo = new URL(window.location.pathname, window.location.origin).toString();
    const { error } = await client.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo }
    });
    if (error) throw error;
  } catch (error) {
    if (attemptId !== googleAttemptId) return;
    if (googleRedirectTimer !== null) window.clearTimeout(googleRedirectTimer);
    googleRedirectTimer = null;
    clearGoogleOAuthPending();
    setGoogleAuthBusy(false);
    showGoogleMessage(googleAuthFailureKey(error));
  }
}

async function handleGoogleOAuthCallback() {
  const callback = readGoogleOAuthCallback();
  if (!callback.isCallback || googleCallbackProcessed) return;
  googleCallbackProcessed = true;
  clearGoogleOAuthPending();

  if (callback.error || callback.errorDescription || callback.errorCode) {
    cleanGoogleOAuthCallbackUrl();
    setGoogleAuthBusy(false);
    showGoogleMessage(isGoogleOAuthCancellation(callback) ? 'googleCancelled' : 'googleFailed');
    return;
  }

  setGoogleAuthBusy(true);
  showGoogleMessage('googleCheckingProfile');
  try {
    // Supabase's existing detectSessionInUrl initialization completes before getSession returns.
    const session = await window.lnmAuth.getSession();
    cleanGoogleOAuthCallbackUrl();
    if (!session && !callback.hasCallbackMarker) {
      showGoogleMessage('googleCancelled');
      return;
    }
    await loadGoogleProfile(session);
  } catch (error) {
    cleanGoogleOAuthCallbackUrl();
    showGoogleMessage(googleAuthFailureKey(error));
  } finally {
    setGoogleAuthBusy(false);
  }
}

function validateEmailCredentials() {
  if (!emailInput.value.trim() || !emailInput.validity.valid) {
    emailInput.reportValidity();
    return false;
  }
  if (!emailPasswordInput.value) {
    emailPasswordInput.reportValidity();
    return false;
  }
  return true;
}

async function signInWithEmail() {
  if (emailAuthBusy || !validateEmailCredentials()) return;
  showEmailMessage('');
  setEmailAuthBusy('signin');
  showEmailMessage('emailWorking');
  try {
    const result = await window.lnmAuth.signInWithPassword(emailInput.value.trim(), emailPasswordInput.value);
    if (result.error) throw result.error;
    if (!result.data || !result.data.session || !result.data.session.access_token) {
      showEmailMessage('emailNoSession');
      return;
    }
    await loadEmailProfile();
  } catch (error) {
    showEmailMessage('emailAuthFailed', safeAuthErrorMessage(error));
  } finally {
    setEmailAuthBusy('');
  }
}

async function signUpWithEmail() {
  if (emailAuthBusy || !validateEmailCredentials()) return;
  const role = emailRoleInput.value;
  if (role !== 'worker' && role !== 'employer') {
    showEmailMessage('emailRoleRequired');
    emailRoleInput.focus();
    return;
  }

  showEmailMessage('');
  setEmailAuthBusy('signup');
  showEmailMessage('emailWorking');
  try {
    const existingSession = await window.lnmAuth.getSession();
    if (existingSession) {
      showEmailMessage('emailSignOutFirst');
      return;
    }
    const emailRedirectTo = new URL(profileUrl(role), window.location.href).toString();
    const result = await window.lnmAuth.signUpWithPassword(
      emailInput.value.trim(), emailPasswordInput.value, emailRedirectTo
    );
    if (result.error) throw result.error;
    const data = result.data || {};
    if (data.session && data.session.access_token) {
      await loadEmailProfile(role);
    } else if (data.user) {
      showEmailMessage('emailConfirmRequired');
    } else {
      showEmailMessage('emailNoSession');
    }
  } catch (error) {
    showEmailMessage('emailAuthFailed', safeAuthErrorMessage(error));
  } finally {
    setEmailAuthBusy('');
  }
}

emailAuthForm.addEventListener('submit', (event) => {
  event.preventDefault();
  signInWithEmail();
});
emailSignUpButton.addEventListener('click', signUpWithEmail);
googleSignInButton.addEventListener('click', startGoogleSignIn);

async function requestOtp() {
  if (requestingOtp) return;
  otpProfileChoice.hidden = true;
  otpRequestErrorDetail = '';
  showOtpMessage('');
  const phone = otpPhoneInput.value.trim();
  const phoneError = !phone ? 'otpPhoneRequired' : (/^\+[1-9]\d{7,14}$/.test(phone) ? '' : 'otpPhoneInvalid');
  setOtpFieldError(otpPhoneInput, phoneError, 'phone');
  if (phoneError) return;

  requestingOtp = true;
  otpRequestButton.disabled = true;
  otpRequestButton.setAttribute('aria-busy', 'true');
  updateButtonLabels();
  showOtpMessage('otpSending');
  try {
    if (!window.lnmAuth || typeof window.lnmAuth.requestPhoneOtp !== 'function') {
      throw new Error('Phone sign-in is unavailable. Check that the Supabase client loaded correctly.');
    }
    const result = await window.lnmAuth.requestPhoneOtp(phone);
    if (!result) throw new Error('Supabase did not return a response. Please try again.');
    const { error } = result;
    if (error) throw error;
    otpRequestedPhone = phone;
    otpCodeField.hidden = false;
    otpVerifyButton.hidden = false;
    showOtpMessage('otpSent');
    otpCodeInput.focus();
  } catch (error) {
    otpRequestErrorDetail = safeAuthErrorMessage(error);
    showOtpMessage('otpRequestError');
  } finally {
    requestingOtp = false;
    otpRequestButton.disabled = false;
    otpRequestButton.removeAttribute('aria-busy');
    updateButtonLabels();
  }
}

otpRequestButton.addEventListener('click', requestOtp);

otpPhoneInput.addEventListener('input', () => {
  setOtpFieldError(otpPhoneInput, '', 'phone');
  if (otpRequestedPhone && otpPhoneInput.value.trim() !== otpRequestedPhone) {
    otpRequestedPhone = '';
    otpCodeInput.value = '';
    otpCodeField.hidden = true;
    otpVerifyButton.hidden = true;
    otpProfileChoice.hidden = true;
    showOtpMessage('');
  }
});

otpCodeInput.addEventListener('input', () => setOtpFieldError(otpCodeInput, '', 'code'));

document.getElementById('otp-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!otpRequestedPhone || otpPhoneInput.value.trim() !== otpRequestedPhone) {
    await requestOtp();
    return;
  }
  if (verifyingOtp) return;
  otpProfileChoice.hidden = true;
  showOtpMessage('');
  const code = otpCodeInput.value.trim();
  setOtpFieldError(otpCodeInput, code ? '' : 'otpCodeRequired', 'code');
  if (!otpRequestedPhone || !code) return;

  verifyingOtp = true;
  otpVerifyButton.disabled = true;
  updateButtonLabels();
  try {
    const result = await window.lnmAuth.verifyPhoneOtp(otpRequestedPhone, code);
    if (!result) throw new Error('Supabase did not return a response. Please try again.');
    const { data, error } = result;
    if (error) throw error;
    if (!data || !data.session || !data.session.access_token) {
      showOtpMessage('otpSessionError');
      return;
    }
    await loadOtpProfile();
  } catch (_) {
    showOtpMessage('otpVerificationError');
  } finally {
    verifyingOtp = false;
    otpVerifyButton.disabled = false;
    updateButtonLabels();
  }
});

otpProfileChoice.querySelectorAll('[data-otp-role]').forEach((button) => {
  button.addEventListener('click', () => {
    const role = button.dataset.otpRole;
    const destination = profileUrl(role);
    if (otpNewUserConfirm.checked && destination) window.location.href = destination;
  });
});

otpNewUserConfirm.addEventListener('change', () => {
  otpProfileChoice.querySelectorAll('[data-otp-role]').forEach((button) => { button.disabled = !otpNewUserConfirm.checked; });
});

document.addEventListener('lnm-language-change', () => {
  showOtpMessage(otpMessageKey);
  showEmailMessage(emailMessageKey, emailMessageDetail);
  updateEmailButtonLabels();
  updateGoogleButtonLabel();
  showGoogleMessage(googleAuthMessageKey);
  setOtpFieldError(otpPhoneInput, otpPhoneErrorKey, 'phone');
  setOtpFieldError(otpCodeInput, otpCodeErrorKey, 'code');
  updateButtonLabels();
});

handleGoogleOAuthCallback();
