// Shared API configuration and JSON request handling for the static frontend.
window.LNM_API_BASE = 'https://labournearme.onrender.com';
window.lnmRequest = async function (path, options = {}) {
  const { authenticated = false, timeout: timeoutMs, ...requestOptions } = options;
  let accessToken = null;
  if (authenticated) {
    if (!window.lnmAuth || typeof window.lnmAuth.getAccessToken !== 'function') {
      throw new Error('Sign-in is required for this request.');
    }
    accessToken = await window.lnmAuth.getAccessToken();
    if (!accessToken) throw new Error('Your session has expired. Sign in and try again.');
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs || 45000);
  try {
    const response = await fetch(`${window.LNM_API_BASE}${path}`, {
      ...requestOptions,
      signal: requestOptions.signal || controller.signal,
      headers: {
        ...(requestOptions.body ? { 'Content-Type': 'application/json' } : {}),
        ...(requestOptions.headers || {}),
        ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {})
      }
    });
    const text = await response.text();
    let data = {};
    try { data = text ? JSON.parse(text) : {}; } catch (_) { data = { detail: text }; }
    if (!response.ok) {
      const detail = data.detail || data.message || `Request failed (${response.status})`;
      const error = new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
      error.status = response.status;
      error.payload = data;
      throw error;
    }
    return data;
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('The request timed out. The server may be starting; please try again.');
    if (error instanceof TypeError) throw new Error('Could not reach the server. Check your connection and try again.');
    throw error;
  } finally {
    clearTimeout(timeout);
  }
};
window.lnmGeolocation = function () {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) return reject(new Error('Location access is not available in this browser.'));
    navigator.geolocation.getCurrentPosition(
      position => resolve({ location_lat: position.coords.latitude, location_lng: position.coords.longitude }),
      error => reject(new Error(error.code === 1 ? 'Allow location access to use your current coordinates.' : 'Could not determine your location. Please try again.')),
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 60000 }
    );
  });
};
