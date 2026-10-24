'use strict';

const otpPhoneInput = document.getElementById('otp-phone');
const otpCodeInput = document.getElementById('otp-code');
const otpCodeField = document.getElementById('otp-code-field');
const otpRequestButton = document.getElementById('request-otp');
const otpVerifyButton = document.getElementById('verify-otp');
const otpMessage = document.getElementById('otp-message');
const otpProfileChoice = document.getElementById('otp-profile-choice');
const otpNewUserConfirm = document.getElementById('otp-new-user-confirm');
let otpRequestedPhone = '';
let otpMessageKey = '';
let otpPhoneErrorKey = '';
let otpCodeErrorKey = '';
let otpRequestErrorDetail = '';
let requestingOtp = false;
let verifyingOtp = false;

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
  return role === 'worker' ? 'worker.html?complete_profile=worker' : 'post-job.html?complete_profile=employer';
}

function routeFromAuthProfile(response) {
  if (!response || typeof response.user_id !== 'string' || !response.user_id) {
    throw new Error('unexpected');
  }

  if (response.profile_status === 'missing' && response.needs_registration === true && response.profile === null) {
    otpNewUserConfirm.checked = false;
    otpProfileChoice.querySelectorAll('[data-otp-role]').forEach((button) => { button.disabled = true; });
    otpProfileChoice.hidden = false;
    showOtpMessage('');
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
    if (otpNewUserConfirm.checked && (role === 'worker' || role === 'employer')) window.location.href = profileUrl(role);
  });
});

otpNewUserConfirm.addEventListener('change', () => {
  otpProfileChoice.querySelectorAll('[data-otp-role]').forEach((button) => { button.disabled = !otpNewUserConfirm.checked; });
});

document.addEventListener('lnm-language-change', () => {
  showOtpMessage(otpMessageKey);
  setOtpFieldError(otpPhoneInput, otpPhoneErrorKey, 'phone');
  setOtpFieldError(otpCodeInput, otpCodeErrorKey, 'code');
  updateButtonLabels();
});
