// Shared browser authentication for LabourNearMe's static pages.
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
    document.querySelectorAll('[data-auth-signout]').forEach((button) => {
      button.addEventListener('click', async () => {
        button.disabled = true;
        let signedOut = false;
        try {
          await window.lnmAuth.signOut();
          signedOut = true;
          const status = document.getElementById('auth-status');
          if (status) status.textContent = authText('signedOut', 'You are signed out.');
        } catch (_) {
          const status = document.getElementById('auth-status');
          if (status) status.textContent = authText('signOutError', 'Could not sign out.');
        } finally {
          button.disabled = false;
          if (signedOut) button.hidden = true;
        }
      });
    });

    if (client) {
      client.auth.getSession().then(({ data }) => {
        if (data.session) document.querySelectorAll('[data-auth-signout]').forEach((button) => { button.hidden = false; });
      }).catch(() => {});
      client.auth.onAuthStateChange((event, session) => {
        document.querySelectorAll('[data-auth-signout]').forEach((button) => { button.hidden = !session; });
      });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bindSignOut, { once: true });
  else bindSignOut();
})();
