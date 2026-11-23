(function () {
  'use strict';

  const authTranslations = {
    en: { phoneLoginWelcome: 'PHONE SIGN-IN', phoneAuthIntro: 'Sign in or create an account using a verified phone number.', otpSending: 'Sending code…', otpVerifying: 'Verifying…', otpNewUserConfirm: 'I have not registered a profile before.', signOut: 'Sign out', signedOut: 'You are signed out.', signOutError: 'Could not sign out.', phoneAuthRequired: 'A verified phone sign-in is required before profile registration.', phoneSignIn: 'Continue to phone sign-in', verifiedPhoneRequired: 'This account does not have a verified phone number. Sign in with phone OTP before continuing.', profileLookupUnauthorized: 'Your sign-in could not be verified. Sign in again with phone OTP.', profileLookupConflict: 'Multiple profiles are linked to this account. Contact support before continuing.', profileLookupFailed: 'Could not verify your profile with the server. Check your connection and try again.', profileResponseUnexpected: 'The server returned an unexpected profile response. No profile was created.', profileRegistrationFailed: 'Profile registration could not be confirmed. Do not retry until its status is checked.', profileRegistering: 'Registering profile…', registrationOutcomeUnknown: 'Registration not confirmed. Do not retry; contact support.', completeProfileAndPostJob: 'Complete profile and post job' },
    hi: { phoneLoginWelcome: 'फ़ोन से लॉग इन', phoneAuthIntro: 'सत्यापित फ़ोन नंबर से लॉग इन करें या नया खाता बनाएँ।', otpSending: 'कोड भेजा जा रहा है…', otpVerifying: 'सत्यापन हो रहा है…', otpNewUserConfirm: 'मैंने पहले कोई प्रोफ़ाइल पंजीकृत नहीं की है।', signOut: 'लॉग आउट', signedOut: 'आप लॉग आउट हो गए हैं।', signOutError: 'लॉग आउट नहीं हो सका।', phoneAuthRequired: 'प्रोफ़ाइल पंजीकरण से पहले सत्यापित फ़ोन लॉग इन आवश्यक है।', phoneSignIn: 'फ़ोन से लॉग इन जारी रखें', verifiedPhoneRequired: 'इस खाते में सत्यापित फ़ोन नंबर नहीं है। आगे बढ़ने के लिए फ़ोन OTP से लॉग इन करें।', profileLookupUnauthorized: 'आपका लॉग इन सत्यापित नहीं हो सका। फ़ोन OTP से फिर लॉग इन करें।', profileLookupConflict: 'इस खाते से कई प्रोफ़ाइल जुड़ी हैं। आगे बढ़ने से पहले सहायता से संपर्क करें।', profileLookupFailed: 'सर्वर से प्रोफ़ाइल की पुष्टि नहीं हो सकी। कनेक्शन जाँचकर फिर प्रयास करें।', profileResponseUnexpected: 'सर्वर से प्रोफ़ाइल का अप्रत्याशित उत्तर मिला। कोई प्रोफ़ाइल नहीं बनाई गई।', profileRegistrationFailed: 'प्रोफ़ाइल पंजीकरण की पुष्टि नहीं हुई। स्थिति जाँचे बिना दोबारा न करें।', profileRegistering: 'प्रोफ़ाइल पंजीकृत हो रही है…', registrationOutcomeUnknown: 'पंजीकरण की पुष्टि नहीं हुई। दोबारा न करें; सहायता से संपर्क करें।', completeProfileAndPostJob: 'प्रोफ़ाइल पूरी करें और नौकरी पोस्ट करें' },
    gu: { phoneLoginWelcome: 'ફોનથી લૉગ ઇન', phoneAuthIntro: 'ચકાસેલા ફોન નંબરથી લૉગ ઇન કરો અથવા નવું ખાતું બનાવો.', otpSending: 'કોડ મોકલાઈ રહ્યો છે…', otpVerifying: 'ચકાસણી થઈ રહી છે…', otpNewUserConfirm: 'મેં અગાઉ કોઈ પ્રોફાઇલ નોંધાવી નથી.', signOut: 'લૉગ આઉટ', signedOut: 'તમે લૉગ આઉટ થયા છો.', signOutError: 'લૉગ આઉટ થઈ શક્યું નથી.', phoneAuthRequired: 'પ્રોફાઇલ નોંધણી પહેલાં ચકાસેલું ફોન લૉગ ઇન જરૂરી છે.', phoneSignIn: 'ફોનથી લૉગ ઇન ચાલુ રાખો', verifiedPhoneRequired: 'આ ખાતામાં ચકાસેલો ફોન નંબર નથી. આગળ વધવા ફોન OTPથી લૉગ ઇન કરો.', profileLookupUnauthorized: 'તમારા લૉગ ઇનની પુષ્ટિ થઈ શકી નથી. ફોન OTPથી ફરી લૉગ ઇન કરો.', profileLookupConflict: 'આ ખાતા સાથે અનેક પ્રોફાઇલ જોડાયેલી છે. આગળ વધતાં પહેલાં સહાયનો સંપર્ક કરો.', profileLookupFailed: 'સર્વર પર પ્રોફાઇલની પુષ્ટિ થઈ શકી નથી. કનેક્શન તપાસીને ફરી પ્રયાસ કરો.', profileResponseUnexpected: 'સર્વર તરફથી પ્રોફાઇલનો અનપેક્ષિત જવાબ મળ્યો. કોઈ પ્રોફાઇલ બનાવાઈ નથી.', profileRegistrationFailed: 'પ્રોફાઇલ નોંધણીની પુષ્ટિ થઈ નથી. સ્થિતિ તપાસ્યા વિના ફરી પ્રયાસ ન કરો.', profileRegistering: 'પ્રોફાઇલ નોંધાઈ રહી છે…', registrationOutcomeUnknown: 'નોંધણીની પુષ્ટિ થઈ નથી. ફરી પ્રયાસ ન કરો; સહાયનો સંપર્ક કરો.', completeProfileAndPostJob: 'પ્રોફાઇલ પૂર્ણ કરો અને નોકરી પોસ્ટ કરો' },
    mr: { phoneLoginWelcome: 'फोनद्वारे लॉग इन', phoneAuthIntro: 'पडताळलेल्या फोन नंबरने लॉग इन करा किंवा नवीन खाते तयार करा.', otpSending: 'कोड पाठवत आहे…', otpVerifying: 'पडताळणी सुरू आहे…', otpNewUserConfirm: 'मी यापूर्वी कोणतेही प्रोफाइल नोंदवलेले नाही.', signOut: 'लॉग आउट', signedOut: 'तुम्ही लॉग आउट झाला आहात.', signOutError: 'लॉग आउट करता आले नाही.', phoneAuthRequired: 'प्रोफाइल नोंदणीपूर्वी पडताळलेले फोन लॉग इन आवश्यक आहे.', phoneSignIn: 'फोनद्वारे लॉग इन सुरू ठेवा', verifiedPhoneRequired: 'या खात्यात पडताळलेला फोन नंबर नाही. पुढे जाण्यासाठी फोन OTP ने लॉग इन करा.', profileLookupUnauthorized: 'तुमच्या लॉग इनची पुष्टी होऊ शकली नाही. फोन OTP ने पुन्हा लॉग इन करा.', profileLookupConflict: 'या खात्याशी अनेक प्रोफाइल जोडलेली आहेत. पुढे जाण्यापूर्वी मदतीशी संपर्क साधा.', profileLookupFailed: 'सर्व्हरवर प्रोफाइलची पुष्टी होऊ शकली नाही. कनेक्शन तपासून पुन्हा प्रयत्न करा.', profileResponseUnexpected: 'सर्व्हरकडून प्रोफाइलबाबत अनपेक्षित उत्तर मिळाले. कोणतेही प्रोफाइल तयार केले नाही.', profileRegistrationFailed: 'प्रोफाइल नोंदणीची पुष्टी झाली नाही. स्थिती तपासल्याशिवाय पुन्हा प्रयत्न करू नका.', profileRegistering: 'प्रोफाइल नोंदवत आहे…', registrationOutcomeUnknown: 'नोंदणीची पुष्टी झाली नाही. पुन्हा प्रयत्न करू नका; मदतीशी संपर्क साधा.', completeProfileAndPostJob: 'प्रोफाइल पूर्ण करा आणि नोकरी पोस्ट करा' }
  };

  Object.assign(authTranslations.en, {
    voiceSpeakCategory: 'Speak your work category', voiceListening: 'Listening… speak your work category.',
    voiceRecognized: 'Speech recognized. Review the category before submitting.',
    voiceUnsupported: 'Voice input is not supported in this browser. Type your category instead.',
    voicePermissionDenied: 'Microphone access was denied. Allow microphone access or type your category.',
    voiceNoSpeech: 'No speech was detected. Try again or type your category.', voiceError: 'Voice input failed. Type your category instead.'
  });
  Object.assign(authTranslations.hi, {
    voiceSpeakCategory: 'अपना काम बोलकर बताएँ', voiceListening: 'सुन रहा है… अपने काम की श्रेणी बोलें।',
    voiceRecognized: 'आवाज़ पहचानी गई। जमा करने से पहले श्रेणी जाँचें।',
    voiceUnsupported: 'इस ब्राउज़र में आवाज़ से लिखना उपलब्ध नहीं है। श्रेणी टाइप करें।',
    voicePermissionDenied: 'माइक्रोफ़ोन की अनुमति नहीं मिली। अनुमति दें या श्रेणी टाइप करें।',
    voiceNoSpeech: 'आवाज़ नहीं मिली। फिर कोशिश करें या श्रेणी टाइप करें।', voiceError: 'आवाज़ से लिखना विफल हुआ। श्रेणी टाइप करें।'
  });
  Object.assign(authTranslations.gu, {
    voiceSpeakCategory: 'તમારું કામ બોલીને જણાવો', voiceListening: 'સાંભળી રહ્યું છે… તમારા કામની શ્રેણી બોલો.',
    voiceRecognized: 'વાણી ઓળખાઈ. સબમિટ કરતાં પહેલાં શ્રેણી તપાસો.',
    voiceUnsupported: 'આ બ્રાઉઝરમાં અવાજથી લખવાનું ઉપલબ્ધ નથી. શ્રેણી ટાઇપ કરો.',
    voicePermissionDenied: 'માઇક્રોફોનની મંજૂરી ન મળી. મંજૂરી આપો અથવા શ્રેણી ટાઇપ કરો.',
    voiceNoSpeech: 'અવાજ સંભળાયો નહીં. ફરી પ્રયાસ કરો અથવા શ્રેણી ટાઇપ કરો.', voiceError: 'અવાજથી લખવાનું નિષ્ફળ થયું. શ્રેણી ટાઇપ કરો.'
  });
  Object.assign(authTranslations.mr, {
    voiceSpeakCategory: 'तुमचे काम बोलून सांगा', voiceListening: 'ऐकत आहे… तुमच्या कामाचा प्रकार सांगा.',
    voiceRecognized: 'आवाज ओळखला. सबमिट करण्यापूर्वी प्रकार तपासा.',
    voiceUnsupported: 'या ब्राउझरमध्ये आवाजाने टाइप करणे उपलब्ध नाही. कामाचा प्रकार टाइप करा.',
    voicePermissionDenied: 'मायक्रोफोनची परवानगी नाकारली. परवानगी द्या किंवा कामाचा प्रकार टाइप करा.',
    voiceNoSpeech: 'आवाज ऐकू आला नाही. पुन्हा प्रयत्न करा किंवा कामाचा प्रकार टाइप करा.', voiceError: 'आवाजाने टाइप करणे अयशस्वी झाले. कामाचा प्रकार टाइप करा.'
  });

  const translations = {
    en: {
      ...authTranslations.en,
      language: 'Language', features: 'Features', how: 'How It Works', about: 'About', login: 'Login', workerRegistration: 'Pro registration', getStarted: 'Get Started', work: 'Work', newTo: 'New to Shramik Setu?', loginHeadline: 'Good work starts with a connection.', loginWelcomeDescription: 'Sign in to continue with Shramik Setu, whether you’re looking for work or building your team.', loginGroupsConnected: 'Connecting Patrons and Pros across Bharat.', welcomeEyebrow: 'A better way to find work', show: 'Show', hide: 'Hide',
      signIn: 'Sign in', signInTitle: 'Sign in to your account', createAccountAction: 'Create account',
      otpDivider: 'Use your phone number to receive a one-time code.', otpPhoneHint: 'Include your country code, for example +91.', sendOtp: 'Send verification code', otpCode: 'Verification code', otpCodeHint: 'Enter the code sent to your phone.', verifyOtp: 'Verify and continue', otpMissingProfileNotice: 'No profile is linked to this verified phone account. If you registered before, stop and contact support before continuing; creating another profile could duplicate your account.', chooseProfileType: 'Choose which profile to complete:', otpPhoneRequired: 'Enter your phone number.', otpPhoneInvalid: 'Use an international number with country code, for example +919876543210.', otpCodeRequired: 'Enter the verification code.', otpSent: 'A verification code was sent. Check your phone.', otpRequestError: 'Could not send the code. Check the number and try again.', otpVerificationError: 'The code could not be verified. Check it and try again.', otpSessionError: 'Verification did not return an active sign-in session.', otpAuthRequired: 'Your sign-in could not be confirmed by the server. Please sign in again.', otpProfileConflict: 'More than one profile is linked to this account. Contact support before continuing.', otpProfileLookupError: 'Could not verify your profile with the server. Check your connection and try again.', otpUnexpectedResponse: 'The server returned an unexpected profile response. Please try again later.',
      haveAccount: 'Already have an account?', profileContinueWarning: 'Sign-in did not create a profile. Continue only if you have not already registered a', profileContinueSuffix: 'profile.', continueTo: 'Continue to', profile: 'profile',
      gov: 'A Digital India Initiative · Connecting Pros Across Bharat · सुरक्षित · विश्वसनीय · आसान',
      connect: 'Connecting Patrons and Pros across Bharat', find: 'Find', or: 'or', hireWorkers: 'Hire Pros', nearYou: 'Near You',
      description: 'A digital platform for Patrons and Pros, with local job listings and skill-based recommendations.',
      joinWorker: 'Join as Pro', browseHire: 'Browse jobs near you & get hired fast', postFind: 'Post a job & find skilled pros today', already: 'Already have an account?', worker: 'Pro', employer: 'Patron',
      loginTitle: 'Sign in to your account', createAccount: 'Create your account', chooseAccount: 'Choose your account type to get started.', roleSignin: 'I am signing in as', roleSignup: 'Create an account as', email: 'Email address', password: 'Password',
      backHome: 'Back to home', welcome: 'WELCOME BACK', workerNearby: 'Find work nearby', employerHire: 'Hire local talent', noteSignin: 'Sign in with your Shramik Setu email and password.', noteSignup: 'Create an account with your email and password. You will complete your Patron or Pro profile next.',
      fullName: 'Full Name', phone: 'Phone Number', skills: 'Skills', category: 'Work category', location: 'Location', experience: 'Experience', wage: 'Expected daily wage (₹)',
      enterName: 'Enter your full name', enterLocation: 'Enter your city or area', addSkill: 'Type a skill and press Enter (e.g. Carpenter)', registerWorker: 'Register as Pro', profileTitle: 'Pro Registration',
      requiredSkills: 'Required skills', skillSelectPlaceholder: 'Choose a skill…', skillAdd: 'Add skill', skillSelectedHeading: 'Selected skills', skillNoSelection: 'No skills selected', skillRemove: 'Remove', skillLoading: 'Loading skills…', skillEmpty: 'No skills are available right now.', skillLoadError: 'Could not load skills. Check your connection and try again.', skillRetry: 'Try again', skillOtherCategory: 'Other skills', skillRequiredWorker: 'Please select at least one skill', skillRequiredJob: 'Please select at least one required skill',
      profileDesc: 'Create a pro profile with your contact details, skills, expected daily wage, and current coordinates.',
      registration: 'Pro Registration', fillDetails: 'Fill your details to get started — takes 2 minutes', completion: 'Profile Completion', optional: 'OPTIONAL DETAILS',
      yearsHint: 'Enter complete years as a whole number. A fresher can enter 0 years.', wageHint: 'This amount is saved as your expected daily wage.',
      selectLanguage: 'Select language'
    },
    hi: {
      ...authTranslations.hi,
      language: 'भाषा', features: 'विशेषताएँ', how: 'यह कैसे काम करता है', about: 'हमारे बारे में', login: 'लॉग इन', workerRegistration: 'साथी पंजीकरण', getStarted: 'शुरू करें', work: 'काम', newTo: 'Shramik Setu पर नए हैं?', loginHeadline: 'अच्छे काम की शुरुआत सही जुड़ाव से होती है।', loginWelcomeDescription: 'काम खोजने या अपनी टीम बनाने के लिए Shramik Setu पर लॉग इन करें।', loginGroupsConnected: 'भारत भर में नियोजक और साथी जुड़ते हैं।', welcomeEyebrow: 'काम खोजने का बेहतर तरीका', show: 'दिखाएँ', hide: 'छिपाएँ', signIn: 'लॉग इन', signInTitle: 'अपने खाते में लॉग इन करें', createAccountAction: 'खाता बनाएँ',
      haveAccount: 'पहले से खाता है?', profileContinueWarning: 'लॉग इन से प्रोफ़ाइल नहीं बनी। तभी आगे बढ़ें जब आपने पहले से यह प्रोफ़ाइल न बनाई हो:', profileContinueSuffix: 'प्रोफ़ाइल।', continueTo: 'आगे बढ़ें:', profile: 'प्रोफ़ाइल',
      otpDivider: 'कोड पाने के लिए अपना फ़ोन नंबर इस्तेमाल करें।', otpPhoneHint: 'देश का कोड शामिल करें, जैसे +91।', sendOtp: 'सत्यापन कोड भेजें', otpCode: 'सत्यापन कोड', otpCodeHint: 'अपने फ़ोन पर आया कोड दर्ज करें।', verifyOtp: 'सत्यापित करें और आगे बढ़ें', otpMissingProfileNotice: 'इस सत्यापित फ़ोन खाते से कोई प्रोफ़ाइल जुड़ी नहीं है। यदि आपने पहले पंजीकरण किया है, तो रुकें और सहायता से संपर्क करें; नई प्रोफ़ाइल बनाने से दोहराव हो सकता है।', chooseProfileType: 'कौन-सी प्रोफ़ाइल पूरी करनी है चुनें:', otpPhoneRequired: 'अपना फ़ोन नंबर दर्ज करें।', otpPhoneInvalid: 'देश कोड सहित अंतरराष्ट्रीय नंबर डालें, जैसे +919876543210।', otpCodeRequired: 'सत्यापन कोड दर्ज करें।', otpSent: 'सत्यापन कोड भेज दिया गया है। अपना फ़ोन देखें।', otpRequestError: 'कोड नहीं भेजा जा सका। नंबर जाँचकर फिर प्रयास करें।', otpVerificationError: 'कोड सत्यापित नहीं हो सका। जाँचकर फिर प्रयास करें।', otpSessionError: 'सत्यापन के बाद सक्रिय साइन-इन सत्र नहीं मिला।', otpAuthRequired: 'सर्वर आपके साइन-इन की पुष्टि नहीं कर सका। कृपया फिर से लॉग इन करें।', otpProfileConflict: 'इस खाते से एक से अधिक प्रोफ़ाइल जुड़ी हैं। आगे बढ़ने से पहले सहायता से संपर्क करें।', otpProfileLookupError: 'सर्वर से प्रोफ़ाइल की पुष्टि नहीं हो सकी। कनेक्शन जाँचकर फिर प्रयास करें।', otpUnexpectedResponse: 'सर्वर से प्रोफ़ाइल का अप्रत्याशित उत्तर मिला। बाद में फिर प्रयास करें।',
      gov: 'डिजिटल इंडिया पहल · भारत भर के साथियों को जोड़ना · सुरक्षित · विश्वसनीय · आसान', connect: 'नियोजक और साथी को जोड़ना', find: 'काम खोजें', or: 'या', hireWorkers: 'साथी नियुक्त करें', nearYou: 'अपने पास',
      description: 'नियोजक और साथी को स्थानीय नौकरियों और कौशल सुझावों से जोड़ने वाला डिजिटल मंच।', joinWorker: 'साथी के रूप में जुड़ें', browseHire: 'पास में काम खोजें और जल्दी नियुक्त हों', postFind: 'नौकरी पोस्ट करें और कुशल साथी खोजें', already: 'पहले से खाता है?', worker: 'साथी', employer: 'नियोजक',
      loginTitle: 'अपने खाते में लॉग इन करें', createAccount: 'अपना खाता बनाएँ', chooseAccount: 'शुरू करने के लिए अपना खाता प्रकार चुनें।', roleSignin: 'मैं लॉग इन कर रहा/रही हूँ', roleSignup: 'इस रूप में खाता बनाएँ', email: 'ईमेल पता', password: 'पासवर्ड', backHome: 'होम पर वापस जाएँ', welcome: 'वापसी पर स्वागत है', workerNearby: 'पास में काम खोजें', employerHire: 'स्थानीय प्रतिभा नियुक्त करें', noteSignin: 'अपने Shramik Setu ईमेल और पासवर्ड से लॉग इन करें।', noteSignup: 'ईमेल और पासवर्ड से खाता बनाएँ। इसके बाद नियोजक या साथी की प्रोफ़ाइल पूरी करें।',
      fullName: 'पूरा नाम', phone: 'फ़ोन नंबर', skills: 'कौशल', category: 'काम की श्रेणी', location: 'स्थान', experience: 'अनुभव', wage: 'अपेक्षित दैनिक मज़दूरी (₹)', enterName: 'अपना पूरा नाम लिखें', enterLocation: 'अपना शहर या क्षेत्र लिखें', addSkill: 'कौशल लिखें और Enter दबाएँ (जैसे बढ़ई)', registerWorker: 'साथी के रूप में पंजीकरण करें', profileTitle: 'साथी पंजीकरण', profileDesc: 'अपनी संपर्क जानकारी, कौशल, दैनिक मज़दूरी और वर्तमान निर्देशांकों के साथ साथी प्रोफ़ाइल बनाएँ।', registration: 'साथी पंजीकरण', fillDetails: 'शुरू करने के लिए विवरण भरें — 2 मिनट लगेंगे', completion: 'प्रोफ़ाइल पूर्णता', optional: 'वैकल्पिक विवरण', yearsHint: 'पूरे वर्षों की संख्या दर्ज करें। नए साथी 0 वर्ष दर्ज कर सकते हैं।', wageHint: 'यह राशि आपकी अपेक्षित दैनिक मज़दूरी के रूप में सहेजी जाएगी।', selectLanguage: 'भाषा चुनें'
    },
    gu: {
      ...authTranslations.gu,
      language: 'ભાષા', features: 'સુવિધાઓ', how: 'કેવી રીતે કાર્ય કરે છે', about: 'વિશે', login: 'લૉગ ઇન', workerRegistration: 'સાથી નોંધણી', getStarted: 'શરૂ કરો', work: 'કામ', newTo: 'Shramik Setu પર નવા છો?', loginHeadline: 'સારા કામની શરૂઆત યોગ્ય જોડાણથી થાય છે.', loginWelcomeDescription: 'કામ શોધવા અથવા તમારી ટીમ બનાવવા Shramik Setuમાં લૉગ ઇન કરો.', loginGroupsConnected: 'ભારતભરના નિયોજક અને સાથીને જોડે છે.', welcomeEyebrow: 'કામ શોધવાની વધુ સારી રીત', show: 'બતાવો', hide: 'છુપાવો', signIn: 'લૉગ ઇન', signInTitle: 'તમારા ખાતામાં લૉગ ઇન કરો', createAccountAction: 'ખાતું બનાવો',
      haveAccount: 'પહેલેથી ખાતું છે?', profileContinueWarning: 'લૉગ ઇનથી પ્રોફાઇલ બની નથી. તમે આ પ્રોફાઇલ પહેલેથી બનાવી ન હોય ત્યારે જ આગળ વધો:', profileContinueSuffix: 'પ્રોફાઇલ.', continueTo: 'આગળ વધો:', profile: 'પ્રોફાઇલ',
      otpDivider: 'એક વખતનો કોડ મેળવવા ફોન નંબર વાપરો.', otpPhoneHint: 'દેશનો કોડ ઉમેરો, ઉદાહરણ તરીકે +91.', sendOtp: 'ચકાસણી કોડ મોકલો', otpCode: 'ચકાસણી કોડ', otpCodeHint: 'તમારા ફોન પર આવેલો કોડ દાખલ કરો.', verifyOtp: 'ચકાસો અને આગળ વધો', otpMissingProfileNotice: 'આ ચકાસેલા ફોન ખાતા સાથે કોઈ પ્રોફાઇલ જોડાયેલી નથી. અગાઉ નોંધણી કરી હોય તો અટકો અને સહાયનો સંપર્ક કરો; બીજી પ્રોફાઇલથી નકલ થઈ શકે છે.', chooseProfileType: 'કઈ પ્રોફાઇલ પૂર્ણ કરવી તે પસંદ કરો:', otpPhoneRequired: 'તમારો ફોન નંબર દાખલ કરો.', otpPhoneInvalid: 'દેશના કોડ સાથે આંતરરાષ્ટ્રીય નંબર વાપરો, જેમ કે +919876543210.', otpCodeRequired: 'ચકાસણી કોડ દાખલ કરો.', otpSent: 'ચકાસણી કોડ મોકલ્યો છે. તમારો ફોન તપાસો.', otpRequestError: 'કોડ મોકલી શકાયો નથી. નંબર તપાસીને ફરી પ્રયાસ કરો.', otpVerificationError: 'કોડ ચકાસી શકાયો નથી. તપાસીને ફરી પ્રયાસ કરો.', otpSessionError: 'ચકાસણી પછી સક્રિય લૉગ ઇન સત્ર મળ્યું નથી.', otpAuthRequired: 'સર્વર તમારા લૉગ ઇનની પુષ્ટિ કરી શક્યું નથી. ફરી લૉગ ઇન કરો.', otpProfileConflict: 'આ ખાતા સાથે એકથી વધુ પ્રોફાઇલ જોડાયેલી છે. આગળ વધતાં પહેલાં સહાયનો સંપર્ક કરો.', otpProfileLookupError: 'સર્વર પર પ્રોફાઇલની પુષ્ટિ થઈ શકી નથી. કનેક્શન તપાસીને ફરી પ્રયાસ કરો.', otpUnexpectedResponse: 'સર્વર તરફથી પ્રોફાઇલનો અનપેક્ષિત જવાબ મળ્યો. પછીથી ફરી પ્રયાસ કરો.',
      gov: 'ડિજિટલ ઇન્ડિયા પહેલ · ભારતભરના સાથીઓને જોડે છે · સુરક્ષિત · વિશ્વસનીય · સરળ', connect: 'નિયોજક અને સાથીને જોડે છે', find: 'કામ શોધો', or: 'અથવા', hireWorkers: 'સાથીઓ રાખો', nearYou: 'તમારી નજીક',
      description: 'નિયોજક અને સાથીને સ્થાનિક નોકરીઓ અને કૌશલ્ય સૂચનો સાથે જોડતું ડિજિટલ પ્લેટફોર્મ.', joinWorker: 'સાથી તરીકે જોડાઓ', browseHire: 'નજીકમાં કામ શોધો અને ઝડપથી નોકરી મેળવો', postFind: 'નોકરી મૂકો અને કુશળ સાથીઓ શોધો', already: 'પહેલેથી ખાતું છે?', worker: 'સાથી', employer: 'નિયોજક',
      loginTitle: 'તમારા ખાતામાં લૉગ ઇન કરો', createAccount: 'તમારું ખાતું બનાવો', chooseAccount: 'શરૂ કરવા માટે ખાતાનો પ્રકાર પસંદ કરો.', roleSignin: 'હું આ તરીકે લૉગ ઇન કરું છું', roleSignup: 'આ તરીકે ખાતું બનાવો', email: 'ઇમેઇલ સરનામું', password: 'પાસવર્ડ', backHome: 'હોમ પર પાછા જાઓ', welcome: 'ફરી સ્વાગત છે', workerNearby: 'નજીકમાં કામ શોધો', employerHire: 'સ્થાનિક કુશળ લોકોને રાખો', noteSignin: 'તમારા Shramik Setu ઇમેઇલ અને પાસવર્ડથી લૉગ ઇન કરો.', noteSignup: 'ઇમેઇલ અને પાસવર્ડથી ખાતું બનાવો. પછી સાથી અથવા નિયોજકની પ્રોફાઇલ પૂર્ણ કરો.',
      fullName: 'પૂરું નામ', phone: 'ફોન નંબર', skills: 'કૌશલ્યો', category: 'કામનો પ્રકાર', location: 'સ્થળ', experience: 'અનુભવ', wage: 'અપેક્ષિત દૈનિક વેતન (₹)', enterName: 'તમારું પૂરું નામ લખો', enterLocation: 'તમારું શહેર અથવા વિસ્તાર લખો', addSkill: 'કૌશલ્ય લખો અને Enter દબાવો (દા.ત. સુથાર)', registerWorker: 'સાથી તરીકે નોંધણી કરો', profileTitle: 'સાથી નોંધણી', profileDesc: 'તમારી સંપર્ક વિગતો, કૌશલ્યો, અપેક્ષિત દૈનિક વેતન અને વર્તમાન સ્થાન સાથે પ્રોફાઇલ બનાવો.', registration: 'સાથી નોંધણી', fillDetails: 'શરૂ કરવા માટે વિગતો ભરો — 2 મિનિટ લાગશે', completion: 'પ્રોફાઇલ પૂર્ણતા', optional: 'વૈકલ્પિક વિગતો', yearsHint: 'પૂર્ણ વર્ષોની સંખ્યા દાખલ કરો. નવા સાથી 0 વર્ષ દાખલ કરી શકે છે.', wageHint: 'આ રકમ અપેક્ષિત દૈનિક વેતન તરીકે સાચવાશે.', selectLanguage: 'ભાષા પસંદ કરો'
    },
    mr: {
      ...authTranslations.mr,
      language: 'भाषा', features: 'वैशिष्ट्ये', how: 'हे कसे कार्य करते', about: 'आमच्याबद्दल', login: 'लॉग इन', workerRegistration: 'साथी नोंदणी', getStarted: 'सुरू करा', work: 'काम', newTo: 'Shramik Setu वर नवीन आहात?', loginHeadline: 'चांगल्या कामाची सुरुवात योग्य जोडणीतून होते.', loginWelcomeDescription: 'काम शोधण्यासाठी किंवा तुमची टीम तयार करण्यासाठी Shramik Setu वर लॉग इन करा.', loginGroupsConnected: 'भारतभरातील नियोजक आणि साथी यांना जोडतो.', welcomeEyebrow: 'काम शोधण्याचा चांगला मार्ग', show: 'दाखवा', hide: 'लपवा', signIn: 'लॉग इन', signInTitle: 'तुमच्या खात्यात लॉग इन करा', createAccountAction: 'खाते तयार करा',
      haveAccount: 'आधीच खाते आहे?', profileContinueWarning: 'लॉग इनमुळे प्रोफाइल तयार झाले नाही. आधी हे प्रोफाइल तयार केले नसेल तरच पुढे जा:', profileContinueSuffix: 'प्रोफाइल.', continueTo: 'पुढे जा:', profile: 'प्रोफाइल',
      otpDivider: 'एकवेळचा कोड मिळवण्यासाठी फोन नंबर वापरा.', otpPhoneHint: 'देशाचा कोड समाविष्ट करा, उदाहरणार्थ +91.', sendOtp: 'पडताळणी कोड पाठवा', otpCode: 'पडताळणी कोड', otpCodeHint: 'फोनवर आलेला कोड टाका.', verifyOtp: 'पडताळा आणि पुढे जा', otpMissingProfileNotice: 'या पडताळलेल्या फोन खात्याशी प्रोफाइल जोडलेले नाही. आधी नोंदणी केली असल्यास थांबा आणि मदतीशी संपर्क साधा; नवीन प्रोफाइलमुळे डुप्लिकेट होऊ शकते.', chooseProfileType: 'कोणते प्रोफाइल पूर्ण करायचे ते निवडा:', otpPhoneRequired: 'तुमचा फोन नंबर टाका.', otpPhoneInvalid: 'देशाच्या कोडसह आंतरराष्ट्रीय नंबर वापरा, उदा. +919876543210.', otpCodeRequired: 'पडताळणी कोड टाका.', otpSent: 'पडताळणी कोड पाठवला आहे. फोन तपासा.', otpRequestError: 'कोड पाठवता आला नाही. नंबर तपासून पुन्हा प्रयत्न करा.', otpVerificationError: 'कोड पडताळता आला नाही. तपासून पुन्हा प्रयत्न करा.', otpSessionError: 'पडताळणीनंतर सक्रिय लॉग इन सत्र मिळाले नाही.', otpAuthRequired: 'सर्व्हर तुमच्या लॉग इनची पुष्टी करू शकला नाही. पुन्हा लॉग इन करा.', otpProfileConflict: 'या खात्याशी एकापेक्षा जास्त प्रोफाइल जोडलेली आहेत. पुढे जाण्यापूर्वी मदतीशी संपर्क साधा.', otpProfileLookupError: 'सर्व्हरवर प्रोफाइलची पुष्टी होऊ शकली नाही. कनेक्शन तपासून पुन्हा प्रयत्न करा.', otpUnexpectedResponse: 'सर्व्हरकडून प्रोफाइलबाबत अनपेक्षित उत्तर मिळाले. नंतर पुन्हा प्रयत्न करा.',
      gov: 'डिजिटल इंडिया उपक्रम · भारतभरातील साथींना जोडतो · सुरक्षित · विश्वासार्ह · सोपे', connect: 'नियोजक आणि साथी यांना जोडतो', find: 'काम शोधा', or: 'किंवा', hireWorkers: 'साथी नियुक्त करा', nearYou: 'तुमच्या जवळ',
      description: 'नियोजक आणि साथी यांना स्थानिक नोकऱ्या व कौशल्य सूचनांशी जोडणारे डिजिटल व्यासपीठ.', joinWorker: 'साथी म्हणून सामील व्हा', browseHire: 'जवळचे काम शोधा आणि लवकर नोकरी मिळवा', postFind: 'नोकरी पोस्ट करा आणि कुशल साथी शोधा', already: 'आधीच खाते आहे?', worker: 'साथी', employer: 'नियोजक',
      loginTitle: 'तुमच्या खात्यात लॉग इन करा', createAccount: 'तुमचे खाते तयार करा', chooseAccount: 'सुरू करण्यासाठी खाते प्रकार निवडा.', roleSignin: 'मी याप्रमाणे लॉग इन करत आहे', roleSignup: 'याप्रमाणे खाते तयार करा', email: 'ईमेल पत्ता', password: 'पासवर्ड', backHome: 'मुख्यपृष्ठावर परत जा', welcome: 'पुन्हा स्वागत आहे', workerNearby: 'जवळचे काम शोधा', employerHire: 'स्थानिक कुशल लोकांना नियुक्त करा', noteSignin: 'तुमच्या Shramik Setu ईमेल आणि पासवर्डने लॉग इन करा.', noteSignup: 'ईमेल आणि पासवर्डने खाते तयार करा. त्यानंतर नियोजक किंवा साथी प्रोफाइल पूर्ण करा.',
      fullName: 'पूर्ण नाव', phone: 'फोन नंबर', skills: 'कौशल्ये', category: 'कामाचा प्रकार', location: 'ठिकाण', experience: 'अनुभव', wage: 'अपेक्षित दैनिक मजुरी (₹)', enterName: 'तुमचे पूर्ण नाव लिहा', enterLocation: 'तुमचे शहर किंवा परिसर लिहा', addSkill: 'कौशल्य लिहा आणि Enter दाबा (उदा. सुतार)', registerWorker: 'साथी म्हणून नोंदणी करा', profileTitle: 'साथी नोंदणी', profileDesc: 'तुमचे संपर्क तपशील, कौशल्ये, अपेक्षित दैनिक मजुरी आणि सध्याचे स्थान देऊन प्रोफाइल तयार करा.', registration: 'साथी नोंदणी', fillDetails: 'सुरू करण्यासाठी तपशील भरा — 2 मिनिटे लागतील', completion: 'प्रोफाइल पूर्णता', optional: 'पर्यायी तपशील', yearsHint: 'पूर्ण वर्षांची संख्या द्या. नवीन साथी 0 वर्षे देऊ शकतो.', wageHint: 'ही रक्कम अपेक्षित दैनिक मजुरी म्हणून जतन केली जाईल.', selectLanguage: 'भाषा निवडा'
    }
  };

  const emailAuthTranslations = {
    en: {
      emailFallbackHeading: 'Email/password demo fallback', emailFallbackDescription: 'Use an email account if SMS delivery is unavailable.',
      authSignIn: 'Continue to sign-in',
      emailRoleLabel: 'Profile type for a new account', emailRoleOptional: 'Choose only when creating an account',
      emailSignIn: 'Sign in with email', emailSignUp: 'Create email account', emailWorking: 'Checking your account…',
      emailConfirmRequired: 'Account creation is not complete yet. Check your email and confirm the address; your profile has not been submitted.',
      emailNoSession: 'Supabase did not return a sign-in session. No profile was submitted.', emailRoleRequired: 'Choose a Patron or Pro profile before creating an account.', emailSignOutFirst: 'Sign out of the current account before creating a separate email account. Accounts are not linked automatically.',
      emailAuthFailed: 'Email sign-in or registration failed:', profileMissingNotice: 'No application profile is linked to this account. If you already registered, stop and contact support before continuing; creating another profile could duplicate it.',
      verifiedAuthRequired: 'A confirmed phone or email sign-in is required before profile registration.'
    },
    hi: {
      emailFallbackHeading: 'डेमो के लिए ईमेल/पासवर्ड विकल्प', emailFallbackDescription: 'SMS न मिलने पर ईमेल खाते का उपयोग करें।',
      authSignIn: 'लॉग इन जारी रखें',
      emailRoleLabel: 'नए खाते के लिए प्रोफ़ाइल प्रकार', emailRoleOptional: 'केवल नया खाता बनाते समय चुनें',
      emailSignIn: 'ईमेल से लॉग इन करें', emailSignUp: 'ईमेल खाता बनाएँ', emailWorking: 'खाते की जाँच हो रही है…',
      emailConfirmRequired: 'खाता बनाना अभी पूरा नहीं हुआ है। ईमेल देखें और पते की पुष्टि करें; प्रोफ़ाइल अभी जमा नहीं की गई है।',
      emailNoSession: 'Supabase से लॉग इन सत्र नहीं मिला। प्रोफ़ाइल जमा नहीं की गई।', emailRoleRequired: 'खाता बनाने से पहले नियोजक या साथी चुनें।', emailSignOutFirst: 'अलग ईमेल खाता बनाने से पहले मौजूदा खाते से लॉग आउट करें। खाते अपने आप नहीं जुड़ते।',
      emailAuthFailed: 'ईमेल लॉग इन या पंजीकरण विफल हुआ:', profileMissingNotice: 'इस खाते से कोई प्रोफ़ाइल जुड़ी नहीं है। पहले पंजीकरण किया हो तो रुकें और सहायता से संपर्क करें; दूसरी प्रोफ़ाइल से दोहराव हो सकता है।',
      verifiedAuthRequired: 'प्रोफ़ाइल पंजीकरण से पहले पुष्टि किया हुआ फ़ोन या ईमेल लॉग इन आवश्यक है।'
    },
    gu: {
      emailFallbackHeading: 'ડેમો માટે ઇમેઇલ/પાસવર્ડ વિકલ્પ', emailFallbackDescription: 'SMS ન મળે તો ઇમેઇલ ખાતાનો ઉપયોગ કરો.',
      authSignIn: 'લૉગ ઇન ચાલુ રાખો',
      emailRoleLabel: 'નવા ખાતા માટે પ્રોફાઇલનો પ્રકાર', emailRoleOptional: 'ખાતું બનાવતી વખતે જ પસંદ કરો',
      emailSignIn: 'ઇમેઇલથી લૉગ ઇન કરો', emailSignUp: 'ઇમેઇલ ખાતું બનાવો', emailWorking: 'તમારા ખાતાની તપાસ થઈ રહી છે…',
      emailConfirmRequired: 'ખાતું બનાવવાની પ્રક્રિયા હજુ પૂર્ણ નથી. ઇમેઇલ તપાસીને સરનામું ચકાસો; પ્રોફાઇલ મોકલાઈ નથી.',
      emailNoSession: 'Supabase તરફથી લૉગ ઇન સત્ર મળ્યું નથી. પ્રોફાઇલ મોકલાઈ નથી.', emailRoleRequired: 'ખાતું બનાવતાં પહેલાં નિયોજક અથવા સાથી પસંદ કરો.', emailSignOutFirst: 'અલગ ઇમેઇલ ખાતું બનાવતાં પહેલાં વર્તમાન ખાતામાંથી લૉગ આઉટ કરો. ખાતાં આપમેળે જોડાતા નથી.',
      emailAuthFailed: 'ઇમેઇલ લૉગ ઇન અથવા નોંધણી નિષ્ફળ:', profileMissingNotice: 'આ ખાતા સાથે કોઈ પ્રોફાઇલ જોડાયેલી નથી. અગાઉ નોંધણી કરી હોય તો અટકો અને સહાયનો સંપર્ક કરો; બીજી પ્રોફાઇલથી નકલ થઈ શકે છે.',
      verifiedAuthRequired: 'પ્રોફાઇલ નોંધણી પહેલાં ચકાસેલું ફોન અથવા ઇમેઇલ લૉગ ઇન જરૂરી છે.'
    },
    mr: {
      emailFallbackHeading: 'डेमोसाठी ईमेल/पासवर्ड पर्याय', emailFallbackDescription: 'SMS मिळत नसल्यास ईमेल खाते वापरा.',
      authSignIn: 'लॉग इन सुरू ठेवा',
      emailRoleLabel: 'नवीन खात्यासाठी प्रोफाइलचा प्रकार', emailRoleOptional: 'फक्त खाते तयार करताना निवडा',
      emailSignIn: 'ईमेलने लॉग इन करा', emailSignUp: 'ईमेल खाते तयार करा', emailWorking: 'खात्याची तपासणी सुरू आहे…',
      emailConfirmRequired: 'खाते तयार करणे अजून पूर्ण झालेले नाही. ईमेल तपासून पत्त्याची पुष्टी करा; प्रोफाइल पाठवलेले नाही.',
      emailNoSession: 'Supabase कडून लॉग इन सत्र मिळाले नाही. प्रोफाइल पाठवलेले नाही.', emailRoleRequired: 'खाते तयार करण्यापूर्वी नियोजक किंवा साथी निवडा.', emailSignOutFirst: 'वेगळे ईमेल खाते तयार करण्यापूर्वी सध्याच्या खात्यातून लॉग आउट करा. खाती आपोआप जोडली जात नाहीत.',
      emailAuthFailed: 'ईमेल लॉग इन किंवा नोंदणी अयशस्वी:', profileMissingNotice: 'या खात्याशी कोणतेही प्रोफाइल जोडलेले नाही. आधी नोंदणी केली असल्यास थांबा आणि मदतीशी संपर्क साधा; दुसऱ्या प्रोफाइलमुळे डुप्लिकेट होऊ शकते.',
      verifiedAuthRequired: 'प्रोफाइल नोंदणीपूर्वी पुष्टी केलेले फोन किंवा ईमेल लॉग इन आवश्यक आहे.'
    }
  };

  const googleAuthTranslations = {
    en: {
      googleSignIn: 'Continue with Google', googleWorking: 'Connecting to Google…',
      googleStarting: 'Opening Google sign-in…', googleCheckingProfile: 'Checking your Shramik Setu profile…',
      googleCancelled: 'Google sign-in was cancelled. You can try again.',
      googleNoSession: 'Google sign-in returned no active session. Please try again.',
      googleAuthRequired: 'Your sign-in session could not be verified. Please sign in again.',
      googleServiceUnavailable: 'Sign-in service temporarily unavailable. Please try again later.',
      googleProfileLookupError: 'Could not verify your profile with the server. Check your connection and try again.',
      googleFailed: 'Could not sign in with Google. Please try again.',
      googleRedirectFailed: 'Google sign-in did not start. Please try again.'
    },
    hi: {
      googleSignIn: 'Google से जारी रखें', googleWorking: 'Google से कनेक्ट हो रहा है…',
      googleStarting: 'Google साइन-इन खोला जा रहा है…', googleCheckingProfile: 'आपकी Shramik Setu प्रोफ़ाइल जाँची जा रही है…',
      googleCancelled: 'Google साइन-इन रद्द हुआ। आप फिर से कोशिश कर सकते हैं।',
      googleNoSession: 'Google साइन-इन से सक्रिय सत्र नहीं मिला। कृपया फिर कोशिश करें।',
      googleAuthRequired: 'आपके साइन-इन सत्र की पुष्टि नहीं हो सकी। कृपया फिर साइन इन करें।',
      googleServiceUnavailable: 'साइन-इन सेवा अभी उपलब्ध नहीं है। कृपया बाद में फिर कोशिश करें।',
      googleProfileLookupError: 'सर्वर से आपकी प्रोफ़ाइल की पुष्टि नहीं हो सकी। कनेक्शन जाँचकर फिर कोशिश करें।',
      googleFailed: 'Google से साइन इन नहीं हो सका। कृपया फिर कोशिश करें।',
      googleRedirectFailed: 'Google साइन-इन शुरू नहीं हुआ। कृपया फिर कोशिश करें.'
    },
    gu: {
      googleSignIn: 'Google સાથે ચાલુ રાખો', googleWorking: 'Google સાથે કનેક્ટ થઈ રહ્યું છે…',
      googleStarting: 'Google લૉગ ઇન ખોલાઈ રહ્યું છે…', googleCheckingProfile: 'તમારી Shramik Setu પ્રોફાઇલ તપાસાઈ રહી છે…',
      googleCancelled: 'Google લૉગ ઇન રદ થયું. તમે ફરી પ્રયાસ કરી શકો છો.',
      googleNoSession: 'Google લૉગ ઇનથી સક્રિય સત્ર મળ્યું નથી. કૃપા કરીને ફરી પ્રયાસ કરો.',
      googleAuthRequired: 'તમારા લૉગ ઇન સત્રની પુષ્ટિ થઈ શકી નથી. કૃપા કરીને ફરી લૉગ ઇન કરો.',
      googleServiceUnavailable: 'લૉગ ઇન સેવા અત્યારે ઉપલબ્ધ નથી. કૃપા કરીને પછી ફરી પ્રયાસ કરો.',
      googleProfileLookupError: 'સર્વર પરથી તમારી પ્રોફાઇલ ચકાસી શકાઈ નથી. કનેક્શન તપાસીને ફરી પ્રયાસ કરો.',
      googleFailed: 'Googleથી લૉગ ઇન થઈ શક્યું નથી. કૃપા કરીને ફરી પ્રયાસ કરો.',
      googleRedirectFailed: 'Google લૉગ ઇન શરૂ થયું નથી. કૃપા કરીને ફરી પ્રયાસ કરો.'
    },
    mr: {
      googleSignIn: 'Google सह पुढे जा', googleWorking: 'Google शी जोडत आहे…',
      googleStarting: 'Google साइन-इन उघडत आहे…', googleCheckingProfile: 'तुमचे Shramik Setu प्रोफाइल तपासत आहे…',
      googleCancelled: 'Google साइन-इन रद्द झाले. तुम्ही पुन्हा प्रयत्न करू शकता.',
      googleNoSession: 'Google साइन-इनमधून सक्रिय सत्र मिळाले नाही. कृपया पुन्हा प्रयत्न करा.',
      googleAuthRequired: 'तुमच्या साइन-इन सत्राची पुष्टी झाली नाही. कृपया पुन्हा साइन इन करा.',
      googleServiceUnavailable: 'साइन-इन सेवा सध्या उपलब्ध नाही. कृपया नंतर पुन्हा प्रयत्न करा.',
      googleProfileLookupError: 'सर्व्हरवरून तुमच्या प्रोफाइलची पुष्टी झाली नाही. कनेक्शन तपासून पुन्हा प्रयत्न करा.',
      googleFailed: 'Google द्वारे साइन इन करता आले नाही. कृपया पुन्हा प्रयत्न करा.',
      googleRedirectFailed: 'Google साइन-इन सुरू झाले नाही. कृपया पुन्हा प्रयत्न करा.'
    }
  };

  Object.assign(translations.hi, {
    requiredSkills: 'आवश्यक कौशल', skillSelectPlaceholder: 'कौशल चुनें…', skillAdd: 'जोड़ें', skillSelectedHeading: 'चुने गए कौशल', skillNoSelection: 'कोई कौशल नहीं चुना गया', skillRemove: 'हटाएँ', skillLoading: 'कौशल लोड हो रहे हैं…', skillEmpty: 'अभी कोई कौशल उपलब्ध नहीं है।', skillLoadError: 'कौशल लोड नहीं हो सके। कनेक्शन जाँचकर फिर प्रयास करें।', skillRetry: 'फिर प्रयास करें', skillOtherCategory: 'अन्य कौशल', skillRequiredWorker: 'कृपया कम से कम एक कौशल चुनें', skillRequiredJob: 'कृपया कम से कम एक आवश्यक कौशल चुनें'
  });
  Object.assign(translations.mr, {
    requiredSkills: 'आवश्यक कौशल्ये', skillSelectPlaceholder: 'कौशल्य निवडा…', skillAdd: 'जोडा', skillSelectedHeading: 'निवडलेली कौशल्ये', skillNoSelection: 'कोणतेही कौशल्य निवडलेले नाही', skillRemove: 'काढा', skillLoading: 'कौशल्ये लोड होत आहेत…', skillEmpty: 'सध्या कोणतेही कौशल्य उपलब्ध नाही.', skillLoadError: 'कौशल्ये लोड झाली नाहीत. कनेक्शन तपासून पुन्हा प्रयत्न करा.', skillRetry: 'पुन्हा प्रयत्न करा', skillOtherCategory: 'इतर कौशल्ये', skillRequiredWorker: 'कृपया किमान एक कौशल्य निवडा', skillRequiredJob: 'कृपया किमान एक आवश्यक कौशल्य निवडा'
  });
  Object.assign(translations.gu, {
    requiredSkills: 'જરૂરી કૌશલ્યો', skillSelectPlaceholder: 'કૌશલ્ય પસંદ કરો…', skillAdd: 'ઉમેરો', skillSelectedHeading: 'પસંદ કરેલાં કૌશલ્યો', skillNoSelection: 'કોઈ કૌશલ્ય પસંદ કરેલ નથી', skillRemove: 'દૂર કરો', skillLoading: 'કૌશલ્યો લોડ થઈ રહ્યાં છે…', skillEmpty: 'હાલમાં કોઈ કૌશલ્ય ઉપલબ્ધ નથી.', skillLoadError: 'કૌશલ્યો લોડ થઈ શક્યાં નથી. કનેક્શન તપાસીને ફરી પ્રયાસ કરો.', skillRetry: 'ફરી પ્રયાસ કરો', skillOtherCategory: 'અન્ય કૌશલ્યો', skillRequiredWorker: 'કૃપા કરીને ઓછામાં ઓછું એક કૌશલ્ય પસંદ કરો', skillRequiredJob: 'કૃપા કરીને ઓછામાં ઓછું એક જરૂરી કૌશલ્ય પસંદ કરો'
  });

  const employerPageTranslations = {
    en: {
      employerRegistrationStrip:'Patron registration · Job posting API',employerPageBadge:'Patron Job Posting',employerHeadlineWorkers:'Hire Skilled Pros',employerHeadlineNearby:'Near You Fast',employerIntro:'Register a patron profile, post a job, and review applications returned by the backend.',employerStatWorkers:'Pros',employerStatProfile:'Profile registration',employerStatJobs:'Jobs',employerStatPosting:'Posting and listing',employerStatApplicants:'Applicants',employerStatReview:'Application review',employerStatCapabilities:'Current capabilities',workerRecommendationsTitle:'Pro Recommendations',workerRecommendationsText:'The backend provides pro recommendations for a job. Applicants are listed separately.',workerProfilesTitle:'Pro Profiles',workerProfilesText:'Pro details are returned by the profile endpoint when available. Identity verification is not supported.',hyperlocalResultsTitle:'Hyperlocal Results',hyperlocalResultsText:'Pros matched by proximity — reducing commute time for everyone and improving reliability',applicantStatusTitle:'Applicant Status',applicantStatusText:'Accept or reject an application using the backend status update endpoint.',jobStatusQuote:'Jobs are created with open status. Daily wage is sent using the backend budget field; unsupported form details are included in the description.',apiCapabilities:'API capabilities',currentBackend:'Current backend',postJobHeading:'Post a Job',postJobIntro:'Enter job details to create an open listing through the backend API.',quickForm:'Quick Form',formCompletion:'Form Completion',jobGenericError:'Something went wrong. Please try again.',jobTitleLabel:'Job Title',jobTitlePlaceholder:'e.g. Experienced Electrician Needed',jobTitleRequired:'Please enter a job title',jobDescriptionLabel:'Job Description',jobDescriptionPlaceholder:'Describe the job role, duties, timings, and any special requirements...',jobDescriptionHint:'Be specific about the work, timings, and expectations to attract the right pros',jobDescriptionRequired:'Please add a job description',jobLocationLabel:'Job Location',jobLocationPlaceholder:'Enter site address, city or area',jobLocationHint:'The API accepts coordinates only. Allow location access while at the work site; the typed address is retained in the job description.',jobLocationRequired:'Please enter the job location',dailyWageLabel:'Daily Wage (₹)',wagePlaceholder:'500',perWorkerPerDay:'Per pro, per day',wageRequired:'Please enter a valid wage',workersNeededLabel:'Pros Needed',workersNeededPlaceholder:'e.g. 3',workersNeededHint:'Number of pros required',workersNeededRequired:'Please enter how many pros you need',urgencyLabel:'Urgency Level',urgencyLow:'Low',urgencyLowHint:'Within a week',urgencyMedium:'Medium',urgencyMediumHint:'Within 2–3 days',urgencyHigh:'High',urgencyHighHint:'ASAP / Today',urgencyRequired:'Please select an urgency level',yourDetails:'YOUR DETAILS',yourFullName:'Your Full Name',fullNamePlaceholder:'Enter your full name',fullNameRequired:'Please enter your full name',contactNumber:'Contact Number',phonePlaceholder:'e.g. 9876543210',phoneRequired:'Please enter a valid phone number',businessName:'Patron or business name',businessNamePlaceholder:'Enter your business name',businessNameRequired:'Please enter your patron or business name',employerDescriptionLabel:'Patron description',employerDescriptionPlaceholder:'Briefly describe your business',employerDescriptionRequired:'Please enter a patron description',jobStatusLabel:'Job Status',optional:'Optional',jobStatusValue:'Job status',jobStatusHint:'The backend currently creates every job with open status.',authSessionHint:'Your authenticated Supabase session is used for protected profile and job requests.',termsConfirmation:'I confirm the job details are accurate and the wage offered is fair and legal. The current backend does not provide a separate terms page.',postJobNow:'Post Job Now',postingJob:'Posting job…',jobPostedSuccess:'Job Posted Successfully! 🎉',jobCreatedConfirmation:'The API reported that your job was created.',jobIdLabel:'Job ID',openMyPostedJobs:'Open My Posted Jobs',viewAppliedWorkers:'View Pros Who Applied',checkPublicJobListings:'Check public job listings',postAnotherJob:'Post Another Job',footerCopyright:'© 2026 Shramik Setu · Digital India',backHomepage:'Back to Homepage',jobRequiredFieldsMessage:'Please fill in all required fields before submitting.',jobAcceptTerms:'Please accept the Terms of Service to continue.',jobRequestFailedStatus:'Request failed ({{status}}).',jobUnexpectedError:'Something went wrong. Please try again.',jobIdUnavailable:'Job ID not available. Please try posting the job again.',jobLocationPermissionError:'Location permission is required. Allow location access and try again.',jobLocationDetectionError:'Could not detect your location. Check location access and try again.',jobLocationUnavailable:'Location is unavailable. Enable location services and try again.'
    },
    hi: {
      employerRegistrationStrip:'नियोजक पंजीकरण · नौकरी पोस्टिंग API',employerPageBadge:'नौकरी पोस्ट करें',employerHeadlineWorkers:'कुशल साथी रखें',employerHeadlineNearby:'अपने पास, जल्दी',employerIntro:'नियोजक प्रोफ़ाइल बनाएँ, नौकरी पोस्ट करें और आवेदन देखें।',employerStatWorkers:'साथी',employerStatProfile:'प्रोफ़ाइल पंजीकरण',employerStatJobs:'नौकरियाँ',employerStatPosting:'पोस्ट और सूची',employerStatApplicants:'आवेदक',employerStatReview:'आवेदन समीक्षा',employerStatCapabilities:'वर्तमान सुविधाएँ',workerRecommendationsTitle:'साथी सुझाव',workerRecommendationsText:'बैकएंड नौकरी के लिए साथी सुझाता है। आवेदक अलग सूची में दिखते हैं।',workerProfilesTitle:'साथी प्रोफ़ाइल',workerProfilesText:'उपलब्ध होने पर प्रोफ़ाइल API साथी का विवरण देती है। पहचान सत्यापन उपलब्ध नहीं है।',hyperlocalResultsTitle:'आस-पास के परिणाम',hyperlocalResultsText:'नज़दीकी साथियों से यात्रा समय घटता है और काम की विश्वसनीयता बढ़ती है।',applicantStatusTitle:'आवेदक की स्थिति',applicantStatusText:'बैकएंड स्थिति सुविधा से आवेदन स्वीकार या अस्वीकार करें।',jobStatusQuote:'नौकरियाँ खुली स्थिति में बनती हैं। दैनिक वेतन बजट फ़ील्ड में भेजा जाता है; अन्य विवरण विवरण में जुड़ते हैं।',apiCapabilities:'API सुविधाएँ',currentBackend:'वर्तमान बैकएंड',postJobHeading:'नौकरी पोस्ट करें',postJobIntro:'बैकएंड पर खुली नौकरी सूची बनाने के लिए विवरण भरें।',quickForm:'त्वरित फ़ॉर्म',formCompletion:'फ़ॉर्म पूरा हुआ',jobGenericError:'कुछ गड़बड़ हुई। फिर प्रयास करें।',jobTitleLabel:'नौकरी का शीर्षक',jobTitlePlaceholder:'जैसे: अनुभवी इलेक्ट्रीशियन चाहिए',jobTitleRequired:'नौकरी का शीर्षक दर्ज करें',jobDescriptionLabel:'नौकरी का विवरण',jobDescriptionPlaceholder:'काम, ज़िम्मेदारियाँ, समय और विशेष आवश्यकताएँ बताएँ…',jobDescriptionHint:'उचित साथी पाने के लिए काम, समय और अपेक्षाएँ स्पष्ट लिखें।',jobDescriptionRequired:'नौकरी का विवरण लिखें',jobLocationLabel:'काम का स्थान',jobLocationPlaceholder:'पता, शहर या क्षेत्र दर्ज करें',jobLocationHint:'API केवल निर्देशांक लेता है। काम की जगह पर स्थान अनुमति दें; लिखा पता नौकरी के विवरण में रहेगा।',jobLocationRequired:'काम का स्थान दर्ज करें',dailyWageLabel:'दैनिक वेतन (₹)',wagePlaceholder:'500',perWorkerPerDay:'प्रति साथी, प्रतिदिन',wageRequired:'मान्य वेतन दर्ज करें',workersNeededLabel:'साथियों की संख्या',workersNeededPlaceholder:'जैसे: 3',workersNeededHint:'आवश्यक साथियों की संख्या',workersNeededRequired:'साथियों की संख्या दर्ज करें',urgencyLabel:'तत्कालता',urgencyLow:'कम',urgencyLowHint:'एक सप्ताह के भीतर',urgencyMedium:'मध्यम',urgencyMediumHint:'2–3 दिनों में',urgencyHigh:'अधिक',urgencyHighHint:'जल्द से जल्द / आज',urgencyRequired:'तत्कालता चुनें',yourDetails:'आपका विवरण',yourFullName:'पूरा नाम',fullNamePlaceholder:'अपना पूरा नाम दर्ज करें',fullNameRequired:'अपना पूरा नाम दर्ज करें',contactNumber:'संपर्क नंबर',phonePlaceholder:'जैसे: 9876543210',phoneRequired:'मान्य फ़ोन नंबर दर्ज करें',businessName:'नियोजक या व्यवसाय का नाम',businessNamePlaceholder:'व्यवसाय का नाम दर्ज करें',businessNameRequired:'नियोजक या व्यवसाय का नाम दर्ज करें',employerDescriptionLabel:'नियोजक का विवरण',employerDescriptionPlaceholder:'अपने व्यवसाय के बारे में संक्षेप में बताएँ',employerDescriptionRequired:'नियोजक का विवरण दर्ज करें',jobStatusLabel:'नौकरी की स्थिति',optional:'वैकल्पिक',jobStatusValue:'नौकरी की स्थिति',jobStatusHint:'बैकएंड अभी हर नौकरी को खुली स्थिति में बनाता है।',authSessionHint:'सुरक्षित प्रोफ़ाइल और नौकरी अनुरोधों के लिए आपका प्रमाणित Supabase सत्र उपयोग होता है।',termsConfirmation:'मैं पुष्टि करता/करती हूँ कि नौकरी का विवरण सही है और वेतन उचित व कानूनी है। बैकएंड पर अलग शर्तें पृष्ठ उपलब्ध नहीं है।',postJobNow:'नौकरी पोस्ट करें',postingJob:'नौकरी पोस्ट हो रही है…',jobPostedSuccess:'नौकरी सफलतापूर्वक पोस्ट हुई! 🎉',jobCreatedConfirmation:'API ने नौकरी बनने की पुष्टि की।',jobIdLabel:'नौकरी ID',openMyPostedJobs:'मेरी पोस्ट की गई नौकरियाँ खोलें',viewAppliedWorkers:'आवेदन करने वाले साथी देखें',checkPublicJobListings:'सार्वजनिक नौकरी सूची देखें',postAnotherJob:'एक और नौकरी पोस्ट करें',footerCopyright:'© 2026 Shramik Setu · डिजिटल इंडिया',backHomepage:'मुखपृष्ठ पर वापस जाएँ',jobRequiredFieldsMessage:'सबमिट करने से पहले सभी आवश्यक फ़ील्ड भरें।',jobAcceptTerms:'आगे बढ़ने के लिए सेवा की शर्तें स्वीकार करें।',jobRequestFailedStatus:'अनुरोध विफल ({{status}})।',jobUnexpectedError:'कुछ गड़बड़ हुई। फिर प्रयास करें।',jobIdUnavailable:'नौकरी ID उपलब्ध नहीं है। फिर से पोस्ट करने का प्रयास करें।',jobLocationPermissionError:'स्थान की अनुमति आवश्यक है। अनुमति देकर फिर प्रयास करें।',jobLocationDetectionError:'आपका स्थान नहीं मिल सका। स्थान अनुमति जाँचकर फिर प्रयास करें।',jobLocationUnavailable:'स्थान उपलब्ध नहीं है। स्थान सेवा चालू करके फिर प्रयास करें।'
    },
    mr: {
      employerRegistrationStrip:'नियोजक नोंदणी · नोकरी पोस्टिंग API',employerPageBadge:'नोकरी पोस्ट करा',employerHeadlineWorkers:'कुशल साथी नेमा',employerHeadlineNearby:'तुमच्या जवळ, लवकर',employerIntro:'नियोजक प्रोफाइल नोंदवा, नोकरी पोस्ट करा आणि अर्ज तपासा.',employerStatWorkers:'साथी',employerStatProfile:'प्रोफाइल नोंदणी',employerStatJobs:'नोकऱ्या',employerStatPosting:'पोस्टिंग आणि यादी',employerStatApplicants:'अर्जदार',employerStatReview:'अर्ज तपासणी',employerStatCapabilities:'सध्याच्या सुविधा',workerRecommendationsTitle:'साथी शिफारसी',workerRecommendationsText:'बॅकएंड नोकरीसाठी साथी सुचवतो. अर्जदार स्वतंत्रपणे दाखवले जातात.',workerProfilesTitle:'साथी प्रोफाइल',workerProfilesText:'उपलब्ध असल्यास प्रोफाइल API साथीाची माहिती देते. ओळख पडताळणी उपलब्ध नाही.',hyperlocalResultsTitle:'जवळचे परिणाम',hyperlocalResultsText:'जवळचे साथी प्रवासाचा वेळ कमी करतात आणि विश्वासार्हता वाढवतात.',applicantStatusTitle:'अर्जदाराची स्थिती',applicantStatusText:'बॅकएंड स्थिती सुविधेद्वारे अर्ज स्वीकारा किंवा नाकारा.',jobStatusQuote:'नोकऱ्या खुल्या स्थितीत तयार होतात. दैनिक वेतन बजेट क्षेत्रात पाठवले जाते; इतर तपशील वर्णनात समाविष्ट होतात.',apiCapabilities:'API सुविधा',currentBackend:'सध्याचे बॅकएंड',postJobHeading:'नोकरी पोस्ट करा',postJobIntro:'बॅकएंडवर खुली नोकरी तयार करण्यासाठी तपशील भरा.',quickForm:'झटपट फॉर्म',formCompletion:'फॉर्म पूर्णता',jobGenericError:'काहीतरी चुकले. पुन्हा प्रयत्न करा.',jobTitleLabel:'नोकरीचे शीर्षक',jobTitlePlaceholder:'उदा. अनुभवी इलेक्ट्रिशियन हवा',jobTitleRequired:'नोकरीचे शीर्षक लिहा',jobDescriptionLabel:'नोकरीचे वर्णन',jobDescriptionPlaceholder:'काम, जबाबदाऱ्या, वेळ आणि विशेष गरजा लिहा…',jobDescriptionHint:'योग्य साथी मिळवण्यासाठी काम, वेळ आणि अपेक्षा स्पष्ट लिहा.',jobDescriptionRequired:'नोकरीचे वर्णन लिहा',jobLocationLabel:'कामाचे ठिकाण',jobLocationPlaceholder:'पत्ता, शहर किंवा परिसर लिहा',jobLocationHint:'API फक्त निर्देशांक स्वीकारते. कामाच्या ठिकाणी स्थान परवानगी द्या; लिहिलेला पत्ता वर्णनात राहील.',jobLocationRequired:'कामाचे ठिकाण लिहा',dailyWageLabel:'दैनिक वेतन (₹)',wagePlaceholder:'500',perWorkerPerDay:'प्रति साथी, प्रतिदिन',wageRequired:'वैध वेतन लिहा',workersNeededLabel:'आवश्यक साथी',workersNeededPlaceholder:'उदा. 3',workersNeededHint:'आवश्यक साथीांची संख्या',workersNeededRequired:'साथीांची संख्या लिहा',urgencyLabel:'तातडीची पातळी',urgencyLow:'कमी',urgencyLowHint:'एका आठवड्यात',urgencyMedium:'मध्यम',urgencyMediumHint:'2–3 दिवसांत',urgencyHigh:'जास्त',urgencyHighHint:'लवकरात लवकर / आज',urgencyRequired:'तातडीची पातळी निवडा',yourDetails:'तुमचा तपशील',yourFullName:'तुमचे पूर्ण नाव',fullNamePlaceholder:'तुमचे पूर्ण नाव लिहा',fullNameRequired:'तुमचे पूर्ण नाव लिहा',contactNumber:'संपर्क क्रमांक',phonePlaceholder:'उदा. 9876543210',phoneRequired:'वैध फोन क्रमांक लिहा',businessName:'नियोजक किंवा व्यवसायाचे नाव',businessNamePlaceholder:'व्यवसायाचे नाव लिहा',businessNameRequired:'नियोजक किंवा व्यवसायाचे नाव लिहा',employerDescriptionLabel:'नियोक्त्याचे वर्णन',employerDescriptionPlaceholder:'तुमच्या व्यवसायाबद्दल थोडक्यात लिहा',employerDescriptionRequired:'नियोक्त्याचे वर्णन लिहा',jobStatusLabel:'नोकरीची स्थिती',optional:'पर्यायी',jobStatusValue:'नोकरीची स्थिती',jobStatusHint:'बॅकएंड सध्या प्रत्येक नोकरी खुल्या स्थितीत तयार करते.',authSessionHint:'सुरक्षित प्रोफाइल आणि नोकरी विनंत्यांसाठी तुमचे प्रमाणित Supabase सत्र वापरले जाते.',termsConfirmation:'नोकरीचा तपशील अचूक असून वेतन योग्य आणि कायदेशीर आहे याची मी पुष्टी करतो/करते. बॅकएंडवर स्वतंत्र अटींचे पृष्ठ नाही.',postJobNow:'नोकरी पोस्ट करा',postingJob:'नोकरी पोस्ट होत आहे…',jobPostedSuccess:'नोकरी यशस्वीपणे पोस्ट झाली! 🎉',jobCreatedConfirmation:'API ने नोकरी तयार झाल्याची पुष्टी केली.',jobIdLabel:'नोकरी ID',openMyPostedJobs:'माझ्या पोस्ट केलेल्या नोकऱ्या उघडा',viewAppliedWorkers:'अर्ज केलेले साथी पहा',checkPublicJobListings:'सार्वजनिक नोकरी यादी पहा',postAnotherJob:'आणखी नोकरी पोस्ट करा',footerCopyright:'© 2026 Shramik Setu · डिजिटल इंडिया',backHomepage:'मुख्यपृष्ठावर परत जा',jobRequiredFieldsMessage:'सबमिट करण्यापूर्वी सर्व आवश्यक क्षेत्रे भरा.',jobAcceptTerms:'पुढे जाण्यासाठी सेवा अटी स्वीकारा.',jobRequestFailedStatus:'विनंती अयशस्वी ({{status}}).',jobUnexpectedError:'काहीतरी चुकले. पुन्हा प्रयत्न करा.',jobIdUnavailable:'नोकरी ID उपलब्ध नाही. पुन्हा पोस्ट करण्याचा प्रयत्न करा.',jobLocationPermissionError:'स्थान परवानगी आवश्यक आहे. परवानगी देऊन पुन्हा प्रयत्न करा.',jobLocationDetectionError:'तुमचे स्थान मिळू शकले नाही. स्थान परवानगी तपासून पुन्हा प्रयत्न करा.',jobLocationUnavailable:'स्थान उपलब्ध नाही. स्थान सेवा सुरू करून पुन्हा प्रयत्न करा.'
    },
    gu: {
      employerRegistrationStrip:'નિયોજક નોંધણી · નોકરી પોસ્ટિંગ API',employerPageBadge:'નોકરી પોસ્ટ કરો',employerHeadlineWorkers:'કુશળ સાથીઓ રાખો',employerHeadlineNearby:'તમારી નજીક, ઝડપથી',employerIntro:'નિયોજક પ્રોફાઇલ નોંધો, નોકરી પોસ્ટ કરો અને અરજીઓ જુઓ.',employerStatWorkers:'સાથીઓ',employerStatProfile:'પ્રોફાઇલ નોંધણી',employerStatJobs:'નોકરીઓ',employerStatPosting:'પોસ્ટિંગ અને યાદી',employerStatApplicants:'અરજદારો',employerStatReview:'અરજી સમીક્ષા',employerStatCapabilities:'હાલની સુવિધાઓ',workerRecommendationsTitle:'સાથી ભલામણો',workerRecommendationsText:'બેકએન્ડ નોકરી માટે સાથીઓ સૂચવે છે. અરજદારો અલગથી સૂચિબદ્ધ થાય છે.',workerProfilesTitle:'સાથી પ્રોફાઇલ',workerProfilesText:'ઉપલબ્ધ હોય ત્યારે પ્રોફાઇલ API સાથીની વિગતો આપે છે. ઓળખની ચકાસણી ઉપલબ્ધ નથી.',hyperlocalResultsTitle:'નજીકના પરિણામો',hyperlocalResultsText:'નજીકના સાથીઓ મુસાફરીનો સમય ઘટાડે છે અને વિશ્વસનીયતા વધારે છે.',applicantStatusTitle:'અરજદારની સ્થિતિ',applicantStatusText:'બેકએન્ડ સ્થિતિ સુવિધાથી અરજી સ્વીકારો અથવા નકારો.',jobStatusQuote:'નોકરીઓ ખુલ્લી સ્થિતિમાં બને છે. દૈનિક વેતન બજેટ ક્ષેત્રમાં મોકલાય છે; અન્ય વિગતો વર્ણનમાં ઉમેરાય છે.',apiCapabilities:'API સુવિધાઓ',currentBackend:'હાલનું બેકએન્ડ',postJobHeading:'નોકરી પોસ્ટ કરો',postJobIntro:'બેકએન્ડ પર ખુલ્લી નોકરી બનાવવા વિગતો દાખલ કરો.',quickForm:'ઝડપી ફોર્મ',formCompletion:'ફોર્મ પૂર્ણતા',jobGenericError:'કંઈક ખોટું થયું. ફરી પ્રયાસ કરો.',jobTitleLabel:'નોકરીનું શીર્ષક',jobTitlePlaceholder:'દા.ત. અનુભવી ઇલેક્ટ્રિશિયન જોઈએ',jobTitleRequired:'નોકરીનું શીર્ષક દાખલ કરો',jobDescriptionLabel:'નોકરીનું વર્ણન',jobDescriptionPlaceholder:'કામ, જવાબદારીઓ, સમય અને ખાસ જરૂરિયાતો જણાવો…',jobDescriptionHint:'યોગ્ય સાથીઓ મેળવવા કામ, સમય અને અપેક્ષાઓ સ્પષ્ટ લખો.',jobDescriptionRequired:'નોકરીનું વર્ણન ઉમેરો',jobLocationLabel:'કામનું સ્થળ',jobLocationPlaceholder:'સરનામું, શહેર કે વિસ્તાર દાખલ કરો',jobLocationHint:'API માત્ર કોઓર્ડિનેટ સ્વીકારે છે. કામના સ્થળે સ્થાનની મંજૂરી આપો; લખેલું સરનામું વર્ણનમાં રહેશે.',jobLocationRequired:'કામનું સ્થળ દાખલ કરો',dailyWageLabel:'દૈનિક વેતન (₹)',wagePlaceholder:'500',perWorkerPerDay:'દરેક સાથી માટે, દરરોજ',wageRequired:'માન્ય વેતન દાખલ કરો',workersNeededLabel:'જરૂરી સાથીઓ',workersNeededPlaceholder:'દા.ત. 3',workersNeededHint:'જરૂરી સાથીઓની સંખ્યા',workersNeededRequired:'સાથીઓની સંખ્યા દાખલ કરો',urgencyLabel:'તાકીદનું સ્તર',urgencyLow:'ઓછું',urgencyLowHint:'એક અઠવાડિયામાં',urgencyMedium:'મધ્યમ',urgencyMediumHint:'2–3 દિવસમાં',urgencyHigh:'વધુ',urgencyHighHint:'શક્ય તેટલું વહેલું / આજે',urgencyRequired:'તાકીદનું સ્તર પસંદ કરો',yourDetails:'તમારી વિગતો',yourFullName:'તમારું પૂરું નામ',fullNamePlaceholder:'તમારું પૂરું નામ દાખલ કરો',fullNameRequired:'તમારું પૂરું નામ દાખલ કરો',contactNumber:'સંપર્ક નંબર',phonePlaceholder:'દા.ત. 9876543210',phoneRequired:'માન્ય ફોન નંબર દાખલ કરો',businessName:'નિયોજક અથવા વ્યવસાયનું નામ',businessNamePlaceholder:'વ્યવસાયનું નામ દાખલ કરો',businessNameRequired:'નિયોજક અથવા વ્યવસાયનું નામ દાખલ કરો',employerDescriptionLabel:'નિયોજકનું વર્ણન',employerDescriptionPlaceholder:'તમારા વ્યવસાય વિશે ટૂંકમાં જણાવો',employerDescriptionRequired:'નિયોજકનું વર્ણન દાખલ કરો',jobStatusLabel:'નોકરીની સ્થિતિ',optional:'વૈકલ્પિક',jobStatusValue:'નોકરીની સ્થિતિ',jobStatusHint:'બેકએન્ડ હાલમાં દરેક નોકરી ખુલ્લી સ્થિતિમાં બનાવે છે.',authSessionHint:'સુરક્ષિત પ્રોફાઇલ અને નોકરી વિનંતીઓ માટે તમારું પ્રમાણિત Supabase સત્ર વપરાય છે.',termsConfirmation:'નોકરીની વિગતો સાચી છે અને વેતન યોગ્ય તથા કાયદેસર છે તેની હું પુષ્ટિ કરું છું. બેકએન્ડ અલગ શરતોનું પાનું આપતું નથી.',postJobNow:'નોકરી પોસ્ટ કરો',postingJob:'નોકરી પોસ્ટ થઈ રહી છે…',jobPostedSuccess:'નોકરી સફળતાપૂર્વક પોસ્ટ થઈ! 🎉',jobCreatedConfirmation:'API એ નોકરી બન્યાની જાણ કરી.',jobIdLabel:'નોકરી ID',openMyPostedJobs:'મારી પોસ્ટ કરેલી નોકરીઓ ખોલો',viewAppliedWorkers:'અરજી કરનારા સાથીઓ જુઓ',checkPublicJobListings:'જાહેર નોકરી યાદી જુઓ',postAnotherJob:'બીજી નોકરી પોસ્ટ કરો',footerCopyright:'© 2026 Shramik Setu · ડિજિટલ ઇન્ડિયા',backHomepage:'મુખ્ય પૃષ્ઠ પર પાછા જાઓ',jobRequiredFieldsMessage:'સબમિટ કરતાં પહેલાં બધી જરૂરી વિગતો ભરો.',jobAcceptTerms:'આગળ વધવા સેવા શરતો સ્વીકારો.',jobRequestFailedStatus:'વિનંતી નિષ્ફળ ({{status}}).',jobUnexpectedError:'કંઈક ખોટું થયું. ફરી પ્રયાસ કરો.',jobIdUnavailable:'નોકરી ID ઉપલબ્ધ નથી. ફરી પોસ્ટ કરવાનો પ્રયાસ કરો.',jobLocationPermissionError:'સ્થાનની મંજૂરી જરૂરી છે. મંજૂરી આપીને ફરી પ્રયાસ કરો.',jobLocationDetectionError:'તમારું સ્થાન મળી શક્યું નથી. સ્થાનની મંજૂરી તપાસીને ફરી પ્રયાસ કરો.',jobLocationUnavailable:'સ્થાન ઉપલબ્ધ નથી. સ્થાન સેવા ચાલુ કરીને ફરી પ્રયાસ કરો.'
    }
  };
  Object.keys(employerPageTranslations).forEach((language) => Object.assign(translations[language], employerPageTranslations[language]));
  Object.assign(translations.en, { jobOutcomeUnknown: 'The job may already have been posted. Check My Posted Jobs before trying again.' });
  Object.assign(translations.hi, { jobOutcomeUnknown: 'नौकरी पोस्ट हो चुकी हो सकती है। दोबारा प्रयास करने से पहले मेरी पोस्ट की गई नौकरियाँ देखें।' });
  Object.assign(translations.mr, { jobOutcomeUnknown: 'नोकरी पोस्ट झाली असण्याची शक्यता आहे. पुन्हा प्रयत्न करण्यापूर्वी माझ्या पोस्ट केलेल्या नोकऱ्या तपासा.' });
  Object.assign(translations.gu, { jobOutcomeUnknown: 'નોકરી કદાચ પોસ્ટ થઈ ગઈ છે. ફરી પ્રયાસ કરતાં પહેલાં મારી પોસ્ટ કરેલી નોકરીઓ તપાસો.' });

  Object.keys(emailAuthTranslations).forEach((language) => Object.assign(translations[language], emailAuthTranslations[language]));
  Object.keys(googleAuthTranslations).forEach((language) => Object.assign(translations[language], googleAuthTranslations[language]));

  const uiPhraseTranslations = {
    'Shramik Setu — Find Work. Hire Fast.': ['Shramik Setu — Find Work. Hire Fast.', 'Shramik Setu — काम खोजें, जल्दी काम पाएँ।', 'Shramik Setu — काम शोधा, लवकर काम मिळवा.', 'Shramik Setu — કામ શોધો, ઝડપથી કામ મેળવો.'],
    'Pro Registration — Shramik Setu': ['Pro Registration — Shramik Setu', 'साथी पंजीकरण — Shramik Setu', 'साथी नोंदणी — Shramik Setu', 'સાથી નોંધણી — Shramik Setu'],
    'Post a Job — Shramik Setu': ['Post a Job — Shramik Setu', 'नौकरी पोस्ट करें — Shramik Setu', 'नोकरी पोस्ट करा — Shramik Setu', 'નોકરી પોસ્ટ કરો — Shramik Setu'],
    'Sign in — Shramik Setu': ['Sign in — Shramik Setu', 'लॉग इन — Shramik Setu', 'लॉग इन — Shramik Setu', 'લૉગ ઇન — Shramik Setu'],
    'Open Jobs — Shramik Setu': ['Open Jobs — Shramik Setu', 'खुली नौकरियाँ — Shramik Setu', 'खुल्या नोकऱ्या — Shramik Setu', 'ખુલ્લી નોકરીઓ — Shramik Setu'],
    'Jobs Near You — Shramik Setu': ['Jobs Near You — Shramik Setu', 'आपके आस-पास नौकरियाँ — Shramik Setu', 'तुमच्या जवळच्या नोकऱ्या — Shramik Setu', 'તમારી નજીકની નોકરીઓ — Shramik Setu'],
    'Job Applicants — Shramik Setu': ['Job Applicants — Shramik Setu', 'नौकरी के आवेदक — Shramik Setu', 'नोकरीचे अर्जदार — Shramik Setu', 'નોકરીના અરજદારો — Shramik Setu'],
    'My Posted Jobs — Shramik Setu': ['My Posted Jobs — Shramik Setu', 'मेरी पोस्ट की गई नौकरियाँ — Shramik Setu', 'माझ्या पोस्ट केलेल्या नोकऱ्या — Shramik Setu', 'મારી પોસ્ટ કરેલી નોકરીઓ — Shramik Setu'],
    'Find Work or Hire Skilled Pros Near You': ['Find Work or Hire Skilled Pros Near You', 'अपने आस-पास काम खोजें या कुशल साथी नियुक्त करें', 'तुमच्या जवळ काम शोधा किंवा कुशल साथींना कामावर ठेवा', 'તમારી નજીક કામ શોધો અથવા કુશળ સાથીઓને કામે રાખો'],
    'Back to Home': ['Back to Home', 'मुखपृष्ठ पर जाएँ', 'मुख्यपृष्ठावर जा', 'મુખ્ય પૃષ્ઠ પર જાઓ'],
    'Back to Homepage': ['Back to Homepage', 'मुखपृष्ठ पर वापस जाएँ', 'मुखपृष्ठावर परत जा', 'મુખ્ય પૃષ્ઠ પર પાછા જાઓ'],
    'Personalised Job Recommendations · Based on Your Skills & Location · Free & Verified': ['Personalised Job Recommendations · Based on Your Skills & Location · Free & Verified', 'आपके कौशल और स्थान के आधार पर नौकरी सुझाव · निःशुल्क', 'तुमची कौशल्ये आणि ठिकाणानुसार नोकरीच्या शिफारसी · विनामूल्य', 'તમારી કુશળતા અને સ્થાન મુજબ નોકરીની ભલામણો · મફત'],
    'Recommended for You': ['Recommended for You', 'आपके लिए सुझाए गए', 'तुमच्यासाठी शिफारस केलेले', 'તમારા માટે સૂચવેલ'],
    'Jobs': ['Jobs', 'नौकरियाँ', 'नोकऱ्या', 'નોકરીઓ'],
    'Near You': ['Near You', 'आपके आस-पास', 'तुमच्या जवळ', 'તમારી નજીક'],
    'Matched to your skills and location — updated in real time.': ['Matched to your skills and location — updated in real time.', 'आपके कौशल और स्थान के अनुसार — तुरंत अपडेट होते हैं।', 'तुमच्या कौशल्ये आणि ठिकाणानुसार — तत्काळ अद्ययावत.', 'તમારી કુશળતા અને સ્થાન મુજબ — તત્કાળ અપડેટ થાય છે.'],
    'Refresh Jobs': ['Refresh Jobs', 'नौकरियाँ रीफ़्रेश करें', 'नोकऱ्या पुन्हा लोड करा', 'નોકરીઓ ફરી લોડ કરો'],
    'Application history': ['Application history', 'आवेदन इतिहास', 'अर्जांचा इतिहास', 'અરજીનો ઇતિહાસ'],
    'Statuses are shown as returned by the API. The Pro ID in this browser is a workflow reference, not secure sign-in.': ['Statuses are shown as returned by the API. The Pro ID in this browser is a workflow reference, not secure sign-in.', 'स्थिति API के अनुसार दिखाई जाती है। इस ब्राउज़र में Pro ID केवल प्रक्रिया के लिए है, सुरक्षित लॉग इन नहीं।', 'स्थिती API कडून मिळाल्याप्रमाणे दाखवली जाते. या ब्राउझरमधील Pro ID हा केवळ प्रक्रियेचा संदर्भ आहे, सुरक्षित लॉग इन नाही.', 'સ્થિતિ API મુજબ બતાવવામાં આવે છે. આ બ્રાઉઝરમાં Pro ID ફક્ત પ્રક્રિયા માટે છે, સુરક્ષિત લૉગ ઇન નથી.'],
    'Loading application history…': ['Loading application history…', 'आवेदन इतिहास लोड हो रहा है…', 'अर्जांचा इतिहास लोड होत आहे…', 'અરજીનો ઇતિહાસ લોડ થઈ રહ્યો છે…'],
    'Open Jobs': ['Open Jobs', 'खुली नौकरियाँ', 'खुल्या नोकऱ्या', 'ખુલ્લી નોકરીઓ'],
    'Register': ['Register', 'पंजीकरण करें', 'नोंदणी करा', 'નોંધણી કરો'],
    'Recommended jobs': ['Recommended jobs', 'सुझाई गई नौकरियाँ', 'शिफारस केलेल्या नोकऱ्या', 'સૂચવેલી નોકરીઓ'],
    'Post a job': ['Post a job', 'नौकरी पोस्ट करें', 'नोकरी पोस्ट करा', 'નોકરી પોસ્ટ કરો'],
    'Sign in': ['Sign in', 'लॉग इन करें', 'लॉग इन करा', 'લૉગ ઇન કરો'],
    'Open jobs': ['Open jobs', 'खुली नौकरियाँ', 'खुल्या नोकऱ्या', 'ખુલ્લી નોકરીઓ'],
    'Current openings returned by Shramik Setu.': ['Current openings returned by Shramik Setu.', 'Shramik Setu पर उपलब्ध मौजूदा नौकरियाँ।', 'Shramik Setu वरील सध्याच्या नोकऱ्या.', 'Shramik Setu પરની હાલની નોકરીઓ.'],
    'Loading jobs…': ['Loading jobs…', 'नौकरियाँ लोड हो रही हैं…', 'नोकऱ्या लोड होत आहेत…', 'નોકરીઓ લોડ થઈ રહી છે…'],
    'Try again': ['Try again', 'फिर प्रयास करें', 'पुन्हा प्रयत्न करा', 'ફરી પ્રયાસ કરો'],
    'Location coordinates were not provided.': ['Location coordinates were not provided.', 'स्थान के निर्देशांक उपलब्ध नहीं हैं।', 'ठिकाणाचे निर्देशांक दिलेले नाहीत.', 'સ્થાનના કોઓર્ડિનેટ આપવામાં આવ્યા નથી.'],
    'Open location map': ['Open location map', 'स्थान का नक्शा खोलें', 'ठिकाणाचा नकाशा उघडा', 'સ્થાનનો નકશો ખોલો'],
    'There are no open jobs right now.': ['There are no open jobs right now.', 'अभी कोई खुली नौकरी नहीं है।', 'सध्या कोणतीही खुली नोकरी नाही.', 'હાલમાં કોઈ ખુલ્લી નોકરી નથી.'],
    'Application submitted': ['Application submitted', 'आवेदन भेज दिया गया', 'अर्ज पाठवला', 'અરજી મોકલાઈ'],
    'Application status unknown': ['Application status unknown', 'आवेदन की स्थिति अज्ञात है', 'अर्जाची स्थिती अज्ञात आहे', 'અરજીની સ્થિતિ અજ્ઞાત છે'],
    'Not open for applications': ['Not open for applications', 'आवेदन स्वीकार नहीं हो रहे', 'अर्ज स्वीकारले जात नाहीत', 'અરજીઓ સ્વીકારાતી નથી'],
    'Job unavailable': ['Job unavailable', 'नौकरी उपलब्ध नहीं', 'नोकरी उपलब्ध नाही', 'નોકરી ઉપલબ્ધ નથી'],
    'Apply for this job': ['Apply for this job', 'इस नौकरी के लिए आवेदन करें', 'या नोकरीसाठी अर्ज करा', 'આ નોકરી માટે અરજી કરો'],
    'Budget not provided': ['Budget not provided', 'वेतन नहीं दिया गया', 'वेतन दिलेले नाही', 'વેતન આપેલું નથી'],
    'Status:': ['Status:', 'स्थिति:', 'स्थिती:', 'સ્થિતિ:'],
    'View job details and location': ['View job details and location', 'नौकरी और स्थान का विवरण देखें', 'नोकरी आणि ठिकाणाचा तपशील पहा', 'નોકરી અને સ્થાનની વિગતો જુઓ'],
    'Coordinates:': ['Coordinates:', 'निर्देशांक:', 'निर्देशांक:', 'કોઓર્ડિનેટ:'],
    'The server did not confirm whether this application was saved. Check your application status before trying again.': ['The server did not confirm whether this application was saved. Check your application status before trying again.', 'सर्वर यह पुष्टि नहीं कर सका कि आवेदन सहेजा गया है। फिर प्रयास करने से पहले आवेदन की स्थिति जाँचें।', 'अर्ज जतन झाला की नाही याची सर्व्हरने पुष्टी केली नाही. पुन्हा प्रयत्न करण्यापूर्वी अर्जाची स्थिती तपासा.', 'અરજી સાચવાઈ છે કે નહીં તેની સર્વરે પુષ્ટિ કરી નથી. ફરી પ્રયાસ કરતાં પહેલાં અરજીની સ્થિતિ તપાસો.'],
    'Sign in to apply.': ['Sign in to apply.', 'आवेदन करने के लिए लॉग इन करें।', 'अर्ज करण्यासाठी लॉग इन करा.', 'અરજી કરવા લૉગ ઇન કરો.'],
    'Go to sign in': ['Go to sign in', 'लॉग इन पर जाएँ', 'लॉग इनकडे जा', 'લૉગ ઇન પર જાઓ'],
    'then return here and try again.': ['then return here and try again.', 'फिर यहाँ लौटकर दोबारा प्रयास करें।', 'नंतर येथे परत येऊन पुन्हा प्रयत्न करा.', 'પછી અહીં પાછા આવી ફરી પ્રયાસ કરો.'],
    'Checking sign-in…': ['Checking sign-in…', 'लॉग इन जाँचा जा रहा है…', 'लॉग इन तपासत आहे…', 'લૉગ ઇન તપાસાઈ રહ્યું છે…'],
    'Submitting…': ['Submitting…', 'भेजा जा रहा है…', 'पाठवत आहे…', 'મોકલાઈ રહ્યું છે…'],
    'Application needs checking': ['Application needs checking', 'आवेदन की जाँच आवश्यक है', 'अर्ज तपासणे आवश्यक आहे', 'અરજીની તપાસ જરૂરી છે'],
    'The server confirmed your application.': ['The server confirmed your application.', 'सर्वर ने आपके आवेदन की पुष्टि की।', 'सर्व्हरने तुमच्या अर्जाची पुष्टी केली.', 'સર્વરે તમારી અરજીની પુષ્ટિ કરી.'],
    'Application status unknown': ['Application status unknown', 'आवेदन की स्थिति अज्ञात है', 'अर्जाची स्थिती अज्ञात आहे', 'અરજીની સ્થિતિ અજ્ઞાત છે'],
    'My Posted Jobs': ['My Posted Jobs', 'मेरी पोस्ट की गई नौकरियाँ', 'माझ्या पोस्ट केलेल्या नोकऱ्या', 'મારી પોસ્ટ કરેલી નોકરીઓ'],
    'Job Applicants': ['Job Applicants', 'नौकरी के आवेदक', 'नोकरीचे अर्जदार', 'નોકરીના અરજદારો'],
    'Pros Who Applied': ['Pros Who Applied', 'आवेदन करने वाले साथी', 'अर्ज केलेले साथी', 'અરજી કરનારા સાથીઓ'],
    'Review each applicant and hire or reject them for this job.': ['Review each applicant and hire or reject them for this job.', 'हर आवेदक की समीक्षा करें और इस नौकरी के लिए चुनें या अस्वीकार करें।', 'प्रत्येक अर्जदाराची तपासणी करून या नोकरीसाठी निवडा किंवा नकार द्या.', 'દરેક અરજદારની સમીક્ષા કરીને આ નોકરી માટે પસંદ કરો અથવા નકારો.'],
    'Refresh': ['Refresh', 'रीफ़्रेश करें', 'पुन्हा लोड करा', 'ફરી લોડ કરો'],
    'Look Up Applicants by Job ID': ['Look Up Applicants by Job ID', 'Job ID से आवेदक खोजें', 'Job ID द्वारे अर्जदार शोधा', 'Job ID દ્વારા અરજદારો શોધો'],
    'Paste a Job ID to see who applied — no URL param needed': ['Paste a Job ID to see who applied — no URL param needed', 'आवेदक देखने के लिए Job ID डालें — URL बदलने की ज़रूरत नहीं', 'अर्जदार पाहण्यासाठी Job ID टाका — URL बदलण्याची गरज नाही', 'અરજદારો જોવા Job ID દાખલ કરો — URL બદલવાની જરૂર નથી'],
    'View Applicants →': ['View Applicants →', 'आवेदक देखें →', 'अर्जदार पहा →', 'અરજદારો જુઓ →'],
    'Recommended pros': ['Recommended pros', 'सुझाए गए साथी', 'शिफारस केलेले साथी', 'સૂચવેલા સાથીઓ'],
    'Pros ranked for this job using the backend match results.': ['Pros ranked for this job using the backend match results.', 'बैकएंड के मिलान परिणामों के आधार पर इस नौकरी के साथी।', 'बॅकएंडच्या जुळणी निकालांनुसार या नोकरीसाठी साथी.', 'બેકએન્ડના મેળવણી પરિણામો મુજબ આ નોકરી માટેના સાથીઓ.'],
    'Recommendations load when a job is selected.': ['Recommendations load when a job is selected.', 'नौकरी चुनने पर सुझाव लोड होंगे।', 'नोकरी निवडल्यानंतर शिफारसी लोड होतील.', 'નોકરી પસંદ કર્યા પછી ભલામણો લોડ થશે.'],
    'My Posted Jobs': ['My Posted Jobs', 'मेरी पोस्ट की गई नौकरियाँ', 'माझ्या पोस्ट केलेल्या नोकऱ्या', 'મારી પોસ્ટ કરેલી નોકરીઓ'],
    'Jobs are loaded from your signed-in patron account. Refresh this page to load the latest status.': ['Jobs are loaded from your signed-in patron account. Refresh this page to load the latest status.', 'नौकरियाँ आपके नियोजक खाते से लोड होती हैं। नवीनतम स्थिति देखने के लिए पृष्ठ रीफ़्रेश करें।', 'नोकऱ्या तुमच्या नियोजक खात्यातून लोड होतात. नवीनतम स्थितीसाठी पृष्ठ पुन्हा लोड करा.', 'નોકરીઓ તમારા નિયોજક ખાતામાંથી લોડ થાય છે. નવીનતમ સ્થિતિ માટે પાનું ફરી લોડ કરો.'],
    'Loading your jobs…': ['Loading your jobs…', 'आपकी नौकरियाँ लोड हो रही हैं…', 'तुमच्या नोकऱ्या लोड होत आहेत…', 'તમારી નોકરીઓ લોડ થઈ રહી છે…'],
    'Post your first job': ['Post your first job', 'अपनी पहली नौकरी पोस्ट करें', 'तुमची पहिली नोकरी पोस्ट करा', 'તમારી પહેલી નોકરી પોસ્ટ કરો'],
    'Budget:': ['Budget:', 'वेतन:', 'वेतन:', 'વેતન:'],
    'Location:': ['Location:', 'स्थान:', 'ठिकाण:', 'સ્થાન:'],
    'Posted:': ['Posted:', 'पोस्ट किया:', 'पोस्ट केले:', 'પોસ્ટ કરી:'],
    'Location unavailable': ['Location unavailable', 'स्थान उपलब्ध नहीं', 'ठिकाण उपलब्ध नाही', 'સ્થાન ઉપલબ્ધ નથી'],
    'Posting date unavailable': ['Posting date unavailable', 'पोस्ट करने की तारीख उपलब्ध नहीं', 'पोस्टची तारीख उपलब्ध नाही', 'પોસ્ટની તારીખ ઉપલબ્ધ નથી'],
    'Recommended Pros': ['Recommended Pros', 'सुझाए गए साथी', 'शिफारस केलेले साथी', 'સૂચવેલા સાથીઓ'],
    'Applied Pros': ['Applied Pros', 'आवेदन करने वाले साथी', 'अर्ज केलेले साथी', 'અરજી કરનારા સાથીઓ'],
    'No applications yet': ['No applications yet', 'अभी कोई आवेदन नहीं आया', 'अद्याप अर्ज आलेले नाहीत', 'હજુ સુધી કોઈ અરજીઓ નથી'],
    'No pros have applied to this job yet.': ['No pros have applied to this job yet.', 'इस नौकरी के लिए अभी किसी साथी ने आवेदन नहीं किया है।', 'या नोकरीसाठी अद्याप कोणत्याही साथीने अर्ज केलेला नाही.', 'આ નોકરી માટે હજી કોઈ સાથીે અરજી કરી નથી.'],
    'Budget not provided': ['Budget not provided', 'वेतन नहीं दिया गया', 'वेतन दिलेले नाही', 'વેતન આપેલું નથી'],
    'OPEN': ['OPEN', 'खुली', 'खुली', 'ખુલ્લી'],
    'Closed': ['Closed', 'बंद', 'बंद', 'બંધ'],
    'Pending': ['Pending', 'लंबित', 'प्रलंबित', 'બાકી'],
    'Hired': ['Hired', 'नियुक्त', 'नियुक्त', 'રાખ્યા'],
    'Rejected': ['Rejected', 'अस्वीकृत', 'नाकारले', 'નકારાયું'],
    'Find Work': ['Find Work', 'काम खोजें', 'काम शोधा', 'કામ શોધો'],
    'Hire Skilled Pros': ['Hire Skilled Pros', 'कुशल साथी नियुक्त करें', 'कुशल साथींना कामावर ठेवा', 'કુશળ સાથીઓને કામે રાખો'],
    'Workflow preview': ['Workflow preview', 'प्रक्रिया का पूर्वावलोकन', 'प्रक्रियेचे पूर्वावलोकन', 'પ્રક્રિયાનું પૂર્વાવલોકન'],
    'Illustrative interface': ['Illustrative interface', 'उदाहरण के लिए', 'प्रातिनिधिक नमुना', 'માત્ર ઉદાહરણ'],
    'Pro & Job Examples': ['Pro & Job Examples', 'साथी और नौकरी के उदाहरण', 'साथी व नोकरीची उदाहरणे', 'સાથી અને નોકરીનાં ઉદાહરણો'],
    'SAMPLE DATA': ['SAMPLE DATA', 'नमूना डेटा', 'नमुना माहिती', 'નમૂનાનો ડેટા'],
    'Example Match Time': ['Example Match Time', 'मिलान समय का उदाहरण', 'जुळणी वेळेचे उदाहरण', 'મેળવણી સમયનું ઉદાહરણ'],
    'Why Shramik Setu': ['Why Shramik Setu', 'Shramik Setu क्यों', 'Shramik Setu का?', 'Shramik Setu શા માટે'],
    'Built for Real India.': ['Built for Real India.', 'भारत के लोगों के लिए बनाया गया।', 'भारताच्या लोकांसाठी बनवलेले.', 'ભારતના લોકો માટે બનાવેલું.'],
    'Designed with Trust.': ['Designed with Trust.', 'भरोसे को ध्यान में रखकर बनाया गया।', 'विश्वास जपून तयार केलेले.', 'વિશ્વાસને ધ્યાનમાં રાખીને બનાવેલું.'],
    'Accessible, fast, and transparent — a dignified, reliable connection for Patrons and Pros.': ['Accessible, fast, and transparent — a dignified, reliable connection for Patrons and Pros.', 'सरल, तेज़ और पारदर्शी — नियोजक और साथी के लिए सम्मानजनक और भरोसेमंद जुड़ाव।', 'सुलभ, जलद आणि पारदर्शक — नियोजक आणि साथींसाठी सन्मानजनक व विश्वासार्ह जोडणी.', 'સરળ, ઝડપી અને પારદર્શક — નિયોજક અને સાથી માટે ગૌરવપૂર્ણ અને વિશ્વસનીય જોડાણ.'],
    'Location-Based Matching': ['Location-Based Matching', 'स्थान के आधार पर मिलान', 'ठिकाणानुसार जुळणी', 'સ્થાન આધારિત મેળવણી'],
    'Pro recommendations use the coordinates stored with profiles and jobs.': ['Pro recommendations use the coordinates stored with profiles and jobs.', 'साथी सुझाव प्रोफ़ाइल और नौकरी में सहेजे स्थान निर्देशांकों का उपयोग करते हैं।', 'साथींच्या शिफारसी प्रोफाइल आणि नोकरीतील जतन केलेल्या निर्देशांकांवर आधारित असतात.', 'સાથીની ભલામણો પ્રોફાઇલ અને નોકરીમાં સંગ્રહિત કોઓર્ડિનેટનો ઉપયોગ કરે છે.'],
    'Patrons and Pros Profiles': ['Patrons and Pros Profiles', 'साथी और नियोजक प्रोफ़ाइल', 'साथी व नियोजक प्रोफाइल', 'સાથી અને નિયોજકની પ્રોફાઇલ'],
    'Create a profile with contact details and skills. Identity verification is not currently provided by the backend.': ['Create a profile with contact details and skills. Identity verification is not currently provided by the backend.', 'संपर्क विवरण और कौशल के साथ प्रोफ़ाइल बनाएँ। बैकएंड अभी पहचान सत्यापन नहीं देता।', 'संपर्क तपशील आणि कौशल्यांसह प्रोफाइल तयार करा. बॅकएंड सध्या ओळख पडताळणी देत नाही.', 'સંપર્ક વિગતો અને કુશળતા સાથે પ્રોફાઇલ બનાવો. બેકએન્ડ હાલમાં ઓળખની ચકાસણી આપતું નથી.'],
    'Job Recommendations': ['Job Recommendations', 'नौकरी सुझाव', 'नोकरीच्या शिफारसी', 'નોકરીની ભલામણો'],
    'Pros can browse open jobs and load skill-based recommendations returned by the backend.': ['Pros can browse open jobs and load skill-based recommendations returned by the backend.', 'साथी खुली नौकरियाँ देख सकते हैं और बैकएंड से कौशल-आधारित सुझाव पा सकते हैं।', 'साथी खुल्या नोकऱ्या पाहू शकतात आणि बॅकएंडकडून कौशल्याधारित शिफारसी मिळवू शकतात.', 'સાથીઓ ખુલ્લી નોકરીઓ જોઈ શકે છે અને બેકએન્ડ તરફથી કુશળતા આધારિત ભલામણો મેળવી શકે છે.'],
    'Application Review': ['Application Review', 'आवेदन समीक्षा', 'अर्ज तपासणी', 'અરજી સમીક્ષા'],
    'Patrons can review applications and send status updates through the available backend endpoints.': ['Patrons can review applications and send status updates through the available backend endpoints.', 'नियोजक आवेदनों की समीक्षा कर उपलब्ध बैकएंड सुविधाओं से स्थिति अपडेट कर सकते हैं।', 'नियोजक अर्ज तपासून उपलब्ध बॅकएंड सुविधांद्वारे स्थिती बदलू शकतात.', 'નિયોજકો અરજીઓ તપાસી ઉપલબ્ધ બેકએન્ડ સુવિધાઓથી સ્થિતિ અપડેટ કરી શકે છે.'],
    'Simple Process': ['Simple Process', 'आसान प्रक्रिया', 'सोपी प्रक्रिया', 'સરળ પ્રક્રિયા'],
    'Three easy steps to transform your work life.': ['Three easy steps to transform your work life.', 'काम की दिशा बदलने के तीन आसान कदम।', 'कामाच्या आयुष्यात बदल घडवणारी तीन सोपी पावले.', 'તમારા કામના જીવનમાં પરિવર્તન લાવતાં ત્રણ સરળ પગલાં.'],
    'Create Your Profile': ['Create Your Profile', 'अपनी प्रोफ़ाइल बनाएँ', 'तुमचे प्रोफाइल तयार करा', 'તમારી પ્રોફાઇલ બનાવો'],
    'Create a pro or patron profile with the details requested on the form.': ['Create a pro or patron profile with the details requested on the form.', 'फ़ॉर्म में माँगे गए विवरण से नियोजक या साथी की प्रोफ़ाइल बनाएँ।', 'फॉर्ममध्ये मागितलेल्या तपशीलांसह नियोजक किंवा साथीचे प्रोफाइल तयार करा.', 'ફોર્મમાં માંગેલી વિગતો સાથે નિયોજક અથવા સાથીની પ્રોફાઇલ બનાવો.'],
    'Get Matched': ['Get Matched', 'उपयुक्त मिलान पाएँ', 'योग्य जुळणी मिळवा', 'યોગ્ય મેળવણી મેળવો'],
    'The recommendation service ranks jobs using skills, location, and backend matching signals.': ['The recommendation service ranks jobs using skills, location, and backend matching signals.', 'सुझाव सेवा कौशल, स्थान और मिलान संकेतों के आधार पर नौकरियों को क्रम देती है।', 'शिफारस सेवा कौशल्ये, ठिकाण आणि जुळणी संकेतांनुसार नोकऱ्यांचा क्रम ठरवते.', 'ભલામણ સેવા કુશળતા, સ્થાન અને મેળવણી સંકેતોના આધારે નોકરીઓ ગોઠવે છે.'],
    'Connect & Work': ['Connect & Work', 'जुड़ें और काम करें', 'जोडा आणि काम करा', 'જોડાઓ અને કામ કરો'],
    'Review available listings and recommendations, then contact each other directly using details you choose to share.': ['Review available listings and recommendations, then contact each other directly using details you choose to share.', 'सूचियाँ और सुझाव देखें, फिर साझा की गई संपर्क जानकारी से सीधे बात करें।', 'याद्या आणि शिफारसी पाहा आणि तुम्ही शेअर केलेल्या तपशीलांद्वारे थेट संपर्क साधा.', 'યાદીઓ અને ભલામણો જોઈ, તમે શેર કરેલી વિગતો દ્વારા સીધો સંપર્ક કરો.'],
    'Ready to Transform Your Work Life?': ['Ready to Transform Your Work Life?', 'क्या आप काम की नई शुरुआत के लिए तैयार हैं?', 'कामाच्या आयुष्यात नवी सुरुवात करण्यास तयार आहात?', 'કામના જીવનમાં નવી શરૂઆત કરવા તૈયાર છો?'],
    'Find work or connect with local patrons': ['Find work or connect with local patrons', 'काम खोजें या स्थानीय नियोजकों से जुड़ें', 'काम शोधा किंवा स्थानिक नियोजकांशी जोडा', 'કામ શોધો અથવા સ્થાનિક નિયોજકો સાથે જોડાઓ'],
    'Browse Jobs': ['Browse Jobs', 'नौकरियाँ देखें', 'नोकऱ्या पहा', 'નોકરીઓ જુઓ'],
    'Create Profile': ['Create Profile', 'प्रोफ़ाइल बनाएँ', 'प्रोफाइल तयार करा', 'પ્રોફાઇલ બનાવો'],
    'Recommended Jobs': ['Recommended Jobs', 'सुझाई गई नौकरियाँ', 'शिफारस केलेल्या नोकऱ्या', 'સૂચવેલી નોકરીઓ'],
    'Post Jobs': ['Post Jobs', 'नौकरियाँ पोस्ट करें', 'नोकऱ्या पोस्ट करा', 'નોકરીઓ પોસ્ટ કરો'],
    'Review Applicants': ['Review Applicants', 'आवेदकों की समीक्षा करें', 'अर्जदार तपासा', 'અરજદારોની સમીક્ષા કરો'],
    'About Us': ['About Us', 'हमारे बारे में', 'आमच्याबद्दल', 'અમારા વિશે'],
    'All rights reserved.': ['All rights reserved.', 'सर्वाधिकार सुरक्षित।', 'सर्व हक्क राखीव.', 'સર્વ હકો સુરક્ષિત.']
  };

  Object.assign(uiPhraseTranslations, {
    'Start Finding Jobs Near You': ['Start Finding Jobs Near You', 'अपने आस-पास काम खोजना शुरू करें', 'तुमच्या जवळ काम शोधायला सुरुवात करा', 'તમારી નજીક કામ શોધવાનું શરૂ કરો'],
    'Shramik Setu · My Posted Jobs': ['Shramik Setu · My Posted Jobs', 'Shramik Setu · मेरी पोस्ट की गई नौकरियाँ', 'Shramik Setu · माझ्या पोस्ट केलेल्या नोकऱ्या', 'Shramik Setu · મારી પોસ્ટ કરેલી નોકરીઓ'],
    'Applications': ['Applications', 'आवेदन', 'अर्ज', 'અરજીઓ'],
    'Start Your Journey': ['Start Your Journey', 'अपनी यात्रा शुरू करें', 'तुमचा प्रवास सुरू करा', 'તમારી સફર શરૂ કરો'],
    'Post as Patron': ['Post as Patron', 'नियोजक के रूप में पोस्ट करें', 'नियोजक म्हणून पोस्ट करा', 'નિયોજક તરીકે પોસ્ટ કરો'],
    'Browse Open Jobs': ['Browse Open Jobs', 'खुली नौकरियाँ देखें', 'खुल्या नोकऱ्या पहा', 'ખુલ્લી નોકરીઓ જુઓ'],
    'Patron Dashboard · Review Applicants · Discover Recommended Pros': ['Patron Dashboard · Review Applicants · Discover Recommended Pros', 'नियोजक डैशबोर्ड · आवेदक देखें · सुझाए गए साथी खोजें', 'नियोजक डॅशबोर्ड · अर्जदार तपासा · शिफारस केलेले साथी शोधा', 'નિયોજક ડેશબોર્ડ · અરજદારો તપાસો · સૂચવેલા સાથીઓ શોધો'],
    'Good work starts with a': ['Good work starts with a', 'अच्छे काम की शुरुआत', 'चांगल्या कामाची सुरुवात', 'સારા કામની શરૂઆત'],
    'connection.': ['connection.', 'सही जुड़ाव से होती है।', 'योग्य जोडणीतून होते.', 'યોગ્ય જોડાણથી થાય છે.'],
    'Please enter your phone number': ['Please enter your phone number', 'अपना फ़ोन नंबर दर्ज करें', 'तुमचा फोन नंबर टाका', 'તમારો ફોન નંબર દાખલ કરો'],
    'Please enter your full name': ['Please enter your full name', 'अपना पूरा नाम दर्ज करें', 'तुमचे पूर्ण नाव टाका', 'તમારું પૂરું નામ દાખલ કરો'],
    'Enter experience as a whole number of years (0 or more).': ['Enter experience as a whole number of years (0 or more).', 'अनुभव पूरे वर्षों में दर्ज करें (0 या अधिक)।', 'अनुभव पूर्ण वर्षांत टाका (0 किंवा अधिक).', 'અનુભવ પૂર્ણ વર્ષોમાં દાખલ કરો (0 અથવા વધુ).'],
    'Enter an expected daily wage greater than 0.': ['Enter an expected daily wage greater than 0.', '0 से अधिक अपेक्षित दैनिक वेतन दर्ज करें।', '0 पेक्षा जास्त अपेक्षित दैनिक वेतन टाका.', '0 કરતાં વધુ અપેક્ષિત દૈનિક વેતન દાખલ કરો.'],
    'Please enter a work category': ['Please enter a work category', 'काम का प्रकार दर्ज करें', 'कामाचा प्रकार टाका', 'કામનો પ્રકાર દાખલ કરો'],
    'Enter your city or area. The backend stores device coordinates, not this address text; allow location access to share your current coordinates.': ['Enter your city or area. The backend stores device coordinates, not this address text; allow location access to share your current coordinates.', 'अपना शहर या क्षेत्र दर्ज करें। बैकएंड डिवाइस के निर्देशांक सहेजता है, यह पता नहीं; अपना वर्तमान स्थान साझा करने के लिए स्थान अनुमति दें।', 'तुमचे शहर किंवा परिसर टाका. बॅकएंड डिव्हाइसचे निर्देशांक जतन करते, हा पत्ता नाही; सध्याचे स्थान शेअर करण्यासाठी परवानगी द्या.', 'તમારું શહેર કે વિસ્તાર દાખલ કરો. બેકએન્ડ ઉપકરણના કોઓર્ડિનેટ સંગ્રહે છે, આ સરનામું નહીં; હાલનું સ્થાન શેર કરવા મંજૂરી આપો.'],
    'Please enter your location': ['Please enter your location', 'अपना स्थान दर्ज करें', 'तुमचे ठिकाण टाका', 'તમારું સ્થાન દાખલ કરો'],
    'Availability': ['Availability', 'उपलब्धता', 'उपलब्धता', 'ઉપલબ્ધતા'],
    'The current backend marks every new pro profile as available.': ['The current backend marks every new pro profile as available.', 'मौजूदा बैकएंड हर नई साथी प्रोफ़ाइल को उपलब्ध मानता है।', 'सध्याचे बॅकएंड प्रत्येक नवीन साथी प्रोफाइल उपलब्ध म्हणून नोंदवते.', 'હાલનું બેકએન્ડ દરેક નવી સાથી પ્રોફાઇલને ઉપલબ્ધ તરીકે નોંધે છે.'],
    'Your profile ID is returned by the API. Your authenticated Supabase session is used for protected requests.': ['Your profile ID is returned by the API. Your authenticated Supabase session is used for protected requests.', 'API आपकी प्रोफ़ाइल ID लौटाती है। सुरक्षित अनुरोधों के लिए आपका प्रमाणित Supabase सत्र उपयोग होता है।', 'API तुमचा प्रोफाइल ID परत करते. सुरक्षित विनंत्यांसाठी प्रमाणित Supabase सत्र वापरले जाते.', 'API તમારી પ્રોફાઇલ ID આપે છે. સુરક્ષિત વિનંતીઓ માટે તમારું પ્રમાણિત Supabase સત્ર વપરાય છે.'],
    'I confirm that the information provided is accurate. The current backend does not provide a separate terms or privacy page.': ['I confirm that the information provided is accurate. The current backend does not provide a separate terms or privacy page.', 'मैं पुष्टि करता/करती हूँ कि दी गई जानकारी सही है। मौजूदा बैकएंड पर अलग शर्तें या गोपनीयता पृष्ठ उपलब्ध नहीं है।', 'दिलेली माहिती अचूक असल्याची मी पुष्टी करतो/करते. सध्याच्या बॅकएंडवर स्वतंत्र अटी किंवा गोपनीयता पृष्ठ नाही.', 'આપેલી માહિતી સાચી છે તેની હું પુષ્ટિ કરું છું. હાલના બેકએન્ડ પર અલગ શરતો કે ગોપનીયતા પાનું નથી.'],
    'Welcome to Shramik Setu,': ['Welcome to Shramik Setu,', 'Shramik Setu में आपका स्वागत है,', 'Shramik Setu मध्ये तुमचे स्वागत आहे,', 'Shramik Setuમાં તમારું સ્વાગત છે,'],
    'Step 1 of 1': ['Step 1 of 1', 'चरण 1 में 1', 'पायरी 1 पैकी 1', 'પગલું 1 માંથી 1'],
    'Rajesh — Carpenter': ['Rajesh — Carpenter', 'राजेश — बढ़ई', 'राजेश — सुतार', 'રાજેશ — સુથાર'],
    'Priya — Painter': ['Priya — Painter', 'प्रिया — रंगसाथी', 'प्रिया — रंगारी', 'પ્રિયા — રંગસાથી'],
    'Applications': ['Applications', 'आवेदन', 'अर्ज', 'અરજીઓ'],
    'NEW': ['NEW', 'नया', 'नवीन', 'નવું'],
    'Job Recommendations': ['Job Recommendations', 'नौकरी सुझाव', 'नोकरीच्या शिफारसी', 'નોકરીની ભલામણો'],
    'Browse open jobs and view recommendations returned by the matching API.': ['Browse open jobs and view recommendations returned by the matching API.', 'खुली नौकरियाँ देखें और मिलान API से मिले सुझाव पाएँ।', 'खुल्या नोकऱ्या पाहा आणि जुळणी API कडून मिळालेल्या शिफारसी पहा.', 'ખુલ્લી નોકરીઓ જુઓ અને મેળવણી API તરફથી મળેલી ભલામણો જુઓ.'],
    'Profile Details': ['Profile Details', 'प्रोफ़ाइल विवरण', 'प्रोफाइल तपशील', 'પ્રોફાઇલ વિગતો'],
    'Your name, phone, skills, wage, and coordinates are submitted to the backend.': ['Your name, phone, skills, wage, and coordinates are submitted to the backend.', 'आपका नाम, फ़ोन, कौशल, वेतन और स्थान निर्देशांक बैकएंड को भेजे जाते हैं।', 'तुमचे नाव, फोन, कौशल्ये, वेतन आणि ठिकाणाचे निर्देशांक बॅकएंडला पाठवले जातात.', 'તમારું નામ, ફોન, કુશળતા, વેતન અને સ્થાનના કોઓર્ડિનેટ બેકએન્ડને મોકલાય છે.'],
    'Jobs in Your Area': ['Jobs in Your Area', 'आपके क्षेत्र की नौकरियाँ', 'तुमच्या परिसरातील नोकऱ्या', 'તમારા વિસ્તારમાં નોકરીઓ'],
    'The recommendation service considers saved coordinates; the frontend does not geocode the typed address.': ['The recommendation service considers saved coordinates; the frontend does not geocode the typed address.', 'सुझाव सेवा सहेजे गए निर्देशांकों का उपयोग करती है; फ़ॉर्म में लिखा पता नक्शे के निर्देशांकों में नहीं बदला जाता।', 'शिफारस सेवा जतन केलेले निर्देशांक वापरते; टाइप केलेला पत्ता नकाशाच्या निर्देशांकात बदलला जात नाही.', 'ભલામણ સેવા સંગ્રહિત કોઓર્ડિનેટનો ઉપયોગ કરે છે; લખેલું સરનામું નકશાના કોઓર્ડિનેટમાં બદલાતું નથી.'],
    'The current API supports pro registration and job recommendations. It does not provide identity verification or job notifications.': ['The current API supports pro registration and job recommendations. It does not provide identity verification or job notifications.', 'मौजूदा API साथी पंजीकरण और नौकरी सुझाव देती है। पहचान सत्यापन और नौकरी सूचनाएँ उपलब्ध नहीं हैं।', 'सध्याची API साथी नोंदणी आणि नोकरीच्या शिफारसी देते. ओळख पडताळणी किंवा नोकरीच्या सूचना उपलब्ध नाहीत.', 'હાલનું API સાથી નોંધણી અને નોકરીની ભલામણોને સપોર્ટ કરે છે. ઓળખ ચકાસણી કે નોકરીની સૂચનાઓ આપતું નથી.'],
    'Registration Successful! 🎉': ['Registration Successful! 🎉', 'पंजीकरण सफल हुआ! 🎉', 'नोंदणी यशस्वी! 🎉', 'નોંધણી સફળ! 🎉'],
    'Your profile is now live. Patrons near you can find you.': ['Your profile is now live. Patrons near you can find you.', 'आपकी प्रोफ़ाइल अब उपलब्ध है। आस-पास के नियोजक आपको ढूँढ सकते हैं।', 'तुमचे प्रोफाइल आता उपलब्ध आहे. जवळचे नियोजक तुम्हाला शोधू शकतात.', 'તમારી પ્રોફાઇલ હવે ઉપલબ્ધ છે. નજીકના નિયોજકો તમને શોધી શકે છે.'],
    'Browse Jobs Near Me →': ['Browse Jobs Near Me →', 'आस-पास की नौकरियाँ देखें →', 'जवळच्या नोकऱ्या पहा →', 'નજીકની નોકરીઓ જુઓ →'],
    'Return to Homepage': ['Return to Homepage', 'मुखपृष्ठ पर लौटें', 'मुखपृष्ठावर परत जा', 'મુખ્ય પૃષ્ઠ પર પાછા જાઓ'],
    'Sign in to continue your Shramik Setu journey, whether you’re looking for work or building your team.': ['Sign in to continue your Shramik Setu journey, whether you’re looking for work or building your team.', 'काम खोजने या अपनी टीम बनाने के लिए Shramik Setu में लॉग इन करें।', 'काम शोधण्यासाठी किंवा तुमची टीम तयार करण्यासाठी Shramik Setu मध्ये लॉग इन करा.', 'કામ શોધવા અથવા તમારી ટીમ બનાવવા Shramik Setuમાં લૉગ ઇન કરો.'],
    'Connecting pros and local patrons across Bharat': ['Connecting pros and local patrons across Bharat', 'भारत भर के साथियों और स्थानीय नियोजकों को जोड़ना', 'भारतभरातील साथी व स्थानिक नियोजकांना जोडणे', 'ભારતભરના સાથીઓ અને સ્થાનિક નિયોજકોને જોડવા'],
    'Current backend capabilities': ['Current backend capabilities', 'मौजूदा बैकएंड सुविधाएँ', 'सध्याच्या बॅकएंड सुविधा', 'હાલની બેકએન્ડ સુવિધાઓ'],
    'Platform integration': ['Platform integration', 'प्लेटफ़ॉर्म एकीकरण', 'प्लॅटफॉर्म एकत्रीकरण', 'પ્લેટફોર્મ સંકલન'],
    'Pro and Patron registration, job posting and listing, job recommendations, applications, and application status updates are available through the connected API.': ['Patrons and Pros can register, post and browse jobs, receive recommendations, submit applications, and update application status through the connected API.', 'जुड़े API के माध्यम से नियोजक और साथी पंजीकरण कर सकते हैं, नौकरियाँ पोस्ट व देख सकते हैं, सुझाव पा सकते हैं, आवेदन कर सकते हैं और आवेदन की स्थिति अपडेट कर सकते हैं।', 'जोडलेल्या API द्वारे नियोजक आणि साथी नोंदणी करू शकतात, नोकऱ्या पोस्ट व पाहू शकतात, शिफारसी मिळवू शकतात, अर्ज करू शकतात आणि अर्जाची स्थिती अद्ययावत करू शकतात.', 'જોડાયેલા API દ્વારા નિયોજક અને સાથી નોંધણી કરી શકે છે, નોકરીઓ પોસ્ટ અને જોઈ શકે છે, ભલામણો મેળવી શકે છે, અરજીઓ કરી શકે છે અને અરજીની સ્થિતિ અપડેટ કરી શકે છે.'],
    'Availability depends on the backend service': ['Availability depends on the backend service', 'उपलब्धता बैकएंड सेवा पर निर्भर है', 'उपलब्धता बॅकएंड सेवेवर अवलंबून आहे', 'ઉપલબ્ધતા બેકએન્ડ સેવા પર આધારિત છે'],
    '2.3 km · ₹600/day': ['2.3 km · ₹600/day', '2.3 किमी · ₹600/दिन', '2.3 किमी · ₹600/दिवस', '2.3 કિમી · ₹600/દિવસ'],
    '3.1 km · ₹700/day': ['3.1 km · ₹700/day', '3.1 किमी · ₹700/दिन', '3.1 किमी · ₹700/दिवस', '3.1 કિમી · ₹700/દિવસ'],
    '4.9 (120 jobs)': ['4.9 (120 jobs)', '4.9 (120 नौकरियाँ)', '4.9 (120 नोकऱ्या)', '4.9 (120 નોકરીઓ)'],
    '5.0 (85 jobs)': ['5.0 (85 jobs)', '5.0 (85 नौकरियाँ)', '5.0 (85 नोकऱ्या)', '5.0 (85 નોકરીઓ)'],
    '12 mins': ['12 mins', '12 मिनट', '12 मिनिटे', '12 મિનિટ'],
    'Pro ID missing!': ['Pro ID missing!', 'Pro ID नहीं मिली!', 'Pro ID सापडली नाही!', 'Pro ID મળી નથી!'],
    'Applied!': ['Applied!', 'आवेदन भेजा!', 'अर्ज केला!', 'અરજી થઈ!'],
    'Could not reach the server. Check your connection and try again.': ['Could not reach the server. Check your connection and try again.', 'सर्वर से संपर्क नहीं हो सका। कनेक्शन जाँचकर फिर प्रयास करें।', 'सर्व्हरशी संपर्क झाला नाही. कनेक्शन तपासून पुन्हा प्रयत्न करा.', 'સર્વર સાથે જોડાઈ શક્યા નથી. કનેક્શન તપાસીને ફરી પ્રયાસ કરો.'],
    'The request timed out. The server may be starting; please try again.': ['The request timed out. The server may be starting; please try again.', 'अनुरोध का समय समाप्त हुआ। सर्वर शुरू हो रहा हो सकता है; फिर प्रयास करें।', 'विनंतीची वेळ संपली. सर्व्हर सुरू होत असू शकतो; पुन्हा प्रयत्न करा.', 'વિનંતીનો સમય પૂરો થયો. સર્વર શરૂ થતું હોઈ શકે છે; ફરી પ્રયાસ કરો.'],
    'The server returned an unexpected jobs response.': ['The server returned an unexpected jobs response.', 'सर्वर से नौकरियों का अप्रत्याशित उत्तर मिला।', 'सर्व्हरकडून नोकऱ्यांचा अनपेक्षित प्रतिसाद मिळाला.', 'સર્વર તરફથી નોકરીઓનો અનપેક્ષિત જવાબ મળ્યો.'],
    'Could not load open jobs. Please try again.': ['Could not load open jobs. Please try again.', 'खुली नौकरियाँ लोड नहीं हो सकीं। फिर प्रयास करें।', 'खुल्या नोकऱ्या लोड करता आल्या नाहीत. पुन्हा प्रयत्न करा.', 'ખુલ્લી નોકરીઓ લોડ થઈ શકી નથી. ફરી પ્રયાસ કરો.'],
    'The server returned an unexpected applications response.': ['The server returned an unexpected applications response.', 'सर्वर से आवेदनों का अप्रत्याशित उत्तर मिला।', 'सर्व्हरकडून अर्जांचा अनपेक्षित प्रतिसाद मिळाला.', 'સર્વર તરફથી અરજીઓનો અનપેક્ષિત જવાબ મળ્યો.'],
    'The server returned an unexpected recommendations response.': ['The server returned an unexpected recommendations response.', 'सर्वर से सुझावों का अप्रत्याशित उत्तर मिला।', 'सर्व्हरकडून शिफारसींचा अनपेक्षित प्रतिसाद मिळाला.', 'સર્વર તરફથી ભલામણોનો અનપેક્ષિત જવાબ મળ્યો.'],
    'The server did not confirm this status update.': ['The server did not confirm this status update.', 'सर्वर इस स्थिति अपडेट की पुष्टि नहीं कर सका।', 'सर्व्हर या स्थिती बदलाची पुष्टी करू शकला नाही.', 'સર્વર આ સ્થિતિ અપડેટની પુષ્ટિ કરી શક્યું નથી.'],
    'Could not update this application.': ['Could not update this application.', 'इस आवेदन को अपडेट नहीं किया जा सका।', 'हा अर्ज अद्ययावत करता आला नाही.', 'આ અરજી અપડેટ થઈ શકી નથી.'],
    'Sign in is unavailable on this page. Open the sign-in page and try again.': ['Sign in is unavailable on this page. Open the sign-in page and try again.', 'इस पृष्ठ पर लॉग इन उपलब्ध नहीं है। लॉग इन पृष्ठ खोलकर फिर प्रयास करें।', 'या पृष्ठावर लॉग इन उपलब्ध नाही. लॉग इन पृष्ठ उघडून पुन्हा प्रयत्न करा.', 'આ પાને લૉગ ઇન ઉપલબ્ધ નથી. લૉગ ઇન પાનું ખોલીને ફરી પ્રયાસ કરો.'],
    'Your sign-in may have expired. Sign in again before retrying.': ['Your sign-in may have expired. Sign in again before retrying.', 'आपका लॉग इन समाप्त हो सकता है। फिर प्रयास करने से पहले दोबारा लॉग इन करें।', 'तुमचे लॉग इन सत्र संपले असू शकते. पुन्हा प्रयत्न करण्यापूर्वी लॉग इन करा.', 'તમારું લૉગ ઇન સમાપ્ત થયું હોઈ શકે છે. ફરી પ્રયાસ કરતાં પહેલાં ફરી લૉગ ઇન કરો.'],
    'The recommendation service returned no matches for this pro. There are open jobs in the general feed; they are not being shown as recommendations.': ['The recommendation service returned no matches for this pro. There are open jobs in the general feed; they are not being shown as recommendations.', 'इस साथी के लिए कोई सुझाव नहीं मिला। सामान्य सूची में खुली नौकरियाँ हैं, लेकिन उन्हें सुझाव के रूप में नहीं दिखाया जा रहा।', 'या साथीासाठी शिफारसी मिळाल्या नाहीत. सामान्य यादीत खुल्या नोकऱ्या आहेत; त्या शिफारसी म्हणून दाखवल्या जात नाहीत.', 'આ સાથી માટે ભલામણો મળી નથી. સામાન્ય યાદીમાં ખુલ્લી નોકરીઓ છે, પરંતુ તે ભલામણ તરીકે બતાવવામાં આવતી નથી.'],
    'open': ['open', 'खुली', 'खुली', 'ખુલ્લી'], 'closed': ['closed', 'बंद', 'बंद', 'બંધ'], 'pending': ['pending', 'लंबित', 'प्रलंबित', 'બાકી'], 'hired': ['hired', 'नियुक्त', 'नियुक्त', 'નોકરીએ રાખ્યા'], 'rejected': ['rejected', 'अस्वीकृत', 'नाकारले', 'નકારાયું'], 'OPEN': ['OPEN', 'खुली', 'खुली', 'ખુલ્લી'],
    'Not provided': ['Not provided', 'नहीं दिया गया', 'दिलेले नाही', 'આપેલું નથી'],
    'Finding jobs near you…': ['Finding jobs near you…', 'आपके आस-पास नौकरियाँ खोजी जा रही हैं…', 'तुमच्या जवळच्या नोकऱ्या शोधत आहोत…', 'તમારી નજીકની નોકરીઓ શોધાઈ રહી છે…'],
    'Retry loading history': ['Retry loading history', 'इतिहास फिर से लोड करें', 'इतिहास पुन्हा लोड करा', 'ઇતિહાસ ફરી લોડ કરો'],
    'No Recommended Matches': ['No Recommended Matches', 'कोई उपयुक्त सुझाव नहीं मिला', 'योग्य शिफारस मिळाली नाही', 'યોગ્ય ભલામણ મળી નથી'],
    'No Open Jobs Right Now': ['No Open Jobs Right Now', 'अभी कोई खुली नौकरी नहीं है', 'सध्या कोणतीही खुली नोकरी नाही', 'હાલમાં કોઈ ખુલ્લી નોકરી નથી'],
    'Browse all open jobs': ['Browse all open jobs', 'सभी खुली नौकरियाँ देखें', 'सर्व खुल्या नोकऱ्या पहा', 'બધી ખુલ્લી નોકરીઓ જુઓ'],
    'Sorted by relevance & proximity': ['Sorted by relevance & proximity', 'प्रासंगिकता और दूरी के अनुसार क्रमबद्ध', 'संबंधितता आणि जवळीक यानुसार क्रम', 'સુસંગતતા અને નજીકતા મુજબ ગોઠવેલ'],
    'Location coordinates are available': ['Location coordinates are available', 'स्थान के निर्देशांक उपलब्ध हैं', 'ठिकाणाचे निर्देशांक उपलब्ध आहेत', 'સ્થાનના કોઓર્ડિનેટ ઉપલબ્ધ છે'],
    'Refreshing…': ['Refreshing…', 'रीफ़्रेश हो रहा है…', 'पुन्हा लोड होत आहे…', 'ફરી લોડ થઈ રહ્યું છે…'],
    'Application status is unknown': ['Application status is unknown', 'आवेदन की स्थिति अज्ञात है', 'अर्जाची स्थिती अज्ञात आहे', 'અરજીની સ્થિતિ અજ્ઞાત છે'],
    'Application submitted': ['Application submitted', 'आवेदन भेज दिया गया', 'अर्ज पाठवला', 'અરજી મોકલાઈ'],
    'The application may already exist; this page will not submit it again.': ['The application may already exist; this page will not submit it again.', 'आवेदन पहले से हो सकता है; यह पृष्ठ इसे दोबारा नहीं भेजेगा।', 'अर्ज आधीच असू शकतो; हे पृष्ठ तो पुन्हा पाठवणार नाही.', 'અરજી પહેલેથી હોઈ શકે છે; આ પાનું તેને ફરી મોકલશે નહીં.'],
    'The server did not confirm whether this application was saved. Check your application status before trying again.': ['The server did not confirm whether this application was saved. Check your application status before trying again.', 'सर्वर यह पुष्टि नहीं कर सका कि आवेदन सहेजा गया है। फिर प्रयास करने से पहले आवेदन की स्थिति जाँचें।', 'अर्ज जतन झाला की नाही याची सर्व्हरने पुष्टी केली नाही. पुन्हा प्रयत्न करण्यापूर्वी अर्जाची स्थिती तपासा.', 'અરજી સાચવાઈ છે કે નહીં તેની સર્વરે પુષ્ટિ કરી નથી. ફરી પ્રયાસ કરતાં પહેલાં અરજીની સ્થિતિ તપાસો.'],
    'Please register first — no pro ID found.': ['Please register first — no pro ID found.', 'पहले पंजीकरण करें — Pro ID नहीं मिली।', 'आधी नोंदणी करा — Pro ID सापडली नाही.', 'પહેલાં નોંધણી કરો — Pro ID મળી નથી.'],
    'This job is no longer open for applications. Refresh the list to check current jobs.': ['This job is no longer open for applications. Refresh the list to check current jobs.', 'इस नौकरी के लिए आवेदन बंद हैं। मौजूदा नौकरियाँ देखने के लिए सूची रीफ़्रेश करें।', 'या नोकरीसाठी अर्ज स्वीकारणे बंद आहे. सध्याच्या नोकऱ्या पाहण्यासाठी यादी पुन्हा लोड करा.', 'આ નોકરી માટે અરજીઓ બંધ છે. હાલની નોકરીઓ જોવા યાદી ફરી લોડ કરો.'],
    'Application submitted': ['Application submitted', 'आवेदन भेज दिया गया', 'अर्ज पाठवला', 'અરજી મોકલાઈ'],
    'Application status unknown': ['Application status unknown', 'आवेदन की स्थिति अज्ञात है', 'अर्जाची स्थिती अज्ञात आहे', 'અરજીની સ્થિતિ અજ્ઞાત છે'],
    'History unavailable': ['History unavailable', 'इतिहास उपलब्ध नहीं', 'इतिहास उपलब्ध नाही', 'ઇતિહાસ ઉપલબ્ધ નથી'],
    'Job not open': ['Job not open', 'नौकरी खुली नहीं है', 'नोकरी खुली नाही', 'નોકરી ખુલ્લી નથી'],
    'Status unavailable': ['Status unavailable', 'स्थिति उपलब्ध नहीं', 'स्थिती उपलब्ध नाही', 'સ્થિતિ ઉપલબ્ધ નથી'],
    'job': ['job', 'नौकरी', 'नोकरी', 'નોકરી'],
    'jobs': ['jobs', 'नौकरियाँ', 'नोकऱ्या', 'નોકરીઓ'],
    'Pro & Job Examples': ['Pro & Job Examples', 'साथी और नौकरी के उदाहरण', 'साथी व नोकरीची उदाहरणे', 'સાથી અને નોકરીનાં ઉદાહરણો'],
    'Names and contact details are not included in this response.': ['Names and contact details are not included in this response.', 'इस उत्तर में नाम और संपर्क विवरण शामिल नहीं हैं।', 'या प्रतिसादात नावे आणि संपर्क तपशील दिलेले नाहीत.', 'આ જવાબમાં નામ અને સંપર્ક વિગતો સામેલ નથી.'],
    'Application ID:': ['Application ID:', 'आवेदन ID:', 'अर्ज ID:', 'અરજી ID:'],
    'Pro ID:': ['Pro ID:', 'साथी ID:', 'साथी ID:', 'સાથી ID:'],
    'Job ID:': ['Job ID:', 'नौकरी ID:', 'नोकरी ID:', 'નોકરી ID:'],
    'Applied:': ['Applied:', 'आवेदन किया:', 'अर्ज केला:', 'અરજી કરી:'],
    'Application ID unavailable; cannot update': ['Application ID unavailable; cannot update', 'आवेदन ID उपलब्ध नहीं; अपडेट नहीं कर सकते', 'अर्ज ID उपलब्ध नाही; बदल करता येत नाही', 'અરજી ID ઉપલબ્ધ નથી; અપડેટ કરી શકાતું નથી'],
    'Application status unknown': ['Application status unknown', 'आवेदन की स्थिति अज्ञात है', 'अर्जाची स्थिती अज्ञात आहे', 'અરજીની સ્થિતિ અજ્ઞાત છે'],
    'No additional match details were returned.': ['No additional match details were returned.', 'मिलान का अतिरिक्त विवरण नहीं मिला।', 'जुळणीचा अतिरिक्त तपशील मिळाला नाही.', 'મેળવણીની વધારાની વિગતો મળી નથી.'],
    'Applicant': ['Applicant', 'आवेदक', 'अर्जदार', 'અરજદાર'],
    'Pro registration': ['Pro registration', 'साथी पंजीकरण', 'साथी नोंदणी', 'સાથી નોંધણી'],
    'Skill recommendations': ['Skill recommendations', 'कौशल सुझाव', 'कौशल्य शिफारसी', 'કુશળતા ભલામણો'],
    'Live job listings': ['Live job listings', 'वर्तमान नौकरी सूची', 'सध्याच्या नोकऱ्यांची यादी', 'ચાલુ નોકરીઓની યાદી'],
    'Location aware matching': ['Location aware matching', 'स्थान के आधार पर मिलान', 'ठिकाणानुसार जुळणी', 'સ્થાન આધારિત મેળવણી'],
    'Registration API': ['Registration API', 'पंजीकरण API', 'नोंदणी API', 'નોંધણી API'],
    'Listing API': ['Listing API', 'सूची API', 'यादी API', 'યાદી API'],
    'Recommendation API': ['Recommendation API', 'सुझाव API', 'शिफारस API', 'ભલામણ API'],
    'Applicant review API': ['Applicant review API', 'आवेदन समीक्षा API', 'अर्ज तपासणी API', 'અરજી સમીક્ષા API'],
    'How It': ['How It', 'यह कैसे', 'हे कसे', 'આ કેવી રીતે'],
    'Works': ['Works', 'काम करता है', 'कार्य करते', 'કામ કરે છે'],
    'Stories': ['Stories', 'अनुभव', 'अनुभव', 'અનુભવો'],
    'Integration': ['Integration', 'एकीकरण', 'एकत्रीकरण', 'સંકલન'],
    'Status': ['Status', 'स्थिति', 'स्थिती', 'સ્થિતિ'],
    'Available backend workflows': ['Available backend workflows', 'उपलब्ध बैकएंड कार्यप्रवाह', 'उपलब्ध बॅकएंड कार्यप्रवाह', 'ઉપલબ્ધ બેકએન્ડ કાર્યપ્રવાહ'],
    'For Pros': ['For Pros', 'साथियों के लिए', 'साथींसाठी', 'સાથીઓ માટે'],
    'For Patrons': ['For Patrons', 'नियोजकों के लिए', 'नियोजकांसाठी', 'નિયોજકો માટે'],
    'Company': ['Company', 'कंपनी', 'कंपनी', 'કંપની'],
    'Connecting daily-wage pros with local patrons across India. Dignified work for every hand.': ['Connecting daily-wage pros with local patrons across India. Dignified work for every hand.', 'भारत भर के साथियों और स्थानीय नियोजकों को जोड़ना। हर हाथ को सम्मानजनक काम।', 'भारतभरातील साथी व स्थानिक नियोजकांना जोडणे. प्रत्येक हाताला सन्मानाचे काम.', 'ભારતભરના સાથીઓ અને સ્થાનિક નિયોજકોને જોડીએ. દરેક હાથને ગૌરવપૂર્ણ કામ.'],
    '© 2026 Shramik Setu. All rights reserved. · Digital India': ['© 2026 Shramik Setu. All rights reserved. · Digital India', '© 2026 Shramik Setu. सर्वाधिकार सुरक्षित। · डिजिटल इंडिया', '© 2026 Shramik Setu. सर्व हक्क सुरक्षित. · डिजिटल इंडिया', '© 2026 Shramik Setu. સર્વ હકો સુરક્ષિત. · ડિજિટલ ઇન્ડિયા'],
    'Job ID': ['Job ID', 'नौकरी ID', 'नोकरी ID', 'નોકરી ID'],
    'Job ID:': ['Job ID:', 'नौकरी ID:', 'नोकरी ID:', 'નોકરી ID:'],
    'application': ['application', 'आवेदन', 'अर्ज', 'અરજી'],
    'applications': ['applications', 'आवेदन', 'अर्ज', 'અરજીઓ'],
    'Results found for you': ['Results found for you', 'आपके लिए परिणाम मिले', 'तुमच्यासाठी निकाल मिळाले', 'તમારા માટે પરિણામો મળ્યાં'],
    'Sorted by relevance & proximity': ['Sorted by relevance & proximity', 'प्रासंगिकता और दूरी के अनुसार क्रमबद्ध', 'संबंधितता आणि जवळीक यानुसार क्रम', 'સુસંગતતા અને નજીકતા મુજબ ગોઠવેલ'],
    'Status unavailable': ['Status unavailable', 'स्थिति उपलब्ध नहीं', 'स्थिती उपलब्ध नाही', 'સ્થિતિ ઉપલબ્ધ નથી'],
    'Application needs checking': ['Application needs checking', 'आवेदन की जाँच आवश्यक है', 'अर्ज तपासणे आवश्यक आहे', 'અરજીની તપાસ જરૂરી છે'],
    'The job may already have been posted. Check My Posted Jobs before trying again.': ['The job may already have been posted. Check My Posted Jobs before trying again.', 'नौकरी पोस्ट हो चुकी हो सकती है। फिर प्रयास करने से पहले मेरी पोस्ट की गई नौकरियाँ देखें।', 'नोकरी पोस्ट झाली असण्याची शक्यता आहे. पुन्हा प्रयत्न करण्यापूर्वी माझ्या पोस्ट केलेल्या नोकऱ्या तपासा.', 'નોકરી કદાચ પોસ્ટ થઈ ગઈ છે. ફરી પ્રયાસ કરતાં પહેલાં મારી પોસ્ટ કરેલી નોકરીઓ તપાસો.'],
    'per day': ['per day', 'प्रतिदिन', 'दररोज', 'દરરોજ'], 'Required Skills': ['Required Skills', 'आवश्यक कौशल', 'आवश्यक कौशल्ये', 'જરૂરી કુશળતાઓ'],
    'Not specified': ['Not specified', 'निर्दिष्ट नहीं', 'नमूद केलेले नाही', 'જણાવેલ નથી'], 'Already applied': ['Already applied', 'पहले ही आवेदन किया', 'आधीच अर्ज केला', 'પહેલેથી અરજી કરી'],
    'History unavailable': ['History unavailable', 'इतिहास उपलब्ध नहीं', 'इतिहास उपलब्ध नाही', 'ઇતિહાસ ઉપલબ્ધ નથી'], 'Job not open': ['Job not open', 'नौकरी खुली नहीं है', 'नोकरी खुली नाही', 'નોકરી ખુલ્લી નથી'],
    'Apply Now': ['Apply Now', 'अभी आवेदन करें', 'आता अर्ज करा', 'હમણાં અરજી કરો'],
    'No pro ID found. Please register first via the Pro Registration page.': ['No pro ID found. Please register first via the Pro Registration page.', 'Pro ID नहीं मिली। पहले साथी पंजीकरण पृष्ठ पर पंजीकरण करें।', 'Pro ID सापडली नाही. आधी साथी नोंदणी पृष्ठावर नोंदणी करा.', 'Pro ID મળી નથી. પહેલાં સાથી નોંધણી પાને નોંધણી કરો.'],
    'Register as a pro to load application history. The browser-stored Pro ID is a workflow reference, not secure sign-in.': ['Register as a pro to load application history. The browser-stored Pro ID is a workflow reference, not secure sign-in.', 'आवेदन इतिहास देखने के लिए साथी के रूप में पंजीकरण करें। ब्राउज़र में सहेजी Pro ID केवल प्रक्रिया संदर्भ है, सुरक्षित लॉग इन नहीं।', 'अर्जांचा इतिहास पाहण्यासाठी साथी म्हणून नोंदणी करा. ब्राउझरमधील Pro ID हा केवळ प्रक्रियेचा संदर्भ आहे, सुरक्षित लॉग इन नाही.', 'અરજીનો ઇતિહાસ જોવા સાથી તરીકે નોંધણી કરો. બ્રાઉઝરમાં સંગ્રહિત Pro ID ફક્ત પ્રક્રિયા માટે છે, સુરક્ષિત લૉગ ઇન નથી.'],
    'No applications were returned for this Pro ID.': ['No applications were returned for this Pro ID.', 'इस Pro ID के लिए कोई आवेदन नहीं मिला।', 'या Pro ID साठी कोणतेही अर्ज मिळाले नाहीत.', 'આ Pro ID માટે કોઈ અરજીઓ મળી નથી.'],
    'Loading applications…': ['Loading applications…', 'आवेदन लोड हो रहे हैं…', 'अर्ज लोड होत आहेत…', 'અરજીઓ લોડ થઈ રહી છે…'], 'Could not load applications': ['Could not load applications', 'आवेदन लोड नहीं हो सके', 'अर्ज लोड करता आले नाहीत', 'અરજીઓ લોડ થઈ શકી નથી'],
    'No applications yet': ['No applications yet', 'अभी कोई आवेदन नहीं आया', 'अद्याप अर्ज आलेले नाहीत', 'હજુ સુધી કોઈ અરજીઓ નથી'], 'No pros have applied to this job yet.': ['No pros have applied to this job yet.', 'इस नौकरी के लिए अभी किसी साथी ने आवेदन नहीं किया है।', 'या नोकरीसाठी अद्याप कोणत्याही साथीने अर्ज केलेला नाही.', 'આ નોકરી માટે હજી કોઈ સાથીે અરજી કરી નથી.'],
    'Names and contact details are not included in this response.': ['Names and contact details are not included in this response.', 'इस उत्तर में नाम और संपर्क विवरण शामिल नहीं हैं।', 'या प्रतिसादात नावे आणि संपर्क तपशील दिलेले नाहीत.', 'આ જવાબમાં નામ અને સંપર્ક વિગતો સામેલ નથી.'],
    'Application ID:': ['Application ID:', 'आवेदन ID:', 'अर्ज ID:', 'અરજી ID:'], 'Pro profile ID:': ['Pro profile ID:', 'साथी प्रोफ़ाइल ID:', 'साथी प्रोफाइल ID:', 'સાથી પ્રોફાઇલ ID:'],
    'Applied:': ['Applied:', 'आवेदन किया:', 'अर्ज केला:', 'અરજી કરી:'], 'Application ID unavailable; cannot update': ['Application ID unavailable; cannot update', 'आवेदन ID उपलब्ध नहीं; अपडेट नहीं कर सकते', 'अर्ज ID उपलब्ध नाही; बदल करता येत नाही', 'અરજી ID ઉપલબ્ધ નથી; અપડેટ કરી શકાતું નથી'],
    'Hire': ['Hire', 'नियुक्त करें', 'नियुक्त करा', 'નોકરીએ રાખો'], 'Reject': ['Reject', 'अस्वीकार करें', 'नकारा', 'નકારો'],
    'Choose a job from My Posted Jobs, or enter a job ID above.': ['Choose a job from My Posted Jobs, or enter a job ID above.', 'मेरी पोस्ट की गई नौकरियों से चुनें या ऊपर Job ID दर्ज करें।', 'माझ्या पोस्ट केलेल्या नोकऱ्यांमधून निवडा किंवा वर Job ID टाका.', 'મારી પોસ્ટ કરેલી નોકરીઓમાંથી પસંદ કરો અથવા ઉપર Job ID દાખલ કરો.'],
    'No recommendations were returned. The recommendation engine may return none for closed jobs.': ['No recommendations were returned. The recommendation engine may return none for closed jobs.', 'कोई सुझाव नहीं मिला। बंद नौकरियों के लिए सुझाव उपलब्ध न हों।', 'कोणत्याही शिफारसी मिळाल्या नाहीत. बंद नोकऱ्यांसाठी शिफारसी मिळणार नाहीत.', 'કોઈ ભલામણ મળી નથી. બંધ નોકરીઓ માટે ભલામણ ન મળે.'],
    'Pro name unavailable': ['Pro name unavailable', 'साथी का नाम उपलब्ध नहीं', 'साथीचे नाव उपलब्ध नाही', 'સાથીનું નામ ઉપલબ્ધ નથી'],
    'Score': ['Score', 'स्कोर', 'गुण', 'સ્કોર'], 'Similarity': ['Similarity', 'समानता', 'साम्य', 'સમાનતા'], 'Skill similarity': ['Skill similarity', 'कौशल समानता', 'कौशल्य साम्य', 'કુશળતા સમાનતા'], 'Distance (km)': ['Distance (km)', 'दूरी (किमी)', 'अंतर (किमी)', 'અંતર (કિમી)'], 'Rating': ['Rating', 'रेटिंग', 'रेटिंग', 'રેટિંગ'], 'Match:': ['Match:', 'मिलान:', 'जुळणी:', 'મેળવણી:'],
    'No additional match details were returned.': ['No additional match details were returned.', 'मिलान का अतिरिक्त विवरण नहीं मिला।', 'जुळणीचा अतिरिक्त तपशील मिळाला नाही.', 'મેળવણીની વધારાની વિગતો મળી નથી.'],
    'Select a job to load recommendations.': ['Select a job to load recommendations.', 'सुझाव देखने के लिए नौकरी चुनें।', 'शिफारसी लोड करण्यासाठी नोकरी निवडा.', 'ભલામણો જોવા નોકરી પસંદ કરો.'], 'Loading pro recommendations…': ['Loading pro recommendations…', 'साथी सुझाव लोड हो रहे हैं…', 'साथींच्या शिफारसी लोड होत आहेत…', 'સાથીની ભલામણો લોડ થઈ રહી છે…'],
    'Pros Recommended for This Job': ['Pros Recommended for This Job', 'इस नौकरी के लिए सुझाए गए साथी', 'या नोकरीसाठी शिफारस केलेले साथी', 'આ નોકરી માટે સૂચવેલા સાથીઓ'], 'Recommendations are separate from pros who have applied.': ['Recommendations are separate from pros who have applied.', 'सुझाव, आवेदन करने वाले साथियों से अलग दिखते हैं।', 'शिफारसी अर्ज केलेल्या साथींपासून वेगळ्या दाखवल्या जातात.', 'ભલામણો અરજી કરનાર સાથીઓથી અલગ છે.'],
    'Review application records and update pending applications.': ['Review application records and update pending applications.', 'आवेदन रिकॉर्ड देखें और लंबित आवेदनों की स्थिति बदलें।', 'अर्ज नोंदी तपासा आणि प्रलंबित अर्जांची स्थिती बदला.', 'અરજી રેકોર્ડ તપાસો અને બાકી અરજીઓની સ્થિતિ અપડેટ કરો.'],
    'Sign in with your patron account to see your posted jobs.': ['Sign in with your patron account to see your posted jobs.', 'पोस्ट की गई नौकरियाँ देखने के लिए नियोजक खाते से लॉग इन करें।', 'पोस्ट केलेल्या नोकऱ्या पाहण्यासाठी नियोजक खात्याने लॉग इन करा.', 'પોસ્ટ કરેલી નોકરીઓ જોવા નિયોજક ખાતાથી લૉગ ઇન કરો.'],
    'This dashboard is available to completed patron accounts. Your existing profile role is never changed here.': ['This dashboard is available to completed patron accounts. Your existing profile role is never changed here.', 'यह डैशबोर्ड केवल पूरी नियोजक प्रोफ़ाइल वाले खातों के लिए है। यहाँ आपकी मौजूदा प्रोफ़ाइल भूमिका नहीं बदली जाती।', 'हा डॅशबोर्ड पूर्ण नियोजक प्रोफाइल असलेल्या खात्यांसाठी आहे. येथे तुमची विद्यमान प्रोफाइल भूमिका बदलली जात नाही.', 'આ ડેશબોર્ડ પૂર્ણ નિયોજક પ્રોફાઇલ ધરાવતા ખાતાઓ માટે છે. અહીં તમારી હાલની પ્રોફાઇલ ભૂમિકા બદલાતી નથી.'],
    'You have not posted any jobs yet.': ['You have not posted any jobs yet.', 'आपने अभी तक कोई नौकरी पोस्ट नहीं की है।', 'तुम्ही अद्याप कोणतीही नोकरी पोस्ट केलेली नाही.', 'તમે હજી સુધી કોઈ નોકરી પોસ્ટ કરી નથી.'], 'The server returned no renderable job records.': ['The server returned no renderable job records.', 'सर्वर से दिखाने योग्य नौकरी रिकॉर्ड नहीं मिले।', 'सर्व्हरकडून दाखवता येण्याजोग्या नोकरी नोंदी मिळाल्या नाहीत.', 'સર્વર તરફથી બતાવી શકાય એવા નોકરી રેકોર્ડ મળ્યા નથી.'],
    'Your sign-in session could not be verified. Sign in again.': ['Your sign-in session could not be verified. Sign in again.', 'आपका लॉग इन सत्र सत्यापित नहीं हो सका। फिर से लॉग इन करें।', 'तुमचे लॉग इन सत्र पडताळता आले नाही. पुन्हा लॉग इन करा.', 'તમારું લૉગ ઇન સત્ર ચકાસી શકાયું નથી. ફરી લૉગ ઇન કરો.'],
    'Untitled job': ['Untitled job', 'बिना शीर्षक की नौकरी', 'शीर्षक नसलेली नोकरी', 'શીર્ષક વિનાની નોકરી'], 'No description provided.': ['No description provided.', 'कोई विवरण नहीं दिया गया।', 'वर्णन दिलेले नाही.', 'કોઈ વર્ણન આપેલું નથી.'], 'Open': ['Open', 'खुली', 'खुली', 'ખુલ્લી'], 'Closed': ['Closed', 'बंद', 'बंद', 'બંધ'], 'unknown': ['unknown', 'अज्ञात', 'अज्ञात', 'અજ્ઞાત'],
    'job loaded from your patron account.': ['job loaded from your patron account.', 'नौकरी आपके नियोजक खाते से लोड हुई।', 'नोकरी तुमच्या नियोजक खात्यातून लोड झाली.', 'નોકરી તમારા નિયોજક ખાતામાંથી લોડ થઈ.'],
    'jobs loaded from your patron account.': ['jobs loaded from your patron account.', 'नौकरियाँ आपके नियोजक खाते से लोड हुईं।', 'नोकऱ्या तुमच्या नियोजक खात्यातून लोड झाल्या.', 'નોકરીઓ તમારા નિયોજક ખાતામાંથી લોડ થઈ.']
  });

  const englishTextKeys = new Map();
  Object.keys(translations.en).forEach((key) => {
    const value = translations.en[key];
    if (typeof value === 'string' && !englishTextKeys.has(value.trim())) englishTextKeys.set(value.trim(), key);
  });
  function localizedPhrase(source, language) {
    const normalized = String(source).trim();
    const index = { en: 0, hi: 1, mr: 2, gu: 3 }[language] ?? 0;
    const phrase = uiPhraseTranslations[normalized];
    if (phrase) return phrase[index];
    const key = englishTextKeys.get(normalized);
    return key ? (translations[language] && translations[language][key]) || translations.en[key] : null;
  }

  function translateTextNodes(root = document.body) {
    if (!root || !document.createTreeWalker) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      const parent = node.parentElement;
      if (!parent || parent.closest('script,style,svg,template,textarea,[contenteditable="true"],code,pre,.card-title,.card-desc,.description,.job h2,.job-details p,.success-job-title,#success-job-title,.pro-name,.pro-meta,.loc-text,[data-user-content]')) continue;
      const current = node.nodeValue;
      let state = translatedTextState.get(node);
      if (state && current !== state.rendered) state.source = current;
      else if (!state) state = { source: current, rendered: current };
      const trimmed = state.source.trim();
      const requestedLanguage = window.LNM_I18N ? window.LNM_I18N.getLanguage() : 'en';
      const language = ['en', 'hi', 'mr', 'gu'].includes(requestedLanguage) ? requestedLanguage : 'en';
      const translation = localizedPhrase(trimmed, language);
      let value = translation || state.source;
      if (!translation && language !== 'en') {
        const countMatch = trimmed.match(/^(\d+) jobs? found for you$/);
        const loadedMatch = trimmed.match(/^(\d+) jobs? loaded from your employer account\.$/);
        const applicationsMatch = trimmed.match(/^(\d+) applications?$/);
        const applicantMatch = trimmed.match(/^Applicant (\d+)$/);
        const recommendationCountMatch = trimmed.match(/^The recommendation service returned no matches for this worker\. There are (\d+) open jobs? in the general feed; they are not being shown as recommendations\.$/);
        const match = countMatch || loadedMatch || applicationsMatch || applicantMatch || recommendationCountMatch;
        if (match) {
          const n = match[1];
          const count = Number(n);
          const plural = count === 1;
          const phrases = {
            hi: countMatch ? `आपके लिए ${n} नौकरी के सुझाव मिले` : loadedMatch ? `${n} ${plural ? 'नौकरी' : 'नौकरियाँ'} आपके नियोजक खाते से लोड ${plural ? 'हुई' : 'हुईं'}।` : applicationsMatch ? `${n} आवेदन` : applicantMatch ? `आवेदक ${n}` : `${n} खुली नौकरियाँ सामान्य सूची में हैं। उन्हें सुझाव के रूप में नहीं दिखाया जा रहा।`,
            mr: countMatch ? `तुमच्यासाठी ${n} नोकऱ्यांच्या शिफारसी मिळाल्या` : loadedMatch ? `${n} ${plural ? 'नोकरी' : 'नोकऱ्या'} तुमच्या नियोजक खात्यातून लोड ${plural ? 'झाली' : 'झाल्या'}.` : applicationsMatch ? `${n} अर्ज` : applicantMatch ? `अर्जदार ${n}` : `${n} खुल्या नोकऱ्या सामान्य यादीत आहेत. त्या शिफारसी म्हणून दाखवल्या जात नाहीत.`,
            gu: countMatch ? `${n} નોકરીઓ તમારા માટે મળી` : loadedMatch ? `${n} ${plural ? 'નોકરી' : 'નોકરીઓ'} તમારા નિયોજક ખાતામાંથી લોડ થઈ.` : applicationsMatch ? `${n} અરજીઓ` : applicantMatch ? `અરજદાર ${n}` : `${n} ખુલ્લી નોકરીઓ સામાન્ય યાદીમાં છે. તે ભલામણ તરીકે બતાવવામાં આવતી નથી.`
          };
          value = phrases[language];
        }
      }
      const leading = state.source.match(/^\s*/)[0];
      const trailing = state.source.match(/\s*$/)[0];
      state.rendered = `${leading}${value}${trailing}`;
      translatedTextState.set(node, state);
      if (node.nodeValue !== state.rendered) node.nodeValue = state.rendered;
    }
  }
  const translatedTextState = new WeakMap();
  const translatedAttributeState = new WeakMap();
  const pageTitleSource = document.title.trim();
  Object.assign(translations.en, { heroHeadline: 'Find Work or Hire Skilled Pros Near You', heroHeadlineLead: 'Find Work', heroHeadlineMiddle: 'or', heroHeadlineHire: 'Hire Skilled Pros', heroHeadlineTail: 'Near You', workerHeroHeadline: 'Start Finding Jobs Near You', registrationSuccessTitle: 'Registration Successful! 🎉', welcomeToLabourNearMe: 'Welcome to Shramik Setu,', workerSuccessDescription: 'Your profile is now live. Patrons near you can find you.', workerIdLabel: 'Pro ID', browseJobsNearMe: 'Browse Jobs Near Me →', returnHomepage: 'Return to Homepage' });
  Object.assign(translations.hi, { heroHeadline: 'अपने आस-पास काम खोजें या कुशल साथी नियुक्त करें', heroHeadlineLead: 'अपने आस-पास', heroHeadlineMiddle: 'काम खोजें या', heroHeadlineHire: 'कुशल साथी नियुक्त करें', heroHeadlineTail: '', workerHeroHeadline: 'अपने आस-पास काम खोजना शुरू करें', registrationSuccessTitle: 'पंजीकरण सफल हुआ! 🎉', welcomeToLabourNearMe: 'Shramik Setu में आपका स्वागत है,', workerSuccessDescription: 'आपकी प्रोफ़ाइल अब उपलब्ध है। आस-पास के नियोजक आपको ढूँढ सकते हैं।', workerIdLabel: 'साथी ID', browseJobsNearMe: 'आस-पास की नौकरियाँ देखें →', returnHomepage: 'मुखपृष्ठ पर लौटें' });
  Object.assign(translations.mr, { heroHeadline: 'तुमच्या जवळ काम शोधा किंवा कुशल साथींना कामावर ठेवा', heroHeadlineLead: 'तुमच्या जवळ', heroHeadlineMiddle: 'काम शोधा किंवा', heroHeadlineHire: 'कुशल साथींना कामावर ठेवा', heroHeadlineTail: '', workerHeroHeadline: 'तुमच्या जवळ काम शोधायला सुरुवात करा', registrationSuccessTitle: 'नोंदणी यशस्वी! 🎉', welcomeToLabourNearMe: 'Shramik Setu मध्ये तुमचे स्वागत आहे,', workerSuccessDescription: 'तुमचे प्रोफाइल आता उपलब्ध आहे. जवळचे नियोजक तुम्हाला शोधू शकतात.', workerIdLabel: 'साथी ID', browseJobsNearMe: 'जवळच्या नोकऱ्या पहा →', returnHomepage: 'मुखपृष्ठावर परत जा' });
  Object.assign(translations.gu, { heroHeadline: 'તમારી નજીક કામ શોધો અથવા કુશળ સાથીઓને કામે રાખો', heroHeadlineLead: 'તમારી નજીક', heroHeadlineMiddle: 'કામ શોધો અથવા', heroHeadlineHire: 'કુશળ સાથીઓને કામે રાખો', heroHeadlineTail: '', workerHeroHeadline: 'તમારી નજીક કામ શોધવાનું શરૂ કરો', registrationSuccessTitle: 'નોંધણી સફળ! 🎉', welcomeToLabourNearMe: 'Shramik Setuમાં તમારું સ્વાગત છે,', workerSuccessDescription: 'તમારી પ્રોફાઇલ હવે ઉપલબ્ધ છે. નજીકના નિયોજકો તમને શોધી શકે છે.', workerIdLabel: 'સાથી ID', browseJobsNearMe: 'નજીકની નોકરીઓ જુઓ →', returnHomepage: 'મુખ્ય પૃષ્ઠ પર પાછા જાઓ' });
  Object.assign(translations.en, { 'Pro ID': 'Pro ID', Match: 'Match' });
  Object.assign(translations.hi, { 'Pro ID': 'साथी ID', Match: 'मिलान' });
  Object.assign(translations.mr, { 'Pro ID': 'साथी ID', Match: 'जुळणी' });
  Object.assign(translations.gu, { 'Worker ID': 'સાથી ID', Match: 'મેળવણી' });

  function translateAttributes(root, language) {
    if (!root || !root.querySelectorAll) return;
    const elements = [ ...(root.matches && root.matches('[placeholder],[aria-label],[title]') ? [root] : []), ...root.querySelectorAll('[placeholder],[aria-label],[title]') ];
    const localeIndex = { en: 0, hi: 1, mr: 2, gu: 3 }[language] ?? 0;
    elements.forEach((element) => {
      ['placeholder', 'aria-label', 'title'].forEach((attribute) => {
        if (!element.hasAttribute(attribute) || (attribute === 'placeholder' && element.hasAttribute('data-i18n-placeholder'))) return;
        let states = translatedAttributeState.get(element);
        if (!states) { states = {}; translatedAttributeState.set(element, states); }
        const current = element.getAttribute(attribute);
        let state = states[attribute];
        if (state && current !== state.rendered) state.source = current;
        else if (!state) state = { source: current, rendered: current };
        state.rendered = localizedPhrase(state.source, language) || state.source;
        states[attribute] = state;
        if (current !== state.rendered) element.setAttribute(attribute, state.rendered);
      });
    });
  }

  const storageKey = 'lnm-language';

  function applyLanguage(language) {
    const selected = translations[language] ? language : 'en';
    const dictionary = translations[selected];
    document.documentElement.lang = selected;
    document.querySelectorAll('[data-i18n]').forEach((element) => {
      const value = dictionary[element.dataset.i18n];
      if (value !== undefined) element.textContent = value;
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
      const value = dictionary[element.dataset.i18nPlaceholder];
      if (value !== undefined) element.placeholder = value;
    });
    document.querySelectorAll('[data-language-selector]').forEach((selector) => {
      selector.value = selected;
      selector.setAttribute('aria-label', dictionary.selectLanguage);
    });
    translateAttributes(document.body, selected);
    if (uiPhraseTranslations[pageTitleSource]) document.title = uiPhraseTranslations[pageTitleSource][{ en: 0, hi: 1, mr: 2, gu: 3 }[selected]];
    translateTextNodes(document.body);
    document.dispatchEvent(new CustomEvent('lnm-language-change', { detail: { language: selected, dictionary } }));
  }

  document.addEventListener('change', (event) => {
    if (!event.target.matches('[data-language-selector]')) return;
    localStorage.setItem(storageKey, event.target.value);
    applyLanguage(event.target.value);
  });

  window.LNM_I18N = {
    getLanguage: () => localStorage.getItem(storageKey) || 'en',
    t: (key) => {
      const dictionary = translations[window.LNM_I18N.getLanguage()] || translations.en;
      if (Object.prototype.hasOwnProperty.call(dictionary, key)) return dictionary[key];
      if (Object.prototype.hasOwnProperty.call(translations.en, key)) return translations.en[key];
      return key;
    },
    keyForText: (text) => {
      const dictionary = translations[window.LNM_I18N.getLanguage()] || translations.en;
      return Object.keys(dictionary).find((key) => dictionary[key] === text) || null;
    },
    translateText: (text) => {
      return localizedPhrase(text, window.LNM_I18N.getLanguage()) || text;
    },
    applyLanguage
  };

  if (document.head && !document.getElementById('lnm-i18n-style')) {
    const style = document.createElement('style');
    style.id = 'lnm-i18n-style';
    style.textContent = '[data-language-selector]{appearance:auto;-webkit-appearance:menulist;width:auto;min-width:7.5rem;max-width:100%;padding:.45rem .65rem;border:1px solid currentColor;border-radius:7px;background:#fff;color:#17324f;font:600 .85rem/1.2 "Noto Sans",sans-serif;cursor:pointer} nav [data-language-selector],header [data-language-selector]{flex:0 0 auto} @media(max-width:600px){[data-language-selector]{min-width:0;width:7.5rem}}';
    document.head.appendChild(style);
  }
  if (document.body && typeof MutationObserver !== 'undefined') {
    const observer = new MutationObserver((records) => {
      records.forEach((record) => {
        if (record.type === 'childList') record.addedNodes.forEach((node) => { if (node.nodeType === Node.ELEMENT_NODE) { translateTextNodes(node); translateAttributes(node, window.LNM_I18N.getLanguage()); } else if (node.nodeType === Node.TEXT_NODE) translateTextNodes(record.target); });
        else if (record.type === 'characterData') translateTextNodes(record.target.parentElement);
      });
    });
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
  }

  applyLanguage(window.LNM_I18N.getLanguage());
})();
