(function () {
  'use strict';

  // Complete UUID-keyed translations for the supplied Skill Master catalogue.
  // Values are [Hindi, Marathi, Gujarati]; English remains the exact API label.
  const skillTranslations = {
    'bc8f55d6-02be-4b83-aa39-1de7d92d3cfa': ['फसल की बुवाई', 'पीक पेरणी', 'પાકનું વાવેતર'],
    '5d493ec1-c98b-46bc-8b05-c5cb8a1f4cd2': ['फसल कटाई', 'कापणी', 'કાપણી'],
    'e3a356d0-7385-4969-bad0-8c813c7e513d': ['सिंचाई व्यवस्था', 'सिंचन व्यवस्था', 'સિંચાઈ વ્યવસ્થા'],
    '15c7f23b-2403-4fb1-8d8f-fbb866c01f37': ['माइक्रोवेव मरम्मत', 'मायक्रोवेव्ह दुरुस्ती', 'માઇક્રોવેવ રિપેર'],
    '3bf5718b-804e-425f-8788-42f80c6489fd': ['रेफ़्रिजरेटर मरम्मत', 'रेफ्रिजरेटर दुरुस्ती', 'રેફ્રિજરેટર રિપેર'],
    'c4da33ff-46ea-409d-a68c-686914d964eb': ['टीवी मरम्मत', 'टीव्ही दुरुस्ती', 'ટીવી રિપેર'],
    'd420999c-cd05-4b93-87c0-ebc047629170': ['वॉशिंग मशीन मरम्मत', 'वॉशिंग मशीन दुरुस्ती', 'વોશિંગ મશીન રિપેર'],
    '92f4c1ab-8644-49ed-933a-c92dde8b9605': ['बच्चों की देखरेख', 'बालसंगोपन', 'બાળ સંભાળ'],
    '32fbd9b8-3b50-4ff1-8c3a-0cfdfb956e79': ['होमवर्क में सहायता', 'गृहपाठासाठी मदत', 'ઘરકામમાં મદદ'],
    '58de98b7-1bd4-42a1-9604-8cb961a842c3': ['शिशु की देखभाल', 'अर्भकाची काळजी', 'શિશુની સંભાળ'],
    '8fa5a833-ded4-41c2-baf6-20b0adba87cf': ['कार पॉलिश करना', 'कार पॉलिश करणे', 'કાર પોલિશ કરવી'],
    'be776ade-f701-4ff5-b42f-e85bcff95954': ['कार की बाहरी धुलाई', 'कारची बाहेरील धुलाई', 'કારની બહારની સફાઈ'],
    '466a88b1-2466-4805-8ed0-abfe394f8de5': ['कार के अंदर की सफाई', 'कारच्या आतील भागाची स्वच्छता', 'કારના અંદરના ભાગની સફાઈ'],
    '9fe871bd-a593-4ead-bb12-5708be7cee91': ['अलमारी बनाना', 'कपाट बनवणे', 'કબાટ બનાવવું'],
    '384371fd-c973-484b-b2fb-941d6008f8c7': ['दरवाज़ा लगाना', 'दरवाजा बसवणे', 'દરવાજો લગાવવો'],
    '4f6a3469-9f64-4904-9e20-e5f55277c2bb': ['फर्नीचर जोड़ना', 'फर्निचर जोडणी', 'ફર્નિચર જોડવું'],
    '730acb04-1d5c-4c0e-9a57-2dbb383f24ed': ['मॉड्यूलर रसोई फिटिंग', 'मॉड्युलर स्वयंपाकघर फिटिंग', 'મોડ્યુલર રસોડાનું ફિટિંગ'],
    '7ffc0b0b-7157-4690-b3bf-8fce972eba78': ['लकड़ी पॉलिश करना', 'लाकूड पॉलिश करणे', 'લાકડું પોલિશ કરવું'],
    'b195209b-218d-4540-a0cd-b2b64a43b824': ['बाथरूम की सफाई', 'स्नानगृह स्वच्छता', 'બાથરૂમની સફાઈ'],
    '1dacc135-712d-4af5-b37b-aaa50e6bce2c': ['फर्श रगड़कर साफ़ करना', 'जमीन घासून स्वच्छ करणे', 'ફર્શ ઘસીને સાફ કરવો'],
    '2f0b741e-3c46-4211-82c8-21bbf105f9f1': ['घर की सफाई', 'घराची स्वच्छता', 'ઘરની સફાઈ'],
    'd350db5c-38dc-4f46-8dc7-d4a5d8ab7116': ['कार्यालय की सफाई', 'कार्यालयाची स्वच्छता', 'કચેરીની સફાઈ'],
    '07d80d5a-ed01-4f57-ad75-c11268b3bca8': ['बड़े पैमाने पर खाना बनाना', 'मोठ्या प्रमाणात स्वयंपाक', 'મોટા પ્રમાણમાં રસોઈ'],
    '1cdc939d-24a3-4fff-bcc1-b7830c45b5d5': ['भारतीय खाना बनाना', 'भारतीय स्वयंपाक', 'ભારતીય રસોઈ'],
    '7936d238-05b6-4dad-a09c-4dba8eb9307a': ['रसोई प्रबंधन', 'स्वयंपाकघर व्यवस्थापन', 'રસોડાનું સંચાલન'],
    'b93bf1a9-3f8d-496f-8cef-a0085bd68574': ['दक्षिण भारतीय खाना बनाना', 'दक्षिण भारतीय स्वयंपाक', 'દક્ષિણ ભારતીય રસોઈ'],
    'd6c692ce-fd60-465a-a5c7-16eab304d07b': ['रसोई की गहरी सफाई', 'स्वयंपाकघराची सखोल स्वच्छता', 'રસોડાની ઊંડી સફાઈ'],
    'f99f4fc4-c212-4f6b-a5e2-e6953286b225': ['सोफ़े की शैम्पू से सफाई', 'सोफ्याची शॅम्पूने स्वच्छता', 'સોફાની શેમ્પૂથી સફાઈ'],
    '8ed34819-e0a9-413e-883a-4c05dd815636': ['टाइल रगड़कर साफ़ करना', 'फरश्या घासून स्वच्छ करणे', 'ટાઇલ્સ ઘસીને સાફ કરવી'],
    '58cf062d-c837-411f-91a2-f5c42eda2b68': ['बुनियादी खाना पकाना', 'मूलभूत स्वयंपाक', 'મૂળભૂત રસોઈ'],
    'fb90d57a-02ae-4ba2-b4dc-cdf32b01d285': ['घर की देखभाल', 'गृहव्यवस्था', 'ઘરની દેખરેખ'],
    '076f0337-a67d-4ebb-ac8a-4e086b667bb0': ['बर्तन धोना', 'भांडी घासणे', 'વાસણ ધોવાં'],
    '26134a04-862c-4321-9f33-c5f02dde9cae': ['कार चलाना', 'कार चालवणे', 'કાર ચલાવવી'],
    '5d7e1e37-fb20-4c4d-b8d8-7738354d52ea': ['व्यावसायिक वाहन चलाना', 'व्यावसायिक वाहन चालवणे', 'વ્યાવસાયિક વાહન ચલાવવું'],
    '5b2c8cbb-cc3b-4d31-9ea2-52c6b105a2ef': ['मार्ग पहचानना', 'मार्ग शोधणे', 'માર્ગ શોધવો'],
    '7b3b6b46-6948-4ec7-b87a-ea85501a62fc': ['दवा लेने की याद दिलाना', 'औषधांची आठवण करून देणे', 'દવા લેવાની યાદ અપાવવી'],
    '005b11cb-839c-41d6-8f8d-680cd8a751fd': ['चलने-फिरने में सहायता', 'हालचालीसाठी मदत', 'હરવા-ફરવામાં સહાય'],
    '744fcde4-21b8-475b-b3d1-668e6026e15b': ['मरीज़ की सहायता', 'रुग्णाची मदत', 'દર્દીની સહાય'],
    'ebcd049e-a783-4659-8e62-fd3b499346d0': ['पंखा लगाना', 'पंखा बसवणे', 'પંખો લગાવવો'],
    '46bcf081-0935-48b5-9ff8-6fe248307fe8': ['इन्वर्टर लगाना', 'इन्व्हर्टर बसवणे', 'ઇન્વર્ટર લગાવવું'],
    '8a0afad7-db7d-4c4c-abb1-cc59e1189c76': ['लाइटिंग लगाना', 'प्रकाश व्यवस्था बसवणे', 'લાઇટિંગ ગોઠવવું'],
    '3a55930f-a9a0-4cf9-a64e-30d0d8b0034c': ['स्विचबोर्ड मरम्मत', 'स्विचबोर्ड दुरुस्ती', 'સ્વિચબોર્ડ રિપેર'],
    '3a08cd81-a48f-4376-8b53-7250866e7140': ['वायरिंग लगाना', 'वायरिंग बसवणे', 'વાયરિંગ કરવું'],
    '5571cf5e-88e0-471c-bd35-a0e55cc6b329': ['भीड़ को सहायता', 'गर्दीला सहाय्य', 'ભીડને સહાય'],
    '1027250f-b5fd-4881-989f-9c9cbbe4e951': ['उपकरण व्यवस्थित करना', 'साहित्याची मांडणी', 'સાધનો ગોઠવવા'],
    'a434148c-8874-4966-8a61-ebe6057dcc92': ['मंच तैयार करना', 'मंच उभारणी', 'મંચ ગોઠવવો'],
    '22a64357-ca0e-4a7b-b328-0690d58297ad': ['बगीचे की सजावट', 'बागेचे सुशोभीकरण', 'બગીચાનું લેન્ડસ્કેપિંગ'],
    '022d692f-cfac-4320-bf5a-3ccd9cd728f5': ['लॉन की देखभाल', 'हिरवळीची देखभाल', 'લૉનની જાળવણી'],
    '9fc0ad90-ded8-442a-a150-07304b9dd2ad': ['पौधों की छँटाई', 'झाडांची छाटणी', 'છોડની કાપણી'],
    '5f924988-0c6d-41d5-89ac-7d1e8354d936': ['कपड़े धोना', 'कपडे धुणे', 'કપડાં ધોવાં'],
    'e9359508-5152-4160-b72d-8ca6b0fac027': ['ड्राई क्लीनिंग संभालना', 'ड्राय क्लीनिंग हाताळणे', 'ડ્રાય ક્લીનિંગ સંભાળવું'],
    '250eea0d-0291-4310-8b44-2a245612ef31': ['इस्त्री करना', 'इस्त्री करणे', 'ઇસ્ત્રી કરવી'],
    '02c770bb-96a2-48d6-8029-d69be58ba95e': ['सामान एक जगह से दूसरी जगह ले जाना', 'साहित्य स्थलांतरित करणे', 'સામાન ખસેડવો'],
    'f4b35098-d78b-4011-8c08-a75be76972be': ['ट्रक में सामान लादना', 'ट्रकमध्ये माल चढवणे', 'ટ્રકમાં માલ ચઢાવવો'],
    'a718b77f-6452-47d7-946c-a7099cfb1795': ['गोदाम में सामान लादना', 'गोदामात माल चढवणे', 'ગોડાઉનમાં માલ ચઢાવવો'],
    '41a80aea-c6a9-4849-b0e3-f8b5ed95daf0': ['फर्श पॉलिश करना', 'जमीन पॉलिश करणे', 'ફર્શ પોલિશ કરવો'],
    'bef74bd6-5a20-4025-a07d-ad0465d99a0a': ['मार्बल काटना', 'संगमरवर कापणे', 'માર્બલ કાપવું'],
    'cb60bdb9-cd45-4625-8d14-c5ce87f39773': ['टाइल लगाना', 'फरश्या बसवणे', 'ટાઇલ લગાવવી'],
    '6339158d-edb1-4da1-bc87-6943456a6028': ['ईंटें ढोना', 'विटा वाहून नेणे', 'ઈંટો ઊંચકવી'],
    '19f5f26a-c12c-4861-ae89-7c5e9472ca1b': ['सीमेंट मिलाना', 'सिमेंट मिसळणे', 'સિમેન્ટ મિશ્ર કરવું'],
    '7090bd5b-bff1-4fbb-b1d0-9eab1abd5797': ['निर्माण स्थल पर सहायता', 'बांधकामस्थळी मदत', 'બાંધકામ સ્થળે સહાય'],
    '8b9244e8-36ba-4496-ad3b-e9d7346130ca': ['कार इंजन मरम्मत', 'कार इंजिन दुरुस्ती', 'કારના એન્જિનનું રિપેર'],
    'f6d167f8-c1c1-4252-8e85-422a4134423f': ['ऑयल बदलने की सेवा', 'ऑइल बदलण्याची सेवा', 'ઓઇલ બદલવાની સેવા'],
    'ede236e9-ecc5-47bc-8283-bb6d44b01f68': ['दोपहिया वाहन मरम्मत', 'दुचाकी दुरुस्ती', 'દ્વિચક્રી વાહન રિપેર'],
    'f627decb-777a-49b9-bc79-4fa53323f96c': ['फर्नीचर लादना', 'फर्निचर चढवणे', 'ફર્નિચર ચઢાવવું'],
    '5f3bb990-f6ca-44e4-8968-242111436992': ['घरेलू सामान पैक करना', 'घरगुती वस्तूंचे पॅकिंग', 'ઘરવખરી પેક કરવી'],
    'ad0951a2-8da6-4661-bf19-38e98f19e974': ['सामान उतारना', 'माल उतरवणे', 'માલ ઉતારવો'],
    '1d0902b9-a567-4966-bcae-4cd0231d69ca': ['बाहरी दीवारों पर रंग करना', 'बाहेरील रंगकाम', 'બહારનું રંગકામ'],
    '4f919e84-d3a1-4fe0-8d9b-a18fa89ab4e3': ['अंदरूनी रंगाई', 'आतील रंगकाम', 'અંદરનું રંગકામ'],
    'd97c4f7d-f207-4b61-a256-67bb6b645af4': ['दीवार पर पुट्टी लगाना', 'भिंतीला पुट्टी लावणे', 'દીવાલ પર પુટ્ટી લગાવવી'],
    '923c455f-11ba-48f4-96b1-b8addae15b77': ['वॉटरप्रूफ़ कोटिंग', 'जलरोधक लेपन', 'વોટરપ્રૂફ કોટિંગ'],
    '6f01808b-945a-4048-8361-d6fe1dfaabd8': ['सामान्य कीटनाशक छिड़काव', 'कीटकनाशक फवारणी', 'સામાન્ય જંતુનાશક છંટકાવ'],
    '6d1553fa-9dba-44e7-989c-84aa5acca4c9': ['चूहों पर नियंत्रण', 'उंदरांचा बंदोबस्त', 'ઉંદર નિયંત્રણ'],
    'f88f933f-a0ed-4f0e-b5ea-bf2124f39001': ['दीमक उपचार', 'वाळवी नियंत्रण', 'ઉધઈની સારવાર'],
    'ac97d9ca-79ac-4791-936f-99ebb926d216': ['बाथरूम फिटिंग लगाना', 'स्नानगृह फिटिंग बसवणे', 'બાથરૂમ ફિટિંગ લગાવવું'],
    '90061a22-13bc-4653-9026-8f72f0152e25': ['नाली की सफाई', 'नाला स्वच्छता', 'ગટર સાફ કરવી'],
    'ed930eaf-c231-4283-a5b4-f61e57babe70': ['रिसाव की मरम्मत', 'गळती दुरुस्ती', 'લીકેજનું રિપેર'],
    '85f64c86-6e1c-49a8-9566-9ca05ca11488': ['पाइप फिटिंग', 'पाइप फिटिंग', 'પાઇપ ફિટિંગ'],
    '45bf1034-ff67-407e-a7cc-6ab979c657fd': ['पानी की टंकी लगाना', 'पाण्याची टाकी बसवणे', 'પાણીની ટાંકી લગાવવી'],
    'b4d525c9-10a3-405e-ae26-61323a20722a': ['गेट की निगरानी', 'प्रवेशद्वारावर लक्ष ठेवणे', 'દરવાજા પર દેખરેખ'],
    '3d3ad7e3-f37b-4b82-9d98-d3c74d94d8b1': ['रात में गश्त', 'रात्री गस्त', 'રાત્રિ પેટ્રોલિંગ'],
    'a0bad1ec-0567-40de-867d-bfb06920a870': ['आगंतुक रजिस्टर का प्रबंधन', 'अभ्यागत नोंदवही व्यवस्थापन', 'મુલાકાતી રજિસ્ટરનું સંચાલન'],
    'd622f82c-aced-4b7a-bdaf-367defddeee1': ['ग्राहक सहायता डेस्क', 'ग्राहक सहाय्यता कक्ष', 'ગ્રાહક સહાય ડેસ્ક'],
    '5769481c-e042-4a82-8fb8-f93c713edd01': ['किराने का सामान चुनना', 'किराणा सामान निवडणे', 'કરિયાણાની વસ્તુઓ પસંદ કરવી'],
    '0317f642-d72c-4b7a-8efe-87cd840cf8cf': ['इन्वेंटरी में सहायता', 'साठा व्यवस्थापनासाठी मदत', 'ઇન્વેન્ટરીમાં સહાય'],
    'd03fea71-b696-44ab-811c-d0eda4d034cc': ['कपड़ों की अल्टरशन', 'कपड्यांची दुरुस्ती व फेरबदल', 'કપડાંમાં ફેરફાર'],
    'd70c8822-4247-4827-b856-754ebb0152dc': ['ब्लाउज़ डिज़ाइन करना', 'ब्लाउज डिझाइन', 'બ્લાઉઝ ડિઝાઇન'],
    '89fc6311-2ee6-4833-85f3-ac4713c2b7a0': ['सिलाई', 'शिवणकाम', 'સિલાઈ'],
    'c57147d0-9b9c-4bd0-8a5f-395e56b0753f': ['एसी लगाना', 'एसी बसवणे', 'એસી ઇન્સ્ટોલ કરવું'],
    'e4dbab44-a8ab-4080-a9c5-ac4ed000024f': ['सीसीटीवी लगाना', 'सीसीटीव्ही बसवणे', 'સીસીટીવી સેટઅપ'],
    '05459100-3692-49cf-be1c-df7196533777': ['आरओ लगाना', 'आरओ बसवणे', 'આરઓ ઇન્સ્ટોલ કરવું'],
    '78584c4a-b3e7-4cee-8d37-d4f447eb02a4': ['आर्क वेल्डिंग', 'आर्क वेल्डिंग', 'આર્ક વેલ્ડિંગ'],
    'f9c113e0-ca09-4f89-a456-5a0aafeb2d51': ['गैस वेल्डिंग', 'गॅस वेल्डिंग', 'ગેસ વેલ્ડિંગ'],
    'a3107853-6756-4750-a177-f76721cd7c81': ['धातु निर्माण', 'धातू घडवणे', 'ધાતુનું ફેબ્રિકેશન'],
    '7aee5ca2-9c87-475a-8c6c-ae67a865262f': ['बिजली की वायरिंग', 'विद्युत वायरिंग', 'ઇલેક્ટ્રિકલ વાયરિંગ'],
    '0bed0a5d-b5c3-4ca4-9be1-846591ac9f03': ['इलेक्ट्रीशियन', 'इलेक्ट्रिशियन', 'ઇલેક્ટ્રિશિયન'],
    '72c744ff-d619-448a-9dd6-7ea6fa64fea1': ['स्विच मरम्मत', 'स्विच दुरुस्ती', 'સ્વિચ રિપેર'],
    'cde51c1c-3900-40fd-a8c9-f20012ba824f': ['वायरिंग', 'वायरिंग', 'વાયરિંગ'],
    '1130d41e-8ca0-4ccb-9c9a-ba4625989d68': ['लकड़ी काटना', 'लाकूड कापणे', 'લાકડું કાપવું']
  };

  const categoryTranslations = {
    'Agricultural Labor': ['कृषि श्रम', 'शेतीकाम', 'ખેતીકામ'],
    'Appliance Repair': ['उपकरण मरम्मत', 'उपकरण दुरुस्ती', 'ઉપકરણ રિપેર'],
    Babysitter: ['बच्चों की देखभाल', 'बालसंगोपन', 'બાળ સંભાળ'],
    'Car Washing': ['कार धुलाई', 'कार धुलाई', 'કાર ધોવાની સેવા'],
    Carpentry: ['बढ़ईगीरी', 'सुतारकाम', 'સુથારકામ'], Cleaning: ['सफाई', 'स्वच्छता', 'સફાઈ'],
    'Cook/Chef': ['रसोइया/शेफ़', 'स्वयंपाकी/शेफ', 'રસોઈયો/શેફ'],
    'Deep Cleaning': ['गहरी सफाई', 'सखोल स्वच्छता', 'ઊંડી સફાઈ'],
    'Domestic Help': ['घरेलू सहायता', 'घरकामासाठी मदत', 'ઘરગથ્થુ સહાય'], Driver: ['ड्राइवर', 'चालक', 'ડ્રાઇવર'],
    'Elder Care': ['बुज़ुर्गों की देखभाल', 'वृद्धांची काळजी', 'વડીલોની સંભાળ'],
    Electrical: ['बिजली का काम', 'विद्युत काम', 'ઇલેક્ટ્રિકલ કામ'], 'Event Support': ['कार्यक्रम सहायता', 'कार्यक्रम सहाय्य', 'કાર્યક્રમ સહાય'],
    Gardening: ['बागवानी', 'बागकाम', 'બાગકામ'], Laundry: ['कपड़े धोने का काम', 'कपडे धुण्याचे काम', 'ધોબીકામ'],
    Loading: ['सामान लादना-उतारना', 'माल चढवणे-उतरवणे', 'માલ ચઢાવવો-ઉતારવો'],
    'Marble Mistries': ['मार्बल मिस्त्री', 'संगमरवर काम', 'માર્બલ કામ'], 'Masonry Helper': ['राजमिस्त्री सहायक', 'गवंडी मदतनीस', 'કડિયા સહાયક'],
    Mechanic: ['मैकेनिक', 'मेकॅनिक', 'મિકેનિક'], 'Moving and Packing': ['सामान शिफ्टिंग और पैकिंग', 'सामान हलवणे व पॅकिंग', 'સામાન ખસેડવો અને પેકિંગ'],
    Painting: ['रंगाई-पुताई', 'रंगकाम', 'રંગકામ'], 'Pest Control': ['कीट नियंत्रण', 'कीटक नियंत्रण', 'જંતુ નિયંત્રણ'],
    Plumbing: ['प्लंबिंग', 'प्लंबિંગ', 'પ્લમ્બિંગ'], 'Security Guarding': ['सुरक्षा सेवा', 'सुरक्षा सेवा', 'સુરક્ષા સેવા'],
    'Shopper Assistant': ['खरीदारी सहायक', 'खरेदी सहाय्यक', 'ખરીદી સહાયક'],
    'Tailor and Sewers': ['दर्जी और सिलाई', 'शिंपी व शिवणकाम', 'દરજી અને સિલાઈ'],
    Technician: ['तकनीशियन', 'तंत्रज्ञ', 'ટેકનિશિયન'], Welder: ['वेल्डर', 'वेल्डर', 'વેલ્ડર'],
    'Other skills': ['अन्य कौशल', 'इतर कौशल्ये', 'અન્ય કૌશલ્યો']
  };

  function makeIdKeyedTranslations(skill) {
    const names = skillTranslations[skill.id];
    const category = skill.category == null ? categoryTranslations['Other skills'] : categoryTranslations[skill.category];
    return {
      [skill.id]: {
        names: { en: skill.skill_name, hi: names && names[0] || skill.skill_name, mr: names && names[1] || skill.skill_name, gu: names && names[2] || skill.skill_name },
        categories: {
          en: skill.category || 'Other skills',
          hi: category && category[0] || skill.category || 'Other skills',
          mr: category && category[1] || skill.category || 'Other skills',
          gu: category && category[2] || skill.category || 'Other skills'
        }
      }
    };
  }

  function translate(key) {
    return window.LNM_I18N ? window.LNM_I18N.t(key) : key;
  }

  function language() {
    return window.LNM_I18N ? window.LNM_I18N.getLanguage() : 'en';
  }

  function displayName(skill) {
    const translations = skill.translationsById && skill.translationsById[skill.id];
    return translations && translations.names[language()] || skill.skill_name;
  }

  function displayCategory(skill) {
    if (!skill.category || !skill.category.trim()) return translate('skillOtherCategory');
    const translations = skill.translationsById && skill.translationsById[skill.id];
    return translations && translations.categories[language()] || skill.category.trim();
  }

  function create(options) {
    const root = options.root;
    const select = document.createElement('select');
    const controls = document.createElement('div');
    const addButton = document.createElement('button');
    const status = document.createElement('div');
    const selectedSection = document.createElement('div');
    const selectedHeading = document.createElement('p');
    const selectedList = document.createElement('div');
    const errorElement = options.errorElement || null;
    let catalogue = [];
    let selected = [];
    let state = 'loading';
    let requestError = null;

    select.id = options.selectId;
    select.className = 'skill-catalogue-select';
    select.setAttribute('aria-describedby', errorElement ? errorElement.id : '');
    select.required = true;
    controls.className = 'skill-catalogue-controls';
    addButton.type = 'button';
    addButton.className = 'skill-catalogue-add';
    status.className = 'skill-catalogue-status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    selectedSection.className = 'skill-catalogue-selected-section';
    selectedHeading.className = 'skill-catalogue-selected-heading';
    selectedList.className = 'skills-chips skill-catalogue-selected';
    selectedList.setAttribute('aria-label', translate('skillSelectedHeading'));

    controls.append(select, addButton);
    selectedSection.append(selectedHeading, selectedList);
    root.classList.add('skill-catalogue');
    root.replaceChildren(controls, status, selectedSection);

    function renderSelected() {
      selectedHeading.textContent = translate('skillSelectedHeading');
      selectedHeading.hidden = selected.length === 0;
      selectedList.setAttribute('aria-label', translate('skillSelectedHeading'));
      selectedList.replaceChildren();

      if (selected.length === 0) {
        const empty = document.createElement('span');
        empty.className = 'skill-catalogue-no-selection';
        empty.textContent = translate('skillNoSelection');
        selectedList.append(empty);
        return;
      }

      selected.forEach((skill) => {
        const chip = document.createElement('div');
        const name = document.createElement('span');
        const remove = document.createElement('button');
        chip.className = 'skill-chip';
        chip.setAttribute('role', 'listitem');
        name.textContent = displayName(skill);
        remove.type = 'button';
        remove.textContent = '×';
        remove.setAttribute('aria-label', `${translate('skillRemove')} ${displayName(skill)}`);
        remove.addEventListener('click', () => {
          selected = selected.filter((item) => item.id !== skill.id);
          render();
          options.onChange(selected.slice());
        });
        chip.append(name, remove);
        selectedList.append(chip);
      });
    }

    function renderStatus() {
      status.replaceChildren();
      status.classList.toggle('is-error', state === 'error');
      status.textContent = '';

      if (state === 'loading') {
        status.textContent = translate('skillLoading');
      } else if (state === 'empty') {
        status.textContent = translate('skillEmpty');
      } else if (state === 'error') {
        status.append(document.createTextNode(translate('skillLoadError')));
        const retry = document.createElement('button');
        retry.type = 'button';
        retry.className = 'skill-catalogue-retry';
        retry.textContent = translate('skillRetry');
        retry.addEventListener('click', load);
        status.append(document.createTextNode(' '), retry);
      }
    }

    function renderSelect() {
      const currentValue = select.value;
      select.replaceChildren();
      const placeholder = document.createElement('option');
      placeholder.value = '';
      placeholder.textContent = translate('skillSelectPlaceholder');
      select.append(placeholder);

      const selectedIds = new Set(selected.map((skill) => skill.id));
      const groups = new Map();
      catalogue.forEach((skill) => {
        if (selectedIds.has(skill.id)) return;
        const category = displayCategory(skill);
        if (!groups.has(category)) groups.set(category, []);
        groups.get(category).push(skill);
      });

      groups.forEach((items, category) => {
        const group = document.createElement('optgroup');
        group.label = category;
        items.forEach((skill) => {
          const option = document.createElement('option');
          option.value = skill.id;
          option.textContent = displayName(skill);
          group.append(option);
        });
        select.append(group);
      });

      if (catalogue.some((skill) => !selectedIds.has(skill.id))) {
        select.value = currentValue && !selectedIds.has(currentValue) ? currentValue : '';
      }
      select.disabled = state !== 'ready' || catalogue.length === selected.length;
      select.classList.toggle('error', root.classList.contains('has-error'));
      addButton.disabled = select.disabled || !select.value;
      addButton.textContent = translate('skillAdd');
    }

    function render() {
      renderSelect();
      renderStatus();
      renderSelected();
      if (errorElement) {
        errorElement.classList.toggle('show', root.classList.contains('has-error'));
      }
    }

    async function load() {
      state = 'loading';
      requestError = null;
      render();
      try {
        const response = await window.lnmRequest(options.path || '/skills/');
        if (!response || !Array.isArray(response.skills)) {
          throw new Error('The skills response did not contain a skills array.');
        }
        const seen = new Set();
        catalogue = response.skills.map((skill) => {
          if (!skill || skill.id == null || typeof skill.skill_name !== 'string' || !skill.skill_name.trim()) {
            throw new Error('The skills response contained an invalid skill.');
          }
          const normalized = {
            id: String(skill.id),
            skill_name: skill.skill_name,
            category: skill.category == null ? null : String(skill.category)
          };
          if (seen.has(normalized.id)) return null;
          seen.add(normalized.id);
          normalized.translationsById = makeIdKeyedTranslations(normalized);
          return normalized;
        }).filter(Boolean);
        state = catalogue.length ? 'ready' : 'empty';
      } catch (error) {
        requestError = error;
        catalogue = [];
        state = 'error';
      }
      render();
    }

    select.addEventListener('change', () => {
      addButton.disabled = !select.value || state !== 'ready';
    });
    addButton.addEventListener('click', () => {
      const skill = catalogue.find((item) => item.id === select.value);
      if (!skill || selected.some((item) => item.id === skill.id)) return;
      selected = selected.concat(skill);
      root.classList.remove('has-error');
      render();
      options.onChange(selected.slice());
    });
    document.addEventListener('lnm-language-change', render);
    load();

    return {
      clearInvalid() {
        root.classList.remove('has-error');
        render();
      },
      setInvalid(invalid) {
        root.classList.toggle('has-error', Boolean(invalid));
        render();
      },
      clear() {
        selected = [];
        root.classList.remove('has-error');
        render();
        options.onChange([]);
      },
      reload: load,
      getSelected() {
        return selected.slice();
      },
      getError() {
        return requestError;
      }
    };
  }

  window.SkillCatalogue = { create };
})();
