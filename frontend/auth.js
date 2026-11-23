// Shared browser authentication for Shramik Setu's static pages.
(function () {
  'use strict';

  const config = window.LNM_SUPABASE_CONFIG;
  const sdk = window.supabase;
  let client = null;
  let clientInitializationError = '';

  try {
    if (!config || !config.url || !config.publishableKey) {
      throw new Error('Supabase public configuration is missing.');
    }
    if (!sdk || typeof sdk.createClient !== 'function') {
      throw new Error('Supabase JS did not load. Check your internet connection and refresh the page.');
    }
    client = sdk.createClient(config.url, config.publishableKey, {
      auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
    });
    window.lnmSupabase = client;
  } catch (error) {
    clientInitializationError = error && typeof error.message === 'string'
      ? error.message
      : 'Supabase could not be initialized. Refresh the page and try again.';
  }

  function requireClient() {
    if (!client) {
      throw new Error(clientInitializationError || 'Authentication is unavailable. Refresh the page and try again.');
    }
    return client;
  }

  function authText(key, fallback) {
    return window.LNM_I18N ? window.LNM_I18N.t(key) : fallback;
  }

  function hideAuthControlsWhileLoading() {
    document.querySelectorAll('[data-auth-login], [data-auth-signout]').forEach((element) => {
      element.hidden = true;
      element.style.setProperty('display', 'none', 'important');
    });
  }

  window.lnmAuth = {
    isAvailable() {
      return Boolean(client);
    },
    requestPhoneOtp(phone) {
      return requireClient().auth.signInWithOtp({
        phone,
        options: { shouldCreateUser: true }
      });
    },
    verifyPhoneOtp(phone, token) {
      return requireClient().auth.verifyOtp({ phone, token, type: 'sms' });
    },
    signInWithPassword(email, password) {
      return requireClient().auth.signInWithPassword({ email, password });
    },
    signUpWithPassword(email, password, emailRedirectTo) {
      return requireClient().auth.signUp({
        email,
        password,
        options: emailRedirectTo ? { emailRedirectTo } : {}
      });
    },
    async signOut() {
      const { error } = await requireClient().auth.signOut();
      if (error) throw error;
    },
    async getSession() {
      const { data, error } = await requireClient().auth.getSession();
      if (error) throw error;
      return data.session;
    },
    async getAccessToken() {
      const session = await this.getSession();
      return session ? session.access_token : null;
    }
  };

  function bindSignOut() {
    let authEventVersion = 0;
    let hasAuthenticatedSession = false;

    function setHidden(element, hidden) {
      element.hidden = hidden;
      if (hidden) element.style.setProperty('display', 'none', 'important');
      else element.style.removeProperty('display');
    }

    function updateAuthControls(session) {
      const validSession = Boolean(
        session &&
        session.access_token &&
        session.user && session.user.id &&
        (!Number.isFinite(Number(session.expires_at)) || Number(session.expires_at) > Date.now() / 1000)
      );
      hasAuthenticatedSession = validSession;
      document.querySelectorAll('[data-auth-signout]').forEach((button) => setHidden(button, !validSession));
      document.querySelectorAll('[data-auth-login]').forEach((link) => setHidden(link, validSession));
    }

    document.querySelectorAll('[data-auth-signout]').forEach((button) => {
      button.addEventListener('click', async () => {
        document.querySelectorAll('[data-auth-signout]').forEach((control) => { control.disabled = true; });
        const requestVersion = authEventVersion;
        try {
          await window.lnmAuth.signOut();
          if (authEventVersion === requestVersion) {
            authEventVersion += 1;
            updateAuthControls(null);
          }
          const status = document.getElementById('auth-status');
          if (status) status.textContent = authText('signedOut', 'You are signed out.');
          if (!hasAuthenticatedSession) window.location.assign('index.html');
        } catch (_) {
          const status = document.getElementById('auth-status');
          if (status) status.textContent = authText('signOutError', 'Could not sign out.');
        } finally {
          document.querySelectorAll('[data-auth-signout]').forEach((control) => { control.disabled = false; });
        }
      });
    });

    if (client) {
      // Controls start hidden in the markup. Resolve the initial state through
      // Supabase, while allowing newer auth events to supersede a stale lookup.
      const initialVersion = authEventVersion;
      client.auth.onAuthStateChange((event, session) => {
        authEventVersion += 1;
        updateAuthControls(session);
      });
      client.auth.getSession().then(({ data, error }) => {
        if (authEventVersion === initialVersion) updateAuthControls(error ? null : data.session);
      }).catch(() => {
        if (authEventVersion === initialVersion) updateAuthControls(null);
      });
    } else updateAuthControls(null);
  }

  hideAuthControlsWhileLoading();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bindSignOut, { once: true });
  else bindSignOut();
})();
