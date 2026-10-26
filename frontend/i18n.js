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
      language: 'Language', features: 'Features', how: 'How It Works', about: 'About', login: 'Login', workerRegistration: 'Worker registration', getStarted: 'Get Started', work: 'Work', newTo: 'New to LabourNearMe?', welcomeEyebrow: 'A better way to find work', show: 'Show', hide: 'Hide',
      signIn: 'Sign in', signInTitle: 'Sign in to your account', createAccountAction: 'Create account',
      otpDivider: 'Use your phone number to receive a one-time code.', otpPhoneHint: 'Include your country code, for example +91.', sendOtp: 'Send verification code', otpCode: 'Verification code', otpCodeHint: 'Enter the code sent to your phone.', verifyOtp: 'Verify and continue', otpMissingProfileNotice: 'No profile is linked to this verified phone account. If you registered before, stop and contact support before continuing; creating another profile could duplicate your account.', chooseProfileType: 'Choose which profile to complete:', otpPhoneRequired: 'Enter your phone number.', otpPhoneInvalid: 'Use an international number with country code, for example +919876543210.', otpCodeRequired: 'Enter the verification code.', otpSent: 'A verification code was sent. Check your phone.', otpRequestError: 'Could not send the code. Check the number and try again.', otpVerificationError: 'The code could not be verified. Check it and try again.', otpSessionError: 'Verification did not return an active sign-in session.', otpAuthRequired: 'Your sign-in could not be confirmed by the server. Please sign in again.', otpProfileConflict: 'More than one profile is linked to this account. Contact support before continuing.', otpProfileLookupError: 'Could not verify your profile with the server. Check your connection and try again.', otpUnexpectedResponse: 'The server returned an unexpected profile response. Please try again later.',
      haveAccount: 'Already have an account?', profileContinueWarning: 'Sign-in did not create a profile. Continue only if you have not already registered a', profileContinueSuffix: 'profile.', continueTo: 'Continue to', profile: 'profile',
      gov: 'A Digital India Initiative · Connecting Workers Across Bharat · सुरक्षित · विश्वसनीय · आसान',
      connect: 'Connecting workers and local employers', find: 'Find', or: 'or', hireWorkers: 'Hire Workers', nearYou: 'Near You',
      description: 'A digital platform connecting daily-wage workers with local employers through job listings and skill-based recommendations.',
      joinWorker: 'Join as Worker', browseHire: 'Browse jobs near you & get hired fast', postFind: 'Post a job & find skilled workers today', already: 'Already have an account?', worker: 'Worker', employer: 'Employer',
      loginTitle: 'Sign in to your account', createAccount: 'Create your account', chooseAccount: 'Choose your account type to get started.', roleSignin: 'I am signing in as', roleSignup: 'Create an account as', email: 'Email address', password: 'Password',
      backHome: 'Back to home', welcome: 'WELCOME BACK', workerNearby: 'Find work nearby', employerHire: 'Hire local talent', noteSignin: 'Sign in with your LabourNearMe email and password.', noteSignup: 'Create an account with your email and password. You will complete your Worker or Employer profile next.',
      fullName: 'Full Name', phone: 'Phone Number', skills: 'Skills', category: 'Work category', location: 'Location', experience: 'Experience', wage: 'Expected daily wage (₹)',
      enterName: 'Enter your full name', enterLocation: 'Enter your city or area', addSkill: 'Type a skill and press Enter (e.g. Carpenter)', registerWorker: 'Register as Worker', profileTitle: 'Worker Registration',
      profileDesc: 'Create a worker profile with your contact details, skills, expected daily wage, and current coordinates.',
      registration: 'Worker Registration', fillDetails: 'Fill your details to get started — takes 2 minutes', completion: 'Profile Completion', optional: 'OPTIONAL DETAILS',
      yearsHint: 'Enter complete years as a whole number. A fresher can enter 0 years.', wageHint: 'This amount is saved as your expected daily wage.',
      selectLanguage: 'Select language'
    },
    hi: {
      ...authTranslations.hi,
      language: 'भाषा', features: 'विशेषताएँ', how: 'यह कैसे काम करता है', about: 'हमारे बारे में', login: 'लॉग इन', workerRegistration: 'श्रमिक पंजीकरण', getStarted: 'शुरू करें', work: 'काम', newTo: 'LabourNearMe पर नए हैं?', welcomeEyebrow: 'काम खोजने का बेहतर तरीका', show: 'दिखाएँ', hide: 'छिपाएँ', signIn: 'लॉग इन', signInTitle: 'अपने खाते में लॉग इन करें', createAccountAction: 'खाता बनाएँ',
      haveAccount: 'पहले से खाता है?', profileContinueWarning: 'लॉग इन से प्रोफ़ाइल नहीं बनी। तभी आगे बढ़ें जब आपने पहले से यह प्रोफ़ाइल न बनाई हो:', profileContinueSuffix: 'प्रोफ़ाइल।', continueTo: 'आगे बढ़ें:', profile: 'प्रोफ़ाइल',
      otpDivider: 'कोड पाने के लिए अपना फ़ोन नंबर इस्तेमाल करें।', otpPhoneHint: 'देश का कोड शामिल करें, जैसे +91।', sendOtp: 'सत्यापन कोड भेजें', otpCode: 'सत्यापन कोड', otpCodeHint: 'अपने फ़ोन पर आया कोड दर्ज करें।', verifyOtp: 'सत्यापित करें और आगे बढ़ें', otpMissingProfileNotice: 'इस सत्यापित फ़ोन खाते से कोई प्रोफ़ाइल जुड़ी नहीं है। यदि आपने पहले पंजीकरण किया है, तो रुकें और सहायता से संपर्क करें; नई प्रोफ़ाइल बनाने से दोहराव हो सकता है।', chooseProfileType: 'कौन-सी प्रोफ़ाइल पूरी करनी है चुनें:', otpPhoneRequired: 'अपना फ़ोन नंबर दर्ज करें।', otpPhoneInvalid: 'देश कोड सहित अंतरराष्ट्रीय नंबर डालें, जैसे +919876543210।', otpCodeRequired: 'सत्यापन कोड दर्ज करें।', otpSent: 'सत्यापन कोड भेज दिया गया है। अपना फ़ोन देखें।', otpRequestError: 'कोड नहीं भेजा जा सका। नंबर जाँचकर फिर प्रयास करें।', otpVerificationError: 'कोड सत्यापित नहीं हो सका। जाँचकर फिर प्रयास करें।', otpSessionError: 'सत्यापन के बाद सक्रिय साइन-इन सत्र नहीं मिला।', otpAuthRequired: 'सर्वर आपके साइन-इन की पुष्टि नहीं कर सका। कृपया फिर से लॉग इन करें।', otpProfileConflict: 'इस खाते से एक से अधिक प्रोफ़ाइल जुड़ी हैं। आगे बढ़ने से पहले सहायता से संपर्क करें।', otpProfileLookupError: 'सर्वर से प्रोफ़ाइल की पुष्टि नहीं हो सकी। कनेक्शन जाँचकर फिर प्रयास करें।', otpUnexpectedResponse: 'सर्वर से प्रोफ़ाइल का अप्रत्याशित उत्तर मिला। बाद में फिर प्रयास करें।',
      gov: 'डिजिटल इंडिया पहल · भारत भर के श्रमिकों को जोड़ना · सुरक्षित · विश्वसनीय · आसान', connect: 'श्रमिकों और स्थानीय नियोक्ताओं को जोड़ना', find: 'काम खोजें', or: 'या', hireWorkers: 'श्रमिक नियुक्त करें', nearYou: 'अपने पास',
      description: 'दैनिक वेतन वाले श्रमिकों और स्थानीय नियोक्ताओं को नौकरियों और कौशल सुझावों से जोड़ने वाला डिजिटल मंच।', joinWorker: 'श्रमिक के रूप में जुड़ें', browseHire: 'पास में काम खोजें और जल्दी नियुक्त हों', postFind: 'नौकरी पोस्ट करें और कुशल श्रमिक खोजें', already: 'पहले से खाता है?', worker: 'श्रमिक', employer: 'नियोक्ता',
      loginTitle: 'अपने खाते में लॉग इन करें', createAccount: 'अपना खाता बनाएँ', chooseAccount: 'शुरू करने के लिए अपना खाता प्रकार चुनें।', roleSignin: 'मैं लॉग इन कर रहा/रही हूँ', roleSignup: 'इस रूप में खाता बनाएँ', email: 'ईमेल पता', password: 'पासवर्ड', backHome: 'होम पर वापस जाएँ', welcome: 'वापसी पर स्वागत है', workerNearby: 'पास में काम खोजें', employerHire: 'स्थानीय प्रतिभा नियुक्त करें', noteSignin: 'अपने LabourNearMe ईमेल और पासवर्ड से लॉग इन करें।', noteSignup: 'ईमेल और पासवर्ड से खाता बनाएँ। इसके बाद श्रमिक या नियोक्ता प्रोफ़ाइल पूरी करें।',
      fullName: 'पूरा नाम', phone: 'फ़ोन नंबर', skills: 'कौशल', category: 'काम की श्रेणी', location: 'स्थान', experience: 'अनुभव', wage: 'अपेक्षित दैनिक मज़दूरी (₹)', enterName: 'अपना पूरा नाम लिखें', enterLocation: 'अपना शहर या क्षेत्र लिखें', addSkill: 'कौशल लिखें और Enter दबाएँ (जैसे बढ़ई)', registerWorker: 'श्रमिक के रूप में पंजीकरण करें', profileTitle: 'श्रमिक पंजीकरण', profileDesc: 'अपनी संपर्क जानकारी, कौशल, दैनिक मज़दूरी और वर्तमान निर्देशांकों के साथ श्रमिक प्रोफ़ाइल बनाएँ।', registration: 'श्रमिक पंजीकरण', fillDetails: 'शुरू करने के लिए विवरण भरें — 2 मिनट लगेंगे', completion: 'प्रोफ़ाइल पूर्णता', optional: 'वैकल्पिक विवरण', yearsHint: 'पूरे वर्षों की संख्या दर्ज करें। नए श्रमिक 0 वर्ष दर्ज कर सकते हैं।', wageHint: 'यह राशि आपकी अपेक्षित दैनिक मज़दूरी के रूप में सहेजी जाएगी।', selectLanguage: 'भाषा चुनें'
    },
    gu: {
      ...authTranslations.gu,
      language: 'ભાષા', features: 'સુવિધાઓ', how: 'કેવી રીતે કાર્ય કરે છે', about: 'વિશે', login: 'લૉગ ઇન', workerRegistration: 'કામદાર નોંધણી', getStarted: 'શરૂ કરો', work: 'કામ', newTo: 'LabourNearMe પર નવા છો?', welcomeEyebrow: 'કામ શોધવાની વધુ સારી રીત', show: 'બતાવો', hide: 'છુપાવો', signIn: 'લૉગ ઇન', signInTitle: 'તમારા ખાતામાં લૉગ ઇન કરો', createAccountAction: 'ખાતું બનાવો',
      haveAccount: 'પહેલેથી ખાતું છે?', profileContinueWarning: 'લૉગ ઇનથી પ્રોફાઇલ બની નથી. તમે આ પ્રોફાઇલ પહેલેથી બનાવી ન હોય ત્યારે જ આગળ વધો:', profileContinueSuffix: 'પ્રોફાઇલ.', continueTo: 'આગળ વધો:', profile: 'પ્રોફાઇલ',
      otpDivider: 'એક વખતનો કોડ મેળવવા ફોન નંબર વાપરો.', otpPhoneHint: 'દેશનો કોડ ઉમેરો, ઉદાહરણ તરીકે +91.', sendOtp: 'ચકાસણી કોડ મોકલો', otpCode: 'ચકાસણી કોડ', otpCodeHint: 'તમારા ફોન પર આવેલો કોડ દાખલ કરો.', verifyOtp: 'ચકાસો અને આગળ વધો', otpMissingProfileNotice: 'આ ચકાસેલા ફોન ખાતા સાથે કોઈ પ્રોફાઇલ જોડાયેલી નથી. અગાઉ નોંધણી કરી હોય તો અટકો અને સહાયનો સંપર્ક કરો; બીજી પ્રોફાઇલથી નકલ થઈ શકે છે.', chooseProfileType: 'કઈ પ્રોફાઇલ પૂર્ણ કરવી તે પસંદ કરો:', otpPhoneRequired: 'તમારો ફોન નંબર દાખલ કરો.', otpPhoneInvalid: 'દેશના કોડ સાથે આંતરરાષ્ટ્રીય નંબર વાપરો, જેમ કે +919876543210.', otpCodeRequired: 'ચકાસણી કોડ દાખલ કરો.', otpSent: 'ચકાસણી કોડ મોકલ્યો છે. તમારો ફોન તપાસો.', otpRequestError: 'કોડ મોકલી શકાયો નથી. નંબર તપાસીને ફરી પ્રયાસ કરો.', otpVerificationError: 'કોડ ચકાસી શકાયો નથી. તપાસીને ફરી પ્રયાસ કરો.', otpSessionError: 'ચકાસણી પછી સક્રિય લૉગ ઇન સત્ર મળ્યું નથી.', otpAuthRequired: 'સર્વર તમારા લૉગ ઇનની પુષ્ટિ કરી શક્યું નથી. ફરી લૉગ ઇન કરો.', otpProfileConflict: 'આ ખાતા સાથે એકથી વધુ પ્રોફાઇલ જોડાયેલી છે. આગળ વધતાં પહેલાં સહાયનો સંપર્ક કરો.', otpProfileLookupError: 'સર્વર પર પ્રોફાઇલની પુષ્ટિ થઈ શકી નથી. કનેક્શન તપાસીને ફરી પ્રયાસ કરો.', otpUnexpectedResponse: 'સર્વર તરફથી પ્રોફાઇલનો અનપેક્ષિત જવાબ મળ્યો. પછીથી ફરી પ્રયાસ કરો.',
      gov: 'ડિજિટલ ઇન્ડિયા પહેલ · ભારતભરના કામદારોને જોડે છે · સુરક્ષિત · વિશ્વસનીય · સરળ', connect: 'કામદારો અને સ્થાનિક નોકરીદાતાઓને જોડે છે', find: 'કામ શોધો', or: 'અથવા', hireWorkers: 'કામદારો રાખો', nearYou: 'તમારી નજીક',
      description: 'દૈનિક વેતનના કામદારોને સ્થાનિક નોકરીદાતાઓ સાથે નોકરીઓ અને કૌશલ્ય સૂચનો દ્વારા જોડતું ડિજિટલ પ્લેટફોર્મ.', joinWorker: 'કામદાર તરીકે જોડાઓ', browseHire: 'નજીકમાં કામ શોધો અને ઝડપથી નોકરી મેળવો', postFind: 'નોકરી મૂકો અને કુશળ કામદારો શોધો', already: 'પહેલેથી ખાતું છે?', worker: 'કામદાર', employer: 'નોકરીદાતા',
      loginTitle: 'તમારા ખાતામાં લૉગ ઇન કરો', createAccount: 'તમારું ખાતું બનાવો', chooseAccount: 'શરૂ કરવા માટે ખાતાનો પ્રકાર પસંદ કરો.', roleSignin: 'હું આ તરીકે લૉગ ઇન કરું છું', roleSignup: 'આ તરીકે ખાતું બનાવો', email: 'ઇમેઇલ સરનામું', password: 'પાસવર્ડ', backHome: 'હોમ પર પાછા જાઓ', welcome: 'ફરી સ્વાગત છે', workerNearby: 'નજીકમાં કામ શોધો', employerHire: 'સ્થાનિક કુશળ લોકોને રાખો', noteSignin: 'તમારા LabourNearMe ઇમેઇલ અને પાસવર્ડથી લૉગ ઇન કરો.', noteSignup: 'ઇમેઇલ અને પાસવર્ડથી ખાતું બનાવો. પછી કામદાર અથવા નોકરીદાતાની પ્રોફાઇલ પૂર્ણ કરો.',
      fullName: 'પૂરું નામ', phone: 'ફોન નંબર', skills: 'કૌશલ્યો', category: 'કામનો પ્રકાર', location: 'સ્થળ', experience: 'અનુભવ', wage: 'અપેક્ષિત દૈનિક વેતન (₹)', enterName: 'તમારું પૂરું નામ લખો', enterLocation: 'તમારું શહેર અથવા વિસ્તાર લખો', addSkill: 'કૌશલ્ય લખો અને Enter દબાવો (દા.ત. સુથાર)', registerWorker: 'કામદાર તરીકે નોંધણી કરો', profileTitle: 'કામદાર નોંધણી', profileDesc: 'તમારી સંપર્ક વિગતો, કૌશલ્યો, અપેક્ષિત દૈનિક વેતન અને વર્તમાન સ્થાન સાથે પ્રોફાઇલ બનાવો.', registration: 'કામદાર નોંધણી', fillDetails: 'શરૂ કરવા માટે વિગતો ભરો — 2 મિનિટ લાગશે', completion: 'પ્રોફાઇલ પૂર્ણતા', optional: 'વૈકલ્પિક વિગતો', yearsHint: 'પૂર્ણ વર્ષોની સંખ્યા દાખલ કરો. નવા કામદાર 0 વર્ષ દાખલ કરી શકે છે.', wageHint: 'આ રકમ અપેક્ષિત દૈનિક વેતન તરીકે સાચવાશે.', selectLanguage: 'ભાષા પસંદ કરો'
    },
    mr: {
      ...authTranslations.mr,
      language: 'भाषा', features: 'वैशिष्ट्ये', how: 'हे कसे कार्य करते', about: 'आमच्याबद्दल', login: 'लॉग इन', workerRegistration: 'कामगार नोंदणी', getStarted: 'सुरू करा', work: 'काम', newTo: 'LabourNearMe वर नवीन आहात?', welcomeEyebrow: 'काम शोधण्याचा चांगला मार्ग', show: 'दाखवा', hide: 'लपवा', signIn: 'लॉग इन', signInTitle: 'तुमच्या खात्यात लॉग इन करा', createAccountAction: 'खाते तयार करा',
      haveAccount: 'आधीच खाते आहे?', profileContinueWarning: 'लॉग इनमुळे प्रोफाइल तयार झाले नाही. आधी हे प्रोफाइल तयार केले नसेल तरच पुढे जा:', profileContinueSuffix: 'प्रोफाइल.', continueTo: 'पुढे जा:', profile: 'प्रोफाइल',
      otpDivider: 'एकवेळचा कोड मिळवण्यासाठी फोन नंबर वापरा.', otpPhoneHint: 'देशाचा कोड समाविष्ट करा, उदाहरणार्थ +91.', sendOtp: 'पडताळणी कोड पाठवा', otpCode: 'पडताळणी कोड', otpCodeHint: 'फोनवर आलेला कोड टाका.', verifyOtp: 'पडताळा आणि पुढे जा', otpMissingProfileNotice: 'या पडताळलेल्या फोन खात्याशी प्रोफाइल जोडलेले नाही. आधी नोंदणी केली असल्यास थांबा आणि मदतीशी संपर्क साधा; नवीन प्रोफाइलमुळे डुप्लिकेट होऊ शकते.', chooseProfileType: 'कोणते प्रोफाइल पूर्ण करायचे ते निवडा:', otpPhoneRequired: 'तुमचा फोन नंबर टाका.', otpPhoneInvalid: 'देशाच्या कोडसह आंतरराष्ट्रीय नंबर वापरा, उदा. +919876543210.', otpCodeRequired: 'पडताळणी कोड टाका.', otpSent: 'पडताळणी कोड पाठवला आहे. फोन तपासा.', otpRequestError: 'कोड पाठवता आला नाही. नंबर तपासून पुन्हा प्रयत्न करा.', otpVerificationError: 'कोड पडताळता आला नाही. तपासून पुन्हा प्रयत्न करा.', otpSessionError: 'पडताळणीनंतर सक्रिय लॉग इन सत्र मिळाले नाही.', otpAuthRequired: 'सर्व्हर तुमच्या लॉग इनची पुष्टी करू शकला नाही. पुन्हा लॉग इन करा.', otpProfileConflict: 'या खात्याशी एकापेक्षा जास्त प्रोफाइल जोडलेली आहेत. पुढे जाण्यापूर्वी मदतीशी संपर्क साधा.', otpProfileLookupError: 'सर्व्हरवर प्रोफाइलची पुष्टी होऊ शकली नाही. कनेक्शन तपासून पुन्हा प्रयत्न करा.', otpUnexpectedResponse: 'सर्व्हरकडून प्रोफाइलबाबत अनपेक्षित उत्तर मिळाले. नंतर पुन्हा प्रयत्न करा.',
      gov: 'डिजिटल इंडिया उपक्रम · भारतभरातील कामगारांना जोडतो · सुरक्षित · विश्वासार्ह · सोपे', connect: 'कामगार आणि स्थानिक नियोक्त्यांना जोडतो', find: 'काम शोधा', or: 'किंवा', hireWorkers: 'कामगार नियुक्त करा', nearYou: 'तुमच्या जवळ',
      description: 'दैनिक वेतन कामगारांना स्थानिक नियोक्त्यांशी नोकरीच्या जाहिराती आणि कौशल्याच्या सूचनांद्वारे जोडणारे डिजिटल व्यासपीठ.', joinWorker: 'कामगार म्हणून सामील व्हा', browseHire: 'जवळचे काम शोधा आणि लवकर नोकरी मिळवा', postFind: 'नोकरी पोस्ट करा आणि कुशल कामगार शोधा', already: 'आधीच खाते आहे?', worker: 'कामगार', employer: 'नियोक्ता',
      loginTitle: 'तुमच्या खात्यात लॉग इन करा', createAccount: 'तुमचे खाते तयार करा', chooseAccount: 'सुरू करण्यासाठी खाते प्रकार निवडा.', roleSignin: 'मी याप्रमाणे लॉग इन करत आहे', roleSignup: 'याप्रमाणे खाते तयार करा', email: 'ईमेल पत्ता', password: 'पासवर्ड', backHome: 'मुख्यपृष्ठावर परत जा', welcome: 'पुन्हा स्वागत आहे', workerNearby: 'जवळचे काम शोधा', employerHire: 'स्थानिक कुशल लोकांना नियुक्त करा', noteSignin: 'तुमच्या LabourNearMe ईमेल आणि पासवर्डने लॉग इन करा.', noteSignup: 'ईमेल आणि पासवर्डने खाते तयार करा. त्यानंतर कामगार किंवा नियोक्ता प्रोफाइल पूर्ण करा.',
      fullName: 'पूर्ण नाव', phone: 'फोन नंबर', skills: 'कौशल्ये', category: 'कामाचा प्रकार', location: 'ठिकाण', experience: 'अनुभव', wage: 'अपेक्षित दैनिक मजुरी (₹)', enterName: 'तुमचे पूर्ण नाव लिहा', enterLocation: 'तुमचे शहर किंवा परिसर लिहा', addSkill: 'कौशल्य लिहा आणि Enter दाबा (उदा. सुतार)', registerWorker: 'कामगार म्हणून नोंदणी करा', profileTitle: 'कामगार नोंदणी', profileDesc: 'तुमचे संपर्क तपशील, कौशल्ये, अपेक्षित दैनिक मजुरी आणि सध्याचे स्थान देऊन प्रोफाइल तयार करा.', registration: 'कामगार नोंदणी', fillDetails: 'सुरू करण्यासाठी तपशील भरा — 2 मिनिटे लागतील', completion: 'प्रोफाइल पूर्णता', optional: 'पर्यायी तपशील', yearsHint: 'पूर्ण वर्षांची संख्या द्या. नवीन कामगार 0 वर्षे देऊ शकतो.', wageHint: 'ही रक्कम अपेक्षित दैनिक मजुरी म्हणून जतन केली जाईल.', selectLanguage: 'भाषा निवडा'
    }
  };

  const emailAuthTranslations = {
    en: {
      emailFallbackHeading: 'Email/password demo fallback', emailFallbackDescription: 'Use an email account if SMS delivery is unavailable.',
      authSignIn: 'Continue to sign-in',
      emailRoleLabel: 'Profile type for a new account', emailRoleOptional: 'Choose only when creating an account',
      emailSignIn: 'Sign in with email', emailSignUp: 'Create email account', emailWorking: 'Checking your account…',
      emailConfirmRequired: 'Account creation is not complete yet. Check your email and confirm the address; your profile has not been submitted.',
      emailNoSession: 'Supabase did not return a sign-in session. No profile was submitted.', emailRoleRequired: 'Choose Worker or Employer before creating an account.', emailSignOutFirst: 'Sign out of the current account before creating a separate email account. Accounts are not linked automatically.',
      emailAuthFailed: 'Email sign-in or registration failed:', profileMissingNotice: 'No application profile is linked to this account. If you already registered, stop and contact support before continuing; creating another profile could duplicate it.',
      verifiedAuthRequired: 'A confirmed phone or email sign-in is required before profile registration.'
    },
    hi: {
      emailFallbackHeading: 'डेमो के लिए ईमेल/पासवर्ड विकल्प', emailFallbackDescription: 'SMS न मिलने पर ईमेल खाते का उपयोग करें।',
      authSignIn: 'लॉग इन जारी रखें',
      emailRoleLabel: 'नए खाते के लिए प्रोफ़ाइल प्रकार', emailRoleOptional: 'केवल नया खाता बनाते समय चुनें',
      emailSignIn: 'ईमेल से लॉग इन करें', emailSignUp: 'ईमेल खाता बनाएँ', emailWorking: 'खाते की जाँच हो रही है…',
      emailConfirmRequired: 'खाता बनाना अभी पूरा नहीं हुआ है। ईमेल देखें और पते की पुष्टि करें; प्रोफ़ाइल अभी जमा नहीं की गई है।',
      emailNoSession: 'Supabase से लॉग इन सत्र नहीं मिला। प्रोफ़ाइल जमा नहीं की गई।', emailRoleRequired: 'खाता बनाने से पहले श्रमिक या नियोक्ता चुनें।', emailSignOutFirst: 'अलग ईमेल खाता बनाने से पहले मौजूदा खाते से लॉग आउट करें। खाते अपने आप नहीं जुड़ते।',
      emailAuthFailed: 'ईमेल लॉग इन या पंजीकरण विफल हुआ:', profileMissingNotice: 'इस खाते से कोई प्रोफ़ाइल जुड़ी नहीं है। पहले पंजीकरण किया हो तो रुकें और सहायता से संपर्क करें; दूसरी प्रोफ़ाइल से दोहराव हो सकता है।',
      verifiedAuthRequired: 'प्रोफ़ाइल पंजीकरण से पहले पुष्टि किया हुआ फ़ोन या ईमेल लॉग इन आवश्यक है।'
    },
    gu: {
      emailFallbackHeading: 'ડેમો માટે ઇમેઇલ/પાસવર્ડ વિકલ્પ', emailFallbackDescription: 'SMS ન મળે તો ઇમેઇલ ખાતાનો ઉપયોગ કરો.',
      authSignIn: 'લૉગ ઇન ચાલુ રાખો',
      emailRoleLabel: 'નવા ખાતા માટે પ્રોફાઇલનો પ્રકાર', emailRoleOptional: 'ખાતું બનાવતી વખતે જ પસંદ કરો',
      emailSignIn: 'ઇમેઇલથી લૉગ ઇન કરો', emailSignUp: 'ઇમેઇલ ખાતું બનાવો', emailWorking: 'તમારા ખાતાની તપાસ થઈ રહી છે…',
      emailConfirmRequired: 'ખાતું બનાવવાની પ્રક્રિયા હજુ પૂર્ણ નથી. ઇમેઇલ તપાસીને સરનામું ચકાસો; પ્રોફાઇલ મોકલાઈ નથી.',
      emailNoSession: 'Supabase તરફથી લૉગ ઇન સત્ર મળ્યું નથી. પ્રોફાઇલ મોકલાઈ નથી.', emailRoleRequired: 'ખાતું બનાવતાં પહેલાં કામદાર અથવા નોકરીદાતા પસંદ કરો.', emailSignOutFirst: 'અલગ ઇમેઇલ ખાતું બનાવતાં પહેલાં વર્તમાન ખાતામાંથી લૉગ આઉટ કરો. ખાતાં આપમેળે જોડાતા નથી.',
      emailAuthFailed: 'ઇમેઇલ લૉગ ઇન અથવા નોંધણી નિષ્ફળ:', profileMissingNotice: 'આ ખાતા સાથે કોઈ પ્રોફાઇલ જોડાયેલી નથી. અગાઉ નોંધણી કરી હોય તો અટકો અને સહાયનો સંપર્ક કરો; બીજી પ્રોફાઇલથી નકલ થઈ શકે છે.',
      verifiedAuthRequired: 'પ્રોફાઇલ નોંધણી પહેલાં ચકાસેલું ફોન અથવા ઇમેઇલ લૉગ ઇન જરૂરી છે.'
    },
    mr: {
      emailFallbackHeading: 'डेमोसाठी ईमेल/पासवर्ड पर्याय', emailFallbackDescription: 'SMS मिळत नसल्यास ईमेल खाते वापरा.',
      authSignIn: 'लॉग इन सुरू ठेवा',
      emailRoleLabel: 'नवीन खात्यासाठी प्रोफाइलचा प्रकार', emailRoleOptional: 'फक्त खाते तयार करताना निवडा',
      emailSignIn: 'ईमेलने लॉग इन करा', emailSignUp: 'ईमेल खाते तयार करा', emailWorking: 'खात्याची तपासणी सुरू आहे…',
      emailConfirmRequired: 'खाते तयार करणे अजून पूर्ण झालेले नाही. ईमेल तपासून पत्त्याची पुष्टी करा; प्रोफाइल पाठवलेले नाही.',
      emailNoSession: 'Supabase कडून लॉग इन सत्र मिळाले नाही. प्रोफाइल पाठवलेले नाही.', emailRoleRequired: 'खाते तयार करण्यापूर्वी कामगार किंवा नियोक्ता निवडा.', emailSignOutFirst: 'वेगळे ईमेल खाते तयार करण्यापूर्वी सध्याच्या खात्यातून लॉग आउट करा. खाती आपोआप जोडली जात नाहीत.',
      emailAuthFailed: 'ईमेल लॉग इन किंवा नोंदणी अयशस्वी:', profileMissingNotice: 'या खात्याशी कोणतेही प्रोफाइल जोडलेले नाही. आधी नोंदणी केली असल्यास थांबा आणि मदतीशी संपर्क साधा; दुसऱ्या प्रोफाइलमुळे डुप्लिकेट होऊ शकते.',
      verifiedAuthRequired: 'प्रोफाइल नोंदणीपूर्वी पुष्टी केलेले फोन किंवा ईमेल लॉग इन आवश्यक आहे.'
    }
  };

  Object.keys(emailAuthTranslations).forEach((language) => Object.assign(translations[language], emailAuthTranslations[language]));

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
    document.dispatchEvent(new CustomEvent('lnm-language-change', { detail: { language: selected, dictionary } }));
  }

  document.addEventListener('change', (event) => {
    if (!event.target.matches('[data-language-selector]')) return;
    localStorage.setItem(storageKey, event.target.value);
    applyLanguage(event.target.value);
  });

  window.LNM_I18N = {
    getLanguage: () => localStorage.getItem(storageKey) || 'en',
    t: (key) => (translations[window.LNM_I18N.getLanguage()] || translations.en)[key] || translations.en[key] || key,
    applyLanguage
  };

  applyLanguage(window.LNM_I18N.getLanguage());
})();
