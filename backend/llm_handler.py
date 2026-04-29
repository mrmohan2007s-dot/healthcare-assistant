import json
import os
diseases = {
  "common cold": {
    "keywords": ["cold", "runny nose", "sneezing", "sore throat", "congestion", "nasal discharge"],
    "summary": "A viral infection of the upper respiratory tract causing mild illness.",
    "symptoms": ["Runny or stuffy nose", "Sneezing", "Sore throat", "Mild cough", "Low-grade fever", "Mild body aches", "Fatigue", "Watery eyes"],
    "precautions": ["Rest adequately", "Drink plenty of fluids", "Use saline nasal spray", "Avoid close contact with others", "Wash hands frequently", "Use tissues and dispose properly"],
    "when_to_seek_care": ["Fever above 103°F (39.4°C)", "Symptoms lasting more than 10 days", "Severe headache or sinus pain", "Difficulty breathing", "Wheezing"],
    "sources": [{"title": "CDC – Common Cold", "url": "https://www.cdc.gov/antibiotic-use/colds.html"}],
    "confidence": "high"
  },
  "influenza": {
    "keywords": ["flu", "influenza", "body aches", "chills", "high fever", "fatigue"],
    "summary": "A contagious respiratory illness caused by influenza viruses.",
    "symptoms": ["High fever (100–104°F)", "Chills", "Severe muscle aches", "Headache", "Dry cough", "Fatigue", "Sore throat", "Runny nose", "Vomiting (more common in children)"],
    "precautions": ["Get annual flu vaccine", "Rest and stay home", "Drink fluids", "Take antiviral medications if prescribed", "Avoid contact with vulnerable people"],
    "when_to_seek_care": ["Difficulty breathing", "Persistent chest pain", "Confusion", "Severe vomiting", "Fever above 104°F", "Worsening after initial improvement"],
    "sources": [{"title": "CDC – Flu", "url": "https://www.cdc.gov/flu/index.htm"}],
    "confidence": "high"
  },
  "covid-19": {
    "keywords": ["covid", "coronavirus", "loss of smell", "loss of taste", "covid19", "sars"],
    "summary": "A respiratory illness caused by the SARS-CoV-2 virus.",
    "symptoms": ["Fever or chills", "Cough", "Shortness of breath", "Fatigue", "Loss of taste or smell", "Sore throat", "Headache", "Muscle aches", "Nausea or vomiting", "Diarrhea"],
    "precautions": ["Get vaccinated and boosted", "Wear a mask in crowded areas", "Isolate if positive", "Ventilate indoor spaces", "Wash hands frequently"],
    "when_to_seek_care": ["Trouble breathing", "Persistent chest pain", "New confusion", "Inability to stay awake", "Bluish lips or face"],
    "sources": [{"title": "CDC – COVID-19", "url": "https://www.cdc.gov/coronavirus/2019-ncov/index.html"}],
    "confidence": "high"
  },
  "pneumonia": {
    "keywords": ["pneumonia", "lung infection", "chest infection", "productive cough"],
    "summary": "An infection that inflames air sacs in one or both lungs.",
    "symptoms": ["Chest pain when breathing or coughing", "Cough with phlegm", "Fever, sweating, chills", "Shortness of breath", "Fatigue", "Nausea or vomiting", "Confusion (in older adults)"],
    "precautions": ["Get pneumococcal vaccine", "Practice good hygiene", "Don't smoke", "Treat respiratory illnesses promptly", "Rest and fluids"],
    "when_to_seek_care": ["Difficulty breathing", "Chest pain", "Fever above 102°F", "Coughing up blood", "Confusion", "Bluish nails or lips"],
    "sources": [{"title": "Mayo Clinic – Pneumonia", "url": "https://www.mayoclinic.org/diseases-conditions/pneumonia/symptoms-causes/syc-20354204"}],
    "confidence": "high"
  },
  "bronchitis": {
    "keywords": ["bronchitis", "bronchial", "persistent cough", "mucus cough", "chest congestion"],
    "summary": "Inflammation of the lining of bronchial tubes, which carry air to the lungs.",
    "symptoms": ["Persistent cough with mucus", "Chest discomfort", "Fatigue", "Slight fever and chills", "Shortness of breath", "Wheezing"],
    "precautions": ["Avoid smoking", "Use a humidifier", "Rest", "Drink fluids", "Avoid lung irritants"],
    "when_to_seek_care": ["Cough lasting more than 3 weeks", "Fever above 100.4°F", "Blood in mucus", "Difficulty breathing", "Wheezing severely"],
    "sources": [{"title": "Mayo Clinic – Bronchitis", "url": "https://www.mayoclinic.org/diseases-conditions/bronchitis/symptoms-causes/syc-20355566"}],
    "confidence": "high"
  },
  "asthma": {
    "keywords": ["asthma", "wheezing", "breathlessness", "inhaler", "bronchospasm"],
    "summary": "A condition in which airways narrow, swell, and produce extra mucus, making breathing difficult.",
    "symptoms": ["Shortness of breath", "Chest tightness", "Wheezing", "Coughing (especially at night)", "Rapid breathing", "Fatigue during exercise"],
    "precautions": ["Use prescribed inhalers", "Identify and avoid triggers", "Monitor peak flow", "Take controller medications", "Keep rescue inhaler accessible"],
    "when_to_seek_care": ["Severe shortness of breath", "Lips turning blue", "No improvement from inhaler", "Rapid worsening", "Unable to speak in full sentences"],
    "sources": [{"title": "CDC – Asthma", "url": "https://www.cdc.gov/asthma/"}],
    "confidence": "high"
  },
  "hypertension": {
    "keywords": ["hypertension", "high blood pressure", "elevated BP", "blood pressure"],
    "summary": "A chronic condition where blood pressure in the arteries is persistently elevated.",
    "symptoms": ["Often no symptoms (silent killer)", "Headaches", "Nosebleeds", "Shortness of breath", "Dizziness", "Chest pain", "Visual changes"],
    "precautions": ["Monitor blood pressure regularly", "Reduce salt intake", "Exercise regularly", "Maintain healthy weight", "Limit alcohol", "Take prescribed medications"],
    "when_to_seek_care": ["BP above 180/120 mmHg", "Chest pain", "Severe headache", "Vision problems", "Shortness of breath", "Nosebleed that won't stop"],
    "sources": [{"title": "AHA – High Blood Pressure", "url": "https://www.heart.org/en/health-topics/high-blood-pressure"}],
    "confidence": "high"
  },
  "diabetes type 2": {
    "keywords": ["diabetes", "type 2 diabetes", "high blood sugar", "insulin resistance", "hyperglycemia"],
    "summary": "A chronic condition affecting how the body processes blood sugar (glucose).",
    "symptoms": ["Increased thirst", "Frequent urination", "Increased hunger", "Fatigue", "Blurred vision", "Slow-healing sores", "Frequent infections", "Tingling in hands/feet"],
    "precautions": ["Monitor blood sugar", "Follow diabetic diet", "Exercise regularly", "Take medications as prescribed", "Maintain healthy weight", "Check feet daily"],
    "when_to_seek_care": ["Blood sugar above 300 mg/dL", "Ketones in urine", "Confusion", "Fruity breath odor", "Rapid breathing", "Severe nausea or vomiting"],
    "sources": [{"title": "CDC – Type 2 Diabetes", "url": "https://www.cdc.gov/diabetes/basics/type2.html"}],
    "confidence": "high"
  },
  "diabetes type 1": {
    "keywords": ["type 1 diabetes", "juvenile diabetes", "insulin dependent"],
    "summary": "An autoimmune condition in which the pancreas produces little or no insulin.",
    "symptoms": ["Extreme thirst", "Frequent urination", "Weight loss", "Fatigue", "Blurred vision", "Fruity-smelling breath", "Nausea", "Stomach pain"],
    "precautions": ["Daily insulin therapy", "Monitor blood glucose", "Carry fast-acting sugar", "Wear medical ID", "Regular medical checkups"],
    "when_to_seek_care": ["Ketoacidosis symptoms", "Blood sugar extremes", "Confusion", "Vomiting", "Rapid breathing"],
    "sources": [{"title": "JDRF – Type 1 Diabetes", "url": "https://www.jdrf.org/t1d-resources/"}],
    "confidence": "high"
  },
  "stroke": {
    "keywords": ["stroke", "brain attack", "facial drooping", "arm weakness", "sudden numbness"],
    "summary": "A medical emergency where blood supply to part of the brain is cut off.",
    "symptoms": ["Sudden numbness or weakness in face/arm/leg", "Sudden confusion or trouble speaking", "Sudden vision problems", "Sudden severe headache", "Loss of balance or coordination"],
    "precautions": ["Know FAST signs (Face, Arms, Speech, Time)", "Control blood pressure", "Don't smoke", "Control cholesterol", "Exercise regularly"],
    "when_to_seek_care": ["ANY stroke symptom – call emergency services immediately", "Sudden severe headache", "Sudden vision loss", "Sudden weakness or numbness"],
    "sources": [{"title": "CDC – Stroke", "url": "https://www.cdc.gov/stroke/"}],
    "confidence": "high"
  },
  "heart attack": {
    "keywords": ["heart attack", "myocardial infarction", "MI", "cardiac arrest", "chest tightness"],
    "summary": "Occurs when blood flow to part of the heart is blocked.",
    "symptoms": ["Chest pain, pressure or squeezing", "Pain spreading to arm, neck, or jaw", "Shortness of breath", "Cold sweat", "Nausea", "Lightheadedness", "Fatigue"],
    "precautions": ["Chew aspirin if prescribed", "Call emergency services immediately", "Rest", "Don't drive yourself", "Stay calm"],
    "when_to_seek_care": ["ANY suspected heart attack – call 911 immediately", "Chest pain lasting more than a few minutes", "Pain with shortness of breath", "Sudden severe weakness"],
    "sources": [{"title": "AHA – Heart Attack", "url": "https://www.heart.org/en/health-topics/heart-attack"}],
    "confidence": "high"
  },
  "migraine": {
    "keywords": ["migraine", "severe headache", "aura", "throbbing headache", "nausea with headache", "light sensitivity"],
    "summary": "A neurological condition causing intense, debilitating headaches.",
    "symptoms": ["Throbbing or pulsing headache (often one side)", "Nausea or vomiting", "Sensitivity to light and sound", "Visual aura (flashes, zigzag lines)", "Dizziness", "Fatigue"],
    "precautions": ["Identify and avoid triggers", "Maintain regular sleep schedule", "Stay hydrated", "Take medications at onset", "Rest in dark quiet room"],
    "when_to_seek_care": ["Worst headache of your life", "Headache with fever and stiff neck", "Neurological symptoms", "Headache after head injury", "Progressive worsening"],
    "sources": [{"title": "Mayo Clinic – Migraine", "url": "https://www.mayoclinic.org/diseases-conditions/migraine-headache/symptoms-causes/syc-20360201"}],
    "confidence": "high"
  },
  "depression": {
    "keywords": ["depression", "depressed", "low mood", "hopelessness", "sadness", "loss of interest"],
    "summary": "A mood disorder causing persistent feelings of sadness and loss of interest.",
    "symptoms": ["Persistent sadness", "Loss of interest in activities", "Fatigue", "Sleep disturbances", "Appetite changes", "Difficulty concentrating", "Feelings of worthlessness", "Thoughts of death"],
    "precautions": ["Seek professional help", "Take medications as prescribed", "Build support network", "Regular exercise", "Limit alcohol", "Practice self-care"],
    "when_to_seek_care": ["Thoughts of self-harm or suicide", "Inability to care for yourself", "Symptoms lasting more than 2 weeks", "Psychosis symptoms"],
    "sources": [{"title": "NIMH – Depression", "url": "https://www.nimh.nih.gov/health/topics/depression"}],
    "confidence": "high"
  },
  "anxiety disorder": {
    "keywords": ["anxiety", "panic", "worry", "panic attack", "anxious", "nervous"],
    "summary": "A group of mental health conditions characterized by excessive worry and fear.",
    "symptoms": ["Excessive worrying", "Restlessness", "Rapid heartbeat", "Sweating", "Trembling", "Shortness of breath", "Sleep problems", "Difficulty concentrating", "Muscle tension"],
    "precautions": ["Practice relaxation techniques", "Regular exercise", "Limit caffeine and alcohol", "Seek therapy", "Take prescribed medications", "Maintain routine"],
    "when_to_seek_care": ["Panic attacks", "Anxiety interfering with daily life", "Thoughts of self-harm", "Physical symptoms are severe"],
    "sources": [{"title": "NIMH – Anxiety Disorders", "url": "https://www.nimh.nih.gov/health/topics/anxiety-disorders"}],
    "confidence": "high"
  },
  "urinary tract infection": {
    "keywords": ["UTI", "urinary tract infection", "burning urination", "frequent urination", "bladder infection"],
    "summary": "An infection in any part of the urinary system, most commonly the bladder.",
    "symptoms": ["Burning sensation when urinating", "Frequent urge to urinate", "Cloudy or strong-smelling urine", "Pelvic pain", "Blood in urine", "Low-grade fever"],
    "precautions": ["Drink plenty of water", "Urinate frequently", "Wipe front to back", "Urinate after sex", "Avoid irritating feminine products"],
    "when_to_seek_care": ["Fever above 101°F", "Back or side pain", "Nausea and vomiting", "Symptoms not improving in 2-3 days", "Blood in urine"],
    "sources": [{"title": "Mayo Clinic – UTI", "url": "https://www.mayoclinic.org/diseases-conditions/urinary-tract-infection/symptoms-causes/syc-20353447"}],
    "confidence": "high"
  },
  "appendicitis": {
    "keywords": ["appendicitis", "appendix pain", "lower right abdominal pain", "McBurney's point"],
    "summary": "Inflammation of the appendix requiring urgent medical attention.",
    "symptoms": ["Pain starting around navel moving to lower right abdomen", "Nausea and vomiting", "Loss of appetite", "Fever", "Abdominal bloating", "Inability to pass gas"],
    "precautions": ["Do not eat or drink if suspected", "Do not take pain relievers before diagnosis", "Seek emergency care immediately"],
    "when_to_seek_care": ["ANY suspected appendicitis – go to ER immediately", "Severe abdominal pain", "Fever with abdominal pain", "Pain worsening rapidly"],
    "sources": [{"title": "Mayo Clinic – Appendicitis", "url": "https://www.mayoclinic.org/diseases-conditions/appendicitis/symptoms-causes/syc-20369543"}],
    "confidence": "high"
  },
  "gastroenteritis": {
    "keywords": ["gastroenteritis", "stomach flu", "stomach bug", "food poisoning", "vomiting diarrhea"],
    "summary": "Inflammation of the stomach and intestines, causing diarrhea and vomiting.",
    "symptoms": ["Diarrhea", "Nausea and vomiting", "Stomach cramps", "Low-grade fever", "Muscle aches", "Headache", "Loss of appetite"],
    "precautions": ["Stay hydrated with oral rehydration solutions", "Rest", "Eat bland foods (BRAT diet)", "Avoid dairy and fatty foods", "Wash hands thoroughly"],
    "when_to_seek_care": ["Dehydration signs", "Blood in stool or vomit", "Fever above 102°F", "Symptoms lasting more than 3 days", "Unable to keep fluids down"],
    "sources": [{"title": "CDC – Norovirus", "url": "https://www.cdc.gov/norovirus/index.html"}],
    "confidence": "high"
  },
  "irritable bowel syndrome": {
    "keywords": ["IBS", "irritable bowel", "bowel cramps", "alternating diarrhea constipation"],
    "summary": "A common disorder affecting the large intestine causing cramping and bowel changes.",
    "symptoms": ["Abdominal cramping", "Bloating", "Gas", "Diarrhea", "Constipation", "Mucus in stool", "Urgency to have bowel movement"],
    "precautions": ["Identify food triggers", "Eat smaller meals", "Manage stress", "Exercise regularly", "Try low-FODMAP diet if recommended"],
    "when_to_seek_care": ["Blood in stool", "Unexplained weight loss", "Fever", "Severe or changing pain", "Waking from sleep due to symptoms"],
    "sources": [{"title": "Mayo Clinic – IBS", "url": "https://www.mayoclinic.org/diseases-conditions/irritable-bowel-syndrome/symptoms-causes/syc-20360016"}],
    "confidence": "high"
  },
  "acid reflux": {
    "keywords": ["acid reflux", "GERD", "heartburn", "acid indigestion", "regurgitation"],
    "summary": "When stomach acid flows back into the esophagus, causing heartburn.",
    "symptoms": ["Heartburn (burning chest sensation)", "Regurgitation of food", "Chest pain", "Difficulty swallowing", "Lump sensation in throat", "Chronic cough", "Hoarseness"],
    "precautions": ["Eat smaller meals", "Avoid trigger foods (spicy, fatty, acidic)", "Don't lie down after eating", "Elevate head of bed", "Maintain healthy weight"],
    "when_to_seek_care": ["Difficulty swallowing", "Weight loss", "Chest pain (rule out heart)", "Vomiting blood", "Symptoms not responding to antacids"],
    "sources": [{"title": "Mayo Clinic – GERD", "url": "https://www.mayoclinic.org/diseases-conditions/gerd/symptoms-causes/syc-20361940"}],
    "confidence": "high"
  },
  "conjunctivitis": {
    "keywords": ["conjunctivitis", "pink eye", "red eye", "eye infection", "itchy eyes"],
    "summary": "Inflammation or infection of the transparent membrane lining the eyelid.",
    "symptoms": ["Pink or red in the white of the eye", "Increased tearing", "Discharge (watery or thick)", "Itching", "Burning sensation", "Crusty eyelids in the morning", "Sensitivity to light"],
    "precautions": ["Wash hands frequently", "Don't touch eyes", "Don't share towels or pillowcases", "Remove contact lenses", "Don't share eye makeup"],
    "when_to_seek_care": ["Eye pain", "Sensitivity to light", "Blurred vision", "Intense redness", "Symptoms not improving in 3 days"],
    "sources": [{"title": "CDC – Conjunctivitis", "url": "https://www.cdc.gov/conjunctivitis/index.html"}],
    "confidence": "high"
  },
  "otitis media": {
    "keywords": ["ear infection", "otitis media", "ear pain", "middle ear infection"],
    "summary": "An infection of the middle ear, most common in children.",
    "symptoms": ["Ear pain", "Tugging at ear (in children)", "Difficulty hearing", "Fluid drainage from ear", "Fussiness in infants", "Fever", "Difficulty sleeping", "Headache"],
    "precautions": ["Complete antibiotic course if prescribed", "Use pain relievers", "Apply warm compress", "Avoid smoking around children", "Breastfeed infants"],
    "when_to_seek_care": ["Fever above 102°F", "Severe ear pain", "Discharge from ear", "Hearing loss", "Symptoms lasting more than 2-3 days"],
    "sources": [{"title": "Mayo Clinic – Ear Infection", "url": "https://www.mayoclinic.org/diseases-conditions/ear-infections/symptoms-causes/syc-20351616"}],
    "confidence": "high"
  },
  "sinusitis": {
    "keywords": ["sinusitis", "sinus infection", "facial pressure", "nasal congestion", "sinus pain"],
    "summary": "Inflammation of the sinuses, often causing pain and congestion.",
    "symptoms": ["Facial pain or pressure", "Nasal congestion", "Thick nasal discharge (yellow/green)", "Reduced sense of smell", "Headache", "Fatigue", "Fever", "Toothache"],
    "precautions": ["Use saline rinse", "Inhale steam", "Use humidifier", "Stay hydrated", "Avoid allergens and irritants"],
    "when_to_seek_care": ["Symptoms lasting more than 10 days", "Severe headache", "Fever above 102°F", "Vision changes", "Stiff neck", "Swelling around eyes"],
    "sources": [{"title": "CDC – Sinusitis", "url": "https://www.cdc.gov/antibiotic-use/sinusitis.html"}],
    "confidence": "high"
  },
  "chickenpox": {
    "keywords": ["chickenpox", "varicella", "itchy rash blisters", "pox"],
    "summary": "A highly contagious viral infection causing an itchy blister rash.",
    "symptoms": ["Itchy blister rash starting on face/trunk", "Fever", "Fatigue", "Loss of appetite", "Headache", "Rash progressing to fluid-filled blisters"],
    "precautions": ["Isolate until blisters are crusted over", "Don't scratch blisters", "Trim nails short", "Use calamine lotion", "Take oatmeal baths", "Get vaccinated"],
    "when_to_seek_care": ["Rash near eyes", "Bacterial infection of blisters", "High fever", "Difficulty breathing", "Severe headache", "Stiff neck"],
    "sources": [{"title": "CDC – Chickenpox", "url": "https://www.cdc.gov/chickenpox/index.html"}],
    "confidence": "high"
  },
  "measles": {
    "keywords": ["measles", "morbilli", "koplik spots", "rash fever"],
    "summary": "A highly contagious viral illness characterized by fever and rash.",
    "symptoms": ["High fever", "Cough", "Runny nose", "Red eyes", "Skin rash (starts on face)", "Koplik spots in mouth", "Fatigue"],
    "precautions": ["Get MMR vaccine", "Isolate infected person", "Rest and fluids", "Vitamin A supplementation if recommended"],
    "when_to_seek_care": ["Difficulty breathing", "Seizures", "Confusion", "Severe headache", "Eye pain"],
    "sources": [{"title": "CDC – Measles", "url": "https://www.cdc.gov/measles/index.html"}],
    "confidence": "high"
  },
  "malaria": {
    "keywords": ["malaria", "plasmodium", "mosquito fever", "cyclic fever", "chills rigor"],
    "summary": "A mosquito-borne parasitic infection causing cyclic fever and chills.",
    "symptoms": ["Cyclical fever and chills", "Sweating", "Headache", "Nausea and vomiting", "Muscle pain", "Fatigue", "Anemia", "Jaundice"],
    "precautions": ["Use antimalarial medications", "Use insect repellent", "Sleep under mosquito nets", "Wear protective clothing", "Seek treatment promptly"],
    "when_to_seek_care": ["High fever after travel to endemic areas", "Altered consciousness", "Severe anemia", "Difficulty breathing", "Seizures"],
    "sources": [{"title": "WHO – Malaria", "url": "https://www.who.int/news-room/fact-sheets/detail/malaria"}],
    "confidence": "high"
  },
  "dengue fever": {
    "keywords": ["dengue", "dengue fever", "breakbone fever", "dengue hemorrhagic"],
    "summary": "A mosquito-borne viral infection causing severe flu-like illness.",
    "symptoms": ["Sudden high fever", "Severe headache", "Pain behind eyes", "Severe muscle and joint pain", "Skin rash", "Nausea", "Vomiting", "Fatigue"],
    "precautions": ["Prevent mosquito bites", "Use repellent", "Wear long sleeves", "Eliminate standing water", "Rest and stay hydrated"],
    "when_to_seek_care": ["Bleeding gums or nose", "Blood in urine or stool", "Severe abdominal pain", "Rapid breathing", "Cold or clammy skin"],
    "sources": [{"title": "WHO – Dengue", "url": "https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue"}],
    "confidence": "high"
  },
  "typhoid fever": {
    "keywords": ["typhoid", "enteric fever", "salmonella typhi"],
    "summary": "A bacterial infection caused by Salmonella typhi, spread through contaminated food/water.",
    "symptoms": ["Prolonged high fever", "Weakness", "Abdominal pain", "Headache", "Loss of appetite", "Rash (rose spots)", "Constipation or diarrhea"],
    "precautions": ["Get vaccinated", "Drink safe water", "Eat well-cooked food", "Wash hands regularly", "Avoid ice from unknown sources"],
    "when_to_seek_care": ["Fever lasting more than 3 days", "Severe abdominal pain", "Confusion", "Rash", "Worsening symptoms after initial improvement"],
    "sources": [{"title": "CDC – Typhoid Fever", "url": "https://www.cdc.gov/typhoid-fever/index.html"}],
    "confidence": "high"
  },
  "tuberculosis": {
    "keywords": ["tuberculosis", "TB", "pulmonary TB", "consumption", "Mycobacterium"],
    "summary": "A bacterial infection primarily affecting the lungs, spread through airborne droplets.",
    "symptoms": ["Persistent cough lasting 3+ weeks", "Coughing up blood", "Chest pain", "Unintentional weight loss", "Fatigue", "Night sweats", "Fever", "Loss of appetite"],
    "precautions": ["Complete full course of antibiotics", "Cover mouth when coughing", "Ensure good ventilation", "Get tested if exposed", "BCG vaccination"],
    "when_to_seek_care": ["Coughing up blood", "Difficulty breathing", "Persistent fever", "Severe weight loss", "Contact with known TB patient"],
    "sources": [{"title": "WHO – Tuberculosis", "url": "https://www.who.int/news-room/fact-sheets/detail/tuberculosis"}],
    "confidence": "high"
  },
  "HIV/AIDS": {
    "keywords": ["HIV", "AIDS", "human immunodeficiency virus", "retrovirus", "CD4"],
    "summary": "HIV is a virus that attacks the immune system; AIDS is the advanced stage.",
    "symptoms": ["Early: flu-like illness, fever, swollen lymph nodes", "Later: chronic fatigue", "Weight loss", "Frequent infections", "Night sweats", "Oral thrush", "Skin problems"],
    "precautions": ["Use condoms consistently", "Get tested regularly", "Take antiretroviral therapy (ART)", "Don't share needles", "PrEP for high-risk individuals"],
    "when_to_seek_care": ["Suspected exposure", "Persistent fever", "Unexplained weight loss", "Recurrent infections", "CD4 count drops"],
    "sources": [{"title": "CDC – HIV", "url": "https://www.cdc.gov/hiv/index.html"}],
    "confidence": "high"
  },
  "hepatitis A": {
    "keywords": ["hepatitis A", "HAV", "jaundice", "liver inflammation viral"],
    "summary": "A highly contagious liver infection caused by the hepatitis A virus.",
    "symptoms": ["Fatigue", "Sudden nausea and vomiting", "Abdominal pain", "Loss of appetite", "Jaundice (yellowing of skin/eyes)", "Dark urine", "Clay-colored stools", "Joint pain"],
    "precautions": ["Get vaccinated", "Wash hands after using toilet", "Avoid contaminated water", "Eat properly prepared food", "Avoid raw shellfish"],
    "when_to_seek_care": ["Yellowing of eyes or skin", "Abdominal pain", "Vomiting repeatedly", "High fever"],
    "sources": [{"title": "CDC – Hepatitis A", "url": "https://www.cdc.gov/hepatitis/hav/index.htm"}],
    "confidence": "high"
  },
  "hepatitis B": {
    "keywords": ["hepatitis B", "HBV", "liver infection", "chronic liver disease"],
    "summary": "A liver infection caused by the hepatitis B virus that can become chronic.",
    "symptoms": ["Abdominal pain", "Dark urine", "Fever", "Joint pain", "Jaundice", "Nausea and vomiting", "Weakness and fatigue", "Loss of appetite"],
    "precautions": ["Get vaccinated", "Use condoms", "Don't share needles", "Don't share personal items (razors, toothbrushes)", "Get tested"],
    "when_to_seek_care": ["Jaundice", "Severe fatigue", "Abdominal swelling", "Confusion", "Vomiting blood"],
    "sources": [{"title": "WHO – Hepatitis B", "url": "https://www.who.int/news-room/fact-sheets/detail/hepatitis-b"}],
    "confidence": "high"
  },
  "hepatitis C": {
    "keywords": ["hepatitis C", "HCV", "chronic hepatitis", "liver cirrhosis"],
    "summary": "A viral infection causing liver inflammation, often becoming chronic.",
    "symptoms": ["Fatigue", "Jaundice", "Dark urine", "Nausea", "Muscle and joint pain", "Itching", "Spider-like blood vessels on skin"],
    "precautions": ["Don't share needles", "Get tested", "Avoid sharing personal hygiene items", "Practice safe sex", "Antiviral treatment if diagnosed"],
    "when_to_seek_care": ["Jaundice", "Abdominal swelling", "Confusion", "Vomiting blood", "Sudden weight loss"],
    "sources": [{"title": "CDC – Hepatitis C", "url": "https://www.cdc.gov/hepatitis/hcv/index.htm"}],
    "confidence": "high"
  },
  "celiac disease": {
    "keywords": ["celiac", "gluten intolerance", "gluten sensitivity", "celiac sprue"],
    "summary": "An autoimmune disorder where gluten triggers immune damage to the small intestine.",
    "symptoms": ["Diarrhea", "Bloating and gas", "Abdominal pain", "Fatigue", "Weight loss", "Anemia", "Skin rash (dermatitis herpetiformis)", "Mouth sores", "Bone pain"],
    "precautions": ["Strictly avoid gluten (wheat, barley, rye)", "Read food labels carefully", "Use separate cooking utensils", "Notify restaurants of condition", "Take nutritional supplements"],
    "when_to_seek_care": ["Symptoms persist despite gluten-free diet", "Severe malnutrition", "Neurological symptoms", "Severe diarrhea with dehydration"],
    "sources": [{"title": "Mayo Clinic – Celiac Disease", "url": "https://www.mayoclinic.org/diseases-conditions/celiac-disease/symptoms-causes/syc-20352220"}],
    "confidence": "high"
  },
  "hypothyroidism": {
    "keywords": ["hypothyroidism", "underactive thyroid", "low thyroid", "thyroid deficiency"],
    "summary": "A condition where the thyroid gland doesn't produce enough thyroid hormone.",
    "symptoms": ["Fatigue and sluggishness", "Increased cold sensitivity", "Constipation", "Pale, dry skin", "Brittle nails", "Swollen face", "Hoarse voice", "Weight gain", "Depression", "Slow heart rate"],
    "precautions": ["Take thyroid hormone replacement as prescribed", "Regular thyroid function tests", "Avoid excessive iodine", "Take medications consistently", "Monitor symptoms"],
    "when_to_seek_care": ["Sudden worsening of symptoms", "Extreme fatigue", "Chest pain", "Confusion", "Myxedema symptoms"],
    "sources": [{"title": "Mayo Clinic – Hypothyroidism", "url": "https://www.mayoclinic.org/diseases-conditions/hypothyroidism/symptoms-causes/syc-20350284"}],
    "confidence": "high"
  },
  "hyperthyroidism": {
    "keywords": ["hyperthyroidism", "overactive thyroid", "Graves disease", "thyrotoxicosis"],
    "summary": "A condition where the thyroid gland produces too much thyroid hormone.",
    "symptoms": ["Unintentional weight loss", "Rapid heartbeat", "Irregular heartbeat", "Increased appetite", "Nervousness and anxiety", "Tremor", "Sweating", "Sensitivity to heat", "Goiter", "Fatigue"],
    "precautions": ["Take prescribed antithyroid medications", "Avoid excessive iodine", "Protect eyes if Graves' disease", "Regular monitoring", "Limit stress"],
    "when_to_seek_care": ["Thyroid storm symptoms", "Rapid irregular heartbeat", "High fever", "Severe weakness", "Confusion"],
    "sources": [{"title": "Mayo Clinic – Hyperthyroidism", "url": "https://www.mayoclinic.org/diseases-conditions/hyperthyroidism/symptoms-causes/syc-20373659"}],
    "confidence": "high"
  },
  "anemia": {
    "keywords": ["anemia", "anaemia", "low hemoglobin", "iron deficiency", "low blood count"],
    "summary": "A condition where you lack enough healthy red blood cells to carry adequate oxygen.",
    "symptoms": ["Fatigue and weakness", "Pale or yellowish skin", "Irregular heartbeat", "Shortness of breath", "Dizziness", "Chest pain", "Cold hands and feet", "Headaches"],
    "precautions": ["Eat iron-rich foods", "Take prescribed supplements", "Cook in cast iron pots", "Eat Vitamin C with iron-rich foods", "Treat underlying cause", "Regular blood tests"],
    "when_to_seek_care": ["Severe fatigue", "Chest pain", "Rapid heartbeat", "Shortness of breath at rest", "Yellowing of skin"],
    "sources": [{"title": "Mayo Clinic – Anemia", "url": "https://www.mayoclinic.org/diseases-conditions/anemia/symptoms-causes/syc-20351360"}],
    "confidence": "high"
  },
  "kidney stones": {
    "keywords": ["kidney stones", "renal calculi", "nephrolithiasis", "flank pain", "urolithiasis"],
    "summary": "Hard deposits of minerals and salts that form inside the kidneys.",
    "symptoms": ["Severe pain in back or side", "Pain radiating to lower abdomen", "Pain with urination", "Pink, red, or brown urine", "Nausea and vomiting", "Frequent urination", "Cloudy urine"],
    "precautions": ["Drink plenty of water (2+ liters/day)", "Limit salt and animal protein", "Avoid high-oxalate foods if prone", "Maintain healthy weight", "Take prescribed medications"],
    "when_to_seek_care": ["Severe pain", "Fever and chills with pain", "Blood in urine", "Difficulty urinating", "Nausea preventing fluid intake"],
    "sources": [{"title": "Mayo Clinic – Kidney Stones", "url": "https://www.mayoclinic.org/diseases-conditions/kidney-stones/symptoms-causes/syc-20355755"}],
    "confidence": "high"
  },
  "gout": {
    "keywords": ["gout", "uric acid", "gouty arthritis", "big toe pain", "podagra"],
    "summary": "A form of arthritis characterized by sudden, severe joint pain due to uric acid crystals.",
    "symptoms": ["Intense joint pain (often big toe)", "Inflammation and redness", "Swelling", "Warmth over joint", "Limited range of motion", "Lingering discomfort after acute pain"],
    "precautions": ["Limit purine-rich foods (red meat, seafood)", "Avoid alcohol", "Stay well hydrated", "Take prescribed medications", "Maintain healthy weight", "Elevate affected joint"],
    "when_to_seek_care": ["First attack of joint pain", "Fever with joint pain", "Joint appears infected", "Recurrent attacks", "Tophi (lumps under skin)"],
    "sources": [{"title": "Mayo Clinic – Gout", "url": "https://www.mayoclinic.org/diseases-conditions/gout/symptoms-causes/syc-20372897"}],
    "confidence": "high"
  },
  "rheumatoid arthritis": {
    "keywords": ["rheumatoid arthritis", "RA", "autoimmune arthritis", "joint inflammation"],
    "summary": "An autoimmune disease that causes joint inflammation and destruction.",
    "symptoms": ["Tender, warm, swollen joints", "Joint stiffness (worse in morning)", "Fatigue", "Fever", "Loss of appetite", "Symmetrical joint involvement", "Rheumatoid nodules"],
    "precautions": ["Take prescribed DMARDs", "Balance rest and activity", "Apply heat/cold therapy", "Gentle exercise", "Protect joints during activities"],
    "when_to_seek_care": ["Sudden worsening of symptoms", "New joint involvement", "Signs of infection", "Side effects from medications", "Respiratory symptoms"],
    "sources": [{"title": "Mayo Clinic – RA", "url": "https://www.mayoclinic.org/diseases-conditions/rheumatoid-arthritis/symptoms-causes/syc-20353648"}],
    "confidence": "high"
  },
  "osteoarthritis": {
    "keywords": ["osteoarthritis", "OA", "degenerative joint disease", "joint wear", "cartilage loss"],
    "summary": "Degeneration of joint cartilage causing pain and stiffness.",
    "symptoms": ["Joint pain during or after movement", "Stiffness (especially in morning)", "Tenderness", "Loss of flexibility", "Grating sensation", "Bone spurs", "Swelling"],
    "precautions": ["Exercise regularly (low-impact)", "Maintain healthy weight", "Use assistive devices", "Hot/cold therapy", "Take prescribed medications"],
    "when_to_seek_care": ["Severe joint pain", "Sudden increase in swelling", "Joint appears deformed", "Unable to perform daily activities"],
    "sources": [{"title": "Mayo Clinic – Osteoarthritis", "url": "https://www.mayoclinic.org/diseases-conditions/osteoarthritis/symptoms-causes/syc-20351925"}],
    "confidence": "high"
  },
  "psoriasis": {
    "keywords": ["psoriasis", "psoriatic", "scaly skin", "silvery plaques", "skin plaques"],
    "summary": "An immune condition causing rapid skin cell buildup resulting in scaling.",
    "symptoms": ["Red patches covered with thick, silvery scales", "Dry, cracked skin", "Itching, burning, soreness", "Thickened or ridged nails", "Swollen and stiff joints", "Scalp plaques"],
    "precautions": ["Moisturize daily", "Avoid triggers (stress, infections)", "Get moderate sun exposure", "Don't scratch lesions", "Take prescribed treatments"],
    "when_to_seek_care": ["Severe and widespread rash", "Joint pain with rash", "Fever with skin changes", "Rash not responding to treatment"],
    "sources": [{"title": "Mayo Clinic – Psoriasis", "url": "https://www.mayoclinic.org/diseases-conditions/psoriasis/symptoms-causes/syc-20355840"}],
    "confidence": "high"
  },
  "eczema": {
    "keywords": ["eczema", "atopic dermatitis", "atopic eczema", "itchy skin rash", "dry itchy skin"],
    "summary": "A condition causing itchy, inflamed, and irritated skin.",
    "symptoms": ["Dry skin", "Intense itching", "Red to brownish-gray patches", "Small raised bumps", "Thickened or cracked skin", "Swollen, raw skin from scratching"],
    "precautions": ["Moisturize twice daily", "Identify and avoid triggers", "Use mild soap", "Avoid scratching", "Wear soft fabrics", "Apply topical medications"],
    "when_to_seek_care": ["Signs of infection (pus, yellow crust)", "Sleep disruption", "Spreading rash", "Symptoms not responding to treatment"],
    "sources": [{"title": "Mayo Clinic – Eczema", "url": "https://www.mayoclinic.org/diseases-conditions/atopic-dermatitis-eczema/symptoms-causes/syc-20353273"}],
    "confidence": "high"
  },
  "acne": {
    "keywords": ["acne", "pimples", "blackheads", "whiteheads", "zits", "cystic acne"],
    "summary": "A skin condition that occurs when hair follicles become plugged with oil and dead skin cells.",
    "symptoms": ["Whiteheads", "Blackheads", "Small red tender bumps", "Pimples with pus", "Painful lumps under skin", "Scarring"],
    "precautions": ["Wash face twice daily", "Use non-comedogenic products", "Don't pick or squeeze pimples", "Change pillowcases frequently", "Use prescribed treatments"],
    "when_to_seek_care": ["Severe cystic acne", "Scarring", "Not responding to over-the-counter treatments", "Emotional distress from acne"],
    "sources": [{"title": "Mayo Clinic – Acne", "url": "https://www.mayoclinic.org/diseases-conditions/acne/symptoms-causes/syc-20368047"}],
    "confidence": "high"
  },
  "scabies": {
    "keywords": ["scabies", "itch mite", "Sarcoptes scabiei", "burrowing mite"],
    "summary": "A skin infestation caused by tiny mites that burrow into the skin.",
    "symptoms": ["Intense itching (worse at night)", "Pimple-like skin rash", "Thin burrow lines in skin", "Sores from scratching", "Common in finger webs, wrists, armpits"],
    "precautions": ["Use prescribed scabicide cream", "Wash all clothing and bedding", "Treat all household members", "Vacuum furniture", "Avoid close contact until treated"],
    "when_to_seek_care": ["Suspected scabies diagnosis", "Signs of secondary infection", "Symptoms not improving after treatment", "Norwegian/crusted scabies"],
    "sources": [{"title": "CDC – Scabies", "url": "https://www.cdc.gov/parasites/scabies/index.html"}],
    "confidence": "high"
  },
  "ringworm": {
    "keywords": ["ringworm", "tinea", "fungal skin infection", "dermatophytosis"],
    "summary": "A common fungal infection of the skin causing a ring-shaped rash.",
    "symptoms": ["Ring-shaped rash", "Redness", "Itching", "Scaly patches", "Hair loss in affected area (scalp)"],
    "precautions": ["Use antifungal cream", "Keep skin clean and dry", "Don't share personal items", "Wash hands after touching animals", "Change socks daily"],
    "when_to_seek_care": ["Scalp involvement", "Spreading despite treatment", "Nail involvement", "Immunocompromised patients"],
    "sources": [{"title": "CDC – Ringworm", "url": "https://www.cdc.gov/fungal/diseases/ringworm/index.html"}],
    "confidence": "high"
  },
  "hives": {
    "keywords": ["hives", "urticaria", "skin welts", "allergic rash", "raised itchy bumps"],
    "summary": "Raised, itchy welts on the skin, often caused by an allergic reaction.",
    "symptoms": ["Raised, itchy welts", "Red or skin-colored", "Blanch when pressed", "Varies in size and shape", "May merge into large patches", "Temporary swelling"],
    "precautions": ["Identify and avoid triggers", "Take antihistamines", "Apply cool compress", "Wear loose clothing", "Avoid hot showers"],
    "when_to_seek_care": ["Throat swelling or difficulty breathing", "Anaphylaxis symptoms", "Hives lasting more than 6 weeks", "Severe discomfort"],
    "sources": [{"title": "Mayo Clinic – Hives", "url": "https://www.mayoclinic.org/diseases-conditions/chronic-hives/symptoms-causes/syc-20352220"}],
    "confidence": "high"
  },
  "anaphylaxis": {
    "keywords": ["anaphylaxis", "anaphylactic shock", "severe allergic reaction", "epinephrine"],
    "summary": "A severe, life-threatening allergic reaction requiring emergency treatment.",
    "symptoms": ["Skin reactions (hives, flushing)", "Throat tightening", "Difficulty breathing", "Rapid, weak pulse", "Nausea and vomiting", "Dizziness or fainting", "Low blood pressure"],
    "precautions": ["Carry epinephrine auto-injector", "Wear medical alert bracelet", "Avoid known allergens", "Have action plan", "Inform others about allergy"],
    "when_to_seek_care": ["EMERGENCY – Call 911 immediately", "ANY suspected anaphylaxis", "Use epinephrine auto-injector immediately"],
    "sources": [{"title": "Mayo Clinic – Anaphylaxis", "url": "https://www.mayoclinic.org/diseases-conditions/anaphylaxis/symptoms-causes/syc-20351468"}],
    "confidence": "high"
  },
  "epilepsy": {
    "keywords": ["epilepsy", "seizure disorder", "convulsions", "fits", "grand mal"],
    "summary": "A neurological disorder in which brain activity becomes abnormal, causing seizures.",
    "symptoms": ["Seizures (convulsions)", "Temporary confusion", "Staring spell", "Uncontrollable jerking movements", "Loss of consciousness", "Fear or anxiety before seizure"],
    "precautions": ["Take anticonvulsant medications consistently", "Avoid seizure triggers", "Don't drive until seizure-free", "Wear medical alert bracelet", "Never swim alone"],
    "when_to_seek_care": ["Seizure lasting more than 5 minutes", "Second seizure within 24 hours", "First-ever seizure", "Seizure in water", "Injury during seizure"],
    "sources": [{"title": "Mayo Clinic – Epilepsy", "url": "https://www.mayoclinic.org/diseases-conditions/epilepsy/symptoms-causes/syc-20350093"}],
    "confidence": "high"
  },
  "Parkinson's disease": {
    "keywords": ["Parkinson's", "Parkinson's disease", "tremor resting", "bradykinesia", "shuffling gait"],
    "summary": "A progressive nervous system disorder affecting movement.",
    "symptoms": ["Tremor at rest", "Slowed movement (bradykinesia)", "Rigid muscles", "Impaired posture", "Shuffling gait", "Speech changes", "Writing changes", "Loss of facial expression"],
    "precautions": ["Take medications as prescribed", "Physical and occupational therapy", "Exercise regularly", "Fall prevention strategies", "Speech therapy if needed"],
    "when_to_seek_care": ["Rapid progression of symptoms", "Falls", "Swallowing difficulties", "Hallucinations", "Severe behavioral changes"],
    "sources": [{"title": "Mayo Clinic – Parkinson's", "url": "https://www.mayoclinic.org/diseases-conditions/parkinsons-disease/symptoms-causes/syc-20376055"}],
    "confidence": "high"
  },
  "Alzheimer's disease": {
    "keywords": ["Alzheimer's", "dementia", "memory loss", "cognitive decline", "forgetfulness"],
    "summary": "A progressive disease that destroys memory and cognitive function.",
    "symptoms": ["Memory loss disrupting daily life", "Confusion", "Difficulty with familiar tasks", "Language problems", "Disorientation", "Poor judgment", "Mood and personality changes", "Withdrawal"],
    "precautions": ["Seek early diagnosis", "Establish daily routine", "Safety-proof the home", "Maintain social engagement", "Caregiver support", "Legal/financial planning"],
    "when_to_seek_care": ["Significant memory changes", "Getting lost in familiar places", "Personality changes", "Safety concerns"],
    "sources": [{"title": "Alzheimer's Association", "url": "https://www.alz.org/"}],
    "confidence": "high"
  },
  "multiple sclerosis": {
    "keywords": ["multiple sclerosis", "MS", "demyelination", "optic neuritis", "relapsing remitting"],
    "summary": "A disease that attacks the protective covering of nerve fibers in the central nervous system.",
    "symptoms": ["Numbness or weakness in limbs", "Partial or complete vision loss", "Prolonged double vision", "Tingling or pain", "Electric-shock sensations", "Tremor", "Fatigue", "Dizziness"],
    "precautions": ["Take prescribed disease-modifying therapies", "Avoid heat exposure", "Exercise regularly", "Manage stress", "Physical therapy"],
    "when_to_seek_care": ["New or worsening symptoms", "Vision loss", "Sudden weakness", "Bladder problems", "Cognitive changes"],
    "sources": [{"title": "National MS Society", "url": "https://www.nationalmssociety.org/"}],
    "confidence": "high"
  },
  "lupus": {
    "keywords": ["lupus", "SLE", "systemic lupus", "butterfly rash", "autoimmune lupus"],
    "summary": "An autoimmune disease where the immune system attacks its own tissues and organs.",
    "symptoms": ["Butterfly-shaped facial rash", "Fatigue", "Fever", "Joint pain and stiffness", "Skin lesions worsening with sun", "Shortness of breath", "Chest pain", "Dry eyes", "Headaches", "Memory loss"],
    "precautions": ["Avoid sun exposure (use sunscreen)", "Take prescribed medications", "Rest during flares", "Regular medical monitoring", "Vaccinations as recommended"],
    "when_to_seek_care": ["Chest pain", "Shortness of breath", "Severe headache", "Confusion", "New rash", "Blood in urine"],
    "sources": [{"title": "Lupus Foundation of America", "url": "https://www.lupus.org/"}],
    "confidence": "high"
  },
  "endometriosis": {
    "keywords": ["endometriosis", "painful periods", "pelvic pain chronic", "dysmenorrhea"],
    "summary": "A disorder where tissue similar to uterine lining grows outside the uterus.",
    "symptoms": ["Painful periods", "Pelvic pain", "Pain during intercourse", "Excessive bleeding", "Infertility", "Pain with bowel movements", "Bloating", "Fatigue"],
    "precautions": ["Pain management as prescribed", "Hormonal therapy", "Regular gynecological checkups", "Laparoscopy if needed", "Support groups"],
    "when_to_seek_care": ["Severe pelvic pain", "Inability to manage pain", "Fertility concerns", "New or changing symptoms"],
    "sources": [{"title": "Mayo Clinic – Endometriosis", "url": "https://www.mayoclinic.org/diseases-conditions/endometriosis/symptoms-causes/syc-20354656"}],
    "confidence": "high"
  },
  "polycystic ovary syndrome": {
    "keywords": ["PCOS", "polycystic ovary", "irregular periods", "ovarian cysts", "androgen excess"],
    "summary": "A hormonal disorder causing enlarged ovaries with small cysts.",
    "symptoms": ["Irregular periods", "Excess androgen (facial hair, acne)", "Polycystic ovaries", "Weight gain", "Thinning hair", "Pelvic pain", "Difficulty getting pregnant", "Dark skin patches"],
    "precautions": ["Maintain healthy weight", "Exercise regularly", "Take prescribed hormonal medications", "Monitor blood sugar", "Regular gynecological checkups"],
    "when_to_seek_care": ["Irregular or absent periods", "Fertility concerns", "Severe symptoms", "Signs of insulin resistance"],
    "sources": [{"title": "Mayo Clinic – PCOS", "url": "https://www.mayoclinic.org/diseases-conditions/pcos/symptoms-causes/syc-20353439"}],
    "confidence": "high"
  },
  "fibromyalgia": {
    "keywords": ["fibromyalgia", "widespread pain", "tender points", "fibromyalgia syndrome"],
    "summary": "A disorder characterized by widespread musculoskeletal pain, fatigue, and mood issues.",
    "symptoms": ["Widespread muscle pain", "Fatigue", "Sleep problems", "Cognitive difficulties (fibro fog)", "Headaches", "Depression", "Anxiety", "Irritable bowel symptoms", "Painful tender points"],
    "precautions": ["Regular low-impact exercise", "Improve sleep habits", "Stress management", "Medications as prescribed", "Cognitive behavioral therapy"],
    "when_to_seek_care": ["Sudden severe pain", "New neurological symptoms", "Significant functional impairment", "Severe depression"],
    "sources": [{"title": "Mayo Clinic – Fibromyalgia", "url": "https://www.mayoclinic.org/diseases-conditions/fibromyalgia/symptoms-causes/syc-20354780"}],
    "confidence": "high"
  },
  "chronic kidney disease": {
    "keywords": ["chronic kidney disease", "CKD", "renal failure", "kidney disease", "kidney failure"],
    "summary": "A gradual loss of kidney function over time.",
    "symptoms": ["Nausea", "Vomiting", "Fatigue", "Frequent urination", "Decreased urine output", "Swelling in legs and ankles", "Shortness of breath", "Chest pain", "High blood pressure"],
    "precautions": ["Control blood pressure and blood sugar", "Limit protein and salt intake", "Take prescribed medications", "Avoid NSAIDs", "Regular kidney function tests", "Stay hydrated"],
    "when_to_seek_care": ["Sudden decrease in urine output", "Severe swelling", "Difficulty breathing", "Chest pain", "Confusion"],
    "sources": [{"title": "Mayo Clinic – CKD", "url": "https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521"}],
    "confidence": "high"
  },
  "gallstones": {
    "keywords": ["gallstones", "cholelithiasis", "gallbladder pain", "biliary colic"],
    "summary": "Hardened deposits that form in the gallbladder.",
    "symptoms": ["Sudden severe pain in upper right abdomen", "Pain radiating to right shoulder or back", "Nausea and vomiting", "Fever and chills (if infected)", "Jaundice", "Clay-colored stools"],
    "precautions": ["Eat a healthy diet", "Maintain healthy weight", "Avoid rapid weight loss", "Take prescribed medications"],
    "when_to_seek_care": ["Severe abdominal pain", "Jaundice", "Fever with chills and abdominal pain", "Pain lasting more than 5 hours"],
    "sources": [{"title": "Mayo Clinic – Gallstones", "url": "https://www.mayoclinic.org/diseases-conditions/gallstones/symptoms-causes/syc-20354214"}],
    "confidence": "high"
  },
  "pancreatitis": {
    "keywords": ["pancreatitis", "pancreatic pain", "upper abdominal pain radiating back"],
    "summary": "Inflammation of the pancreas causing severe abdominal pain.",
    "symptoms": ["Upper abdominal pain radiating to back", "Pain worsening after eating", "Fever", "Rapid pulse", "Nausea and vomiting", "Tenderness when abdomen touched", "Oily stools"],
    "precautions": ["Stop alcohol intake", "Follow low-fat diet", "Stay hydrated", "Treat underlying cause", "Hospitalization may be needed"],
    "when_to_seek_care": ["Severe abdominal pain", "Fever with abdominal pain", "Persistent vomiting", "Jaundice", "Rapid heart rate"],
    "sources": [{"title": "Mayo Clinic – Pancreatitis", "url": "https://www.mayoclinic.org/diseases-conditions/pancreatitis/symptoms-causes/syc-20360233"}],
    "confidence": "high"
  },
  "peptic ulcer": {
    "keywords": ["peptic ulcer", "stomach ulcer", "gastric ulcer", "duodenal ulcer", "H. pylori"],
    "summary": "Open sores in the lining of the stomach or small intestine.",
    "symptoms": ["Burning stomach pain", "Pain improved by eating (duodenal) or worsened (gastric)", "Nausea", "Feeling full quickly", "Bloating", "Heartburn", "Dark or bloody stools"],
    "precautions": ["Avoid NSAIDs and aspirin", "Avoid alcohol and smoking", "Eat smaller meals", "Limit spicy foods", "Complete antibiotic course if H. pylori+"],
    "when_to_seek_care": ["Blood in stool or vomit", "Dark or black stools", "Severe sudden abdominal pain", "Unexpected weight loss"],
    "sources": [{"title": "Mayo Clinic – Peptic Ulcer", "url": "https://www.mayoclinic.org/diseases-conditions/peptic-ulcer/symptoms-causes/syc-20354223"}],
    "confidence": "high"
  },
  "Crohn's disease": {
    "keywords": ["Crohn's disease", "Crohn disease", "inflammatory bowel disease", "IBD", "terminal ileum"],
    "summary": "A chronic inflammatory bowel disease affecting the lining of the digestive tract.",
    "symptoms": ["Diarrhea", "Abdominal pain and cramping", "Blood in stool", "Mouth sores", "Reduced appetite and weight loss", "Fatigue", "Fever", "Anal fissures", "Fistulas"],
    "precautions": ["Take prescribed medications", "Follow dietary recommendations", "Manage stress", "Regular medical follow-up", "Quit smoking"],
    "when_to_seek_care": ["Blood in stool", "Severe abdominal pain", "Fever", "Inability to eat or drink", "Sudden worsening"],
    "sources": [{"title": "Mayo Clinic – Crohn's", "url": "https://www.mayoclinic.org/diseases-conditions/crohns-disease/symptoms-causes/syc-20353304"}],
    "confidence": "high"
  },
  "ulcerative colitis": {
    "keywords": ["ulcerative colitis", "UC", "colitis", "inflammatory colitis", "bloody diarrhea"],
    "summary": "An inflammatory bowel disease causing ulcers in the colon and rectum.",
    "symptoms": ["Bloody diarrhea", "Abdominal pain", "Rectal pain", "Urgency to defecate", "Inability to defecate despite urgency", "Weight loss", "Fatigue", "Fever"],
    "precautions": ["Take prescribed medications", "Follow a suitable diet", "Manage stress", "Regular colonoscopies", "Watch for colorectal cancer signs"],
    "when_to_seek_care": ["Severe bleeding", "High fever", "Rapid heart rate", "Severe abdominal pain", "Signs of toxic megacolon"],
    "sources": [{"title": "Mayo Clinic – Ulcerative Colitis", "url": "https://www.mayoclinic.org/diseases-conditions/ulcerative-colitis/symptoms-causes/syc-20353326"}],
    "confidence": "high"
  },
  "cystic fibrosis": {
    "keywords": ["cystic fibrosis", "CF", "mucoviscidosis", "CFTR"],
    "summary": "A genetic disorder that causes severe damage to lungs and digestive system.",
    "symptoms": ["Persistent cough with thick mucus", "Frequent lung infections", "Wheezing", "Breathlessness", "Poor weight gain", "Salty skin", "Frequent greasy stools", "Clubbed fingers"],
    "precautions": ["Airway clearance therapy", "Enzyme replacement", "Medications as prescribed", "Nutrition management", "Regular pulmonary function tests"],
    "when_to_seek_care": ["Worsening breathing", "Signs of lung infection", "Poor weight gain", "Hemoptysis"],
    "sources": [{"title": "Cystic Fibrosis Foundation", "url": "https://www.cff.org/"}],
    "confidence": "high"
  },
  "sickle cell disease": {
    "keywords": ["sickle cell", "sickle cell anemia", "HbS", "vaso-occlusive crisis"],
    "summary": "A group of blood disorders where red blood cells take an abnormal sickle shape.",
    "symptoms": ["Pain crises", "Anemia", "Swelling of hands and feet", "Frequent infections", "Delayed growth", "Vision problems", "Stroke symptoms"],
    "precautions": ["Stay hydrated", "Avoid extreme temperatures", "Take prescribed medications", "Penicillin prophylaxis in children", "Regular medical checkups"],
    "when_to_seek_care": ["Severe pain crisis", "Stroke symptoms", "High fever", "Priapism", "Chest syndrome symptoms"],
    "sources": [{"title": "CDC – Sickle Cell Disease", "url": "https://www.cdc.gov/ncbddd/sicklecell/index.html"}],
    "confidence": "high"
  },
  "deep vein thrombosis": {
    "keywords": ["DVT", "deep vein thrombosis", "blood clot leg", "pulmonary embolism", "leg swelling"],
    "summary": "A blood clot forming in a deep vein, usually in the legs.",
    "symptoms": ["Leg swelling", "Leg pain or cramping", "Red or discolored skin", "Warmth in affected leg", "Swollen leg veins", "Shortness of breath (if PE)"],
    "precautions": ["Move legs during long travel", "Stay hydrated", "Compression stockings", "Take prescribed anticoagulants", "Avoid prolonged immobility"],
    "when_to_seek_care": ["Sudden chest pain with shortness of breath (PE emergency)", "Coughing blood", "Severe leg swelling", "Severe leg pain"],
    "sources": [{"title": "CDC – DVT", "url": "https://www.cdc.gov/ncbddd/dvt/index.html"}],
    "confidence": "high"
  },
  "osteoporosis": {
    "keywords": ["osteoporosis", "bone density loss", "brittle bones", "fragility fracture"],
    "summary": "A disease in which bones become brittle and fragile from loss of tissue.",
    "symptoms": ["Often no symptoms until fracture", "Back pain", "Loss of height", "Stooped posture", "Bone fracture from minor stress"],
    "precautions": ["Adequate calcium and Vitamin D", "Weight-bearing exercise", "Quit smoking", "Limit alcohol", "Take prescribed medications", "Fall prevention"],
    "when_to_seek_care": ["Any fracture from minor fall", "Sudden severe back pain", "Loss of height", "Bone pain"],
    "sources": [{"title": "NOF – Osteoporosis", "url": "https://www.bonehealthandosteoporosis.org/"}],
    "confidence": "high"
  },
  "sleep apnea": {
    "keywords": ["sleep apnea", "obstructive sleep apnea", "snoring", "CPAP", "breathing stops during sleep"],
    "summary": "A serious sleep disorder where breathing repeatedly stops and starts.",
    "symptoms": ["Loud snoring", "Episodes of stopped breathing", "Gasping for air during sleep", "Dry mouth in morning", "Headache in morning", "Difficulty sleeping", "Excessive daytime sleepiness", "Difficulty concentrating"],
    "precautions": ["Use CPAP as prescribed", "Maintain healthy weight", "Avoid alcohol and sedatives", "Sleep on side", "Regular sleep schedule"],
    "when_to_seek_care": ["Observed apnea episodes", "Severe daytime sleepiness", "High blood pressure from sleep apnea", "Frequent waking"],
    "sources": [{"title": "Mayo Clinic – Sleep Apnea", "url": "https://www.mayoclinic.org/diseases-conditions/sleep-apnea/symptoms-causes/syc-20377631"}],
    "confidence": "high"
  },
  "bipolar disorder": {
    "keywords": ["bipolar disorder", "bipolar", "manic depression", "mania", "mood swings"],
    "summary": "A mental health condition causing extreme mood swings including emotional highs (mania) and lows (depression).",
    "symptoms": ["Periods of extreme elevated mood (mania)", "Periods of depression", "Decreased need for sleep", "Racing thoughts", "Grandiosity", "Risky behavior", "Irritability"],
    "precautions": ["Take mood stabilizers as prescribed", "Maintain regular sleep", "Avoid alcohol and drugs", "Regular psychiatric follow-up", "Mood tracking"],
    "when_to_seek_care": ["Severe manic episode", "Suicidal thoughts", "Psychosis", "Inability to function", "Rapid cycling"],
    "sources": [{"title": "NIMH – Bipolar Disorder", "url": "https://www.nimh.nih.gov/health/topics/bipolar-disorder"}],
    "confidence": "high"
  },
  "schizophrenia": {
    "keywords": ["schizophrenia", "psychosis", "hallucinations", "delusions", "thought disorder"],
    "summary": "A serious mental disorder affecting how a person thinks, feels, and behaves.",
    "symptoms": ["Hallucinations (hearing voices)", "Delusions", "Disorganized thinking", "Abnormal motor behavior", "Negative symptoms (flat affect, avolition)", "Social withdrawal"],
    "precautions": ["Take antipsychotic medications", "Regular psychiatric care", "Psychosocial therapy", "Family support", "Avoid triggers"],
    "when_to_seek_care": ["First psychotic episode", "Danger to self or others", "Inability to care for self", "Medication non-compliance"],
    "sources": [{"title": "NIMH – Schizophrenia", "url": "https://www.nimh.nih.gov/health/topics/schizophrenia"}],
    "confidence": "high"
  },
  "ADHD": {
    "keywords": ["ADHD", "attention deficit", "hyperactivity", "attention deficit hyperactivity disorder", "ADD"],
    "summary": "A neurodevelopmental disorder marked by inattention, hyperactivity, and impulsivity.",
    "symptoms": ["Inattention", "Hyperactivity", "Impulsivity", "Difficulty following instructions", "Forgetfulness", "Loses things often", "Easily distracted", "Fidgeting"],
    "precautions": ["Medication as prescribed", "Behavioral therapy", "Structured routines", "Educational accommodations", "Exercise regularly"],
    "when_to_seek_care": ["Significant impairment in school or work", "Symptoms causing safety concerns", "Co-occurring depression or anxiety"],
    "sources": [{"title": "CDC – ADHD", "url": "https://www.cdc.gov/ncbddd/adhd/index.html"}],
    "confidence": "high"
  },
  "autism spectrum disorder": {
    "keywords": ["autism", "ASD", "autistic", "Asperger", "autism spectrum"],
    "summary": "A developmental disorder affecting communication and behavior.",
    "symptoms": ["Difficulty with social interaction", "Communication challenges", "Repetitive behaviors", "Restricted interests", "Sensory sensitivities", "Developmental delays"],
    "precautions": ["Early intervention therapy", "Behavioral therapy (ABA)", "Speech therapy", "Structured environment", "Family support"],
    "when_to_seek_care": ["Developmental regression", "Safety concerns", "Severe behavioral issues", "Mental health concerns"],
    "sources": [{"title": "CDC – Autism", "url": "https://www.cdc.gov/ncbddd/autism/index.html"}],
    "confidence": "high"
  },
  "chickenpox": {
    "keywords": ["chickenpox", "varicella", "pox blisters", "itchy blisters"],
    "summary": "A highly contagious viral infection causing an itchy blister rash.",
    "symptoms": ["Itchy blister rash", "Fever", "Fatigue", "Loss of appetite", "Headache"],
    "precautions": ["Isolate until blisters crust", "Calamine lotion", "Oatmeal baths", "Get vaccinated"],
    "when_to_seek_care": ["Rash near eyes", "High fever", "Difficulty breathing", "Bacterial infection"],
    "sources": [{"title": "CDC – Chickenpox", "url": "https://www.cdc.gov/chickenpox/index.html"}],
    "confidence": "high"
  },
  "shingles": {
    "keywords": ["shingles", "herpes zoster", "zoster", "painful rash one side", "post-herpetic neuralgia"],
    "summary": "A viral infection causing a painful rash, caused by the same virus as chickenpox.",
    "symptoms": ["Pain, burning, or tingling", "Sensitivity to touch", "Red rash (appearing days after pain)", "Fluid-filled blisters", "Itching", "Fever", "Headache", "Fatigue"],
    "precautions": ["Antiviral medications (start early)", "Pain management", "Keep rash clean and covered", "Avoid contact with those not immune", "Get shingles vaccine"],
    "when_to_seek_care": ["Rash near eye", "Widespread rash", "High fever", "Neurological symptoms", "Immunocompromised"],
    "sources": [{"title": "CDC – Shingles", "url": "https://www.cdc.gov/shingles/index.html"}],
    "confidence": "high"
  },
  "mumps": {
    "keywords": ["mumps", "parotitis", "swollen parotid glands", "salivary gland swelling"],
    "summary": "A contagious viral illness characterized by swollen salivary glands.",
    "symptoms": ["Swollen, painful parotid glands", "Difficulty chewing or swallowing", "Fever", "Headache", "Muscle aches", "Fatigue", "Loss of appetite"],
    "precautions": ["Get MMR vaccine", "Rest and fluids", "Isolate during illness", "Apply warm or cold compress to glands"],
    "when_to_seek_care": ["Testicular pain (orchitis)", "Severe headache and stiff neck (meningitis)", "Hearing loss", "High fever"],
    "sources": [{"title": "CDC – Mumps", "url": "https://www.cdc.gov/mumps/index.html"}],
    "confidence": "high"
  },
  "whooping cough": {
    "keywords": ["whooping cough", "pertussis", "Bordetella pertussis", "severe coughing fits"],
    "summary": "A highly contagious respiratory tract infection known for a severe coughing fit.",
    "symptoms": ["Runny nose", "Mild fever", "Mild cough progressing to severe coughing fits", "Vomiting after coughing", "'Whoop' sound on inhalation", "Exhaustion after coughing"],
    "precautions": ["Get Tdap vaccine", "Antibiotics if prescribed", "Rest", "Small frequent meals", "Avoid cough triggers"],
    "when_to_seek_care": ["Infants – seek care immediately", "Coughing turning lips blue", "Difficulty breathing", "Vomiting after coughing"],
    "sources": [{"title": "CDC – Pertussis", "url": "https://www.cdc.gov/pertussis/index.html"}],
    "confidence": "high"
  },
  "tetanus": {
    "keywords": ["tetanus", "lockjaw", "Clostridium tetani", "muscle spasms jaw"],
    "summary": "A serious bacterial infection causing muscle stiffness and spasms.",
    "symptoms": ["Jaw stiffness or cramps (lockjaw)", "Muscle spasms", "Difficulty swallowing", "Fever and sweating", "Changes in blood pressure and heart rate", "Neck stiffness"],
    "precautions": ["Get tetanus vaccine (Td booster every 10 years)", "Wound care after injury", "Seek medical care for deep wounds"],
    "when_to_seek_care": ["ANY suspected tetanus – emergency", "Jaw stiffness after wound", "Muscle spasms"],
    "sources": [{"title": "CDC – Tetanus", "url": "https://www.cdc.gov/tetanus/index.html"}],
    "confidence": "high"
  },
  "rabies": {
    "keywords": ["rabies", "animal bite", "hydrophobia", "lyssavirus"],
    "summary": "A deadly viral disease transmitted through the saliva of infected animals.",
    "symptoms": ["Fever", "Headache", "Agitation", "Confusion", "Hydrophobia (fear of water)", "Partial paralysis", "Hallucinations", "Excessive salivation"],
    "precautions": ["Seek immediate medical care after animal bite", "Rabies post-exposure prophylaxis", "Vaccinate pets", "Avoid wildlife contact"],
    "when_to_seek_care": ["ANY animal bite – seek care immediately for rabies evaluation", "Symptoms after animal bite"],
    "sources": [{"title": "CDC – Rabies", "url": "https://www.cdc.gov/rabies/index.html"}],
    "confidence": "high"
  },
  "lyme disease": {
    "keywords": ["Lyme disease", "tick bite", "Borrelia", "bullseye rash", "erythema migrans"],
    "summary": "A bacterial infection spread by infected blacklegged ticks.",
    "symptoms": ["Bull's-eye rash (erythema migrans)", "Fever", "Chills", "Fatigue", "Body aches", "Headache", "Stiff neck", "Joint swelling", "Facial palsy (later)"],
    "precautions": ["Remove ticks promptly", "Use tick repellent", "Wear long clothing in wooded areas", "Check for ticks after outdoor activities", "Take prescribed antibiotics"],
    "when_to_seek_care": ["Bull's-eye rash after tick bite", "Fever after tick bite", "Neurological symptoms", "Joint swelling"],
    "sources": [{"title": "CDC – Lyme Disease", "url": "https://www.cdc.gov/lyme/index.html"}],
    "confidence": "high"
  },
  "meningitis": {
    "keywords": ["meningitis", "meningococcal", "stiff neck fever", "nuchal rigidity", "brain membrane infection"],
    "summary": "Inflammation of the membranes surrounding the brain and spinal cord.",
    "symptoms": ["Sudden high fever", "Severe headache", "Stiff neck", "Nausea and vomiting", "Photophobia", "Rash (with meningococcal)", "Altered mental status", "Seizures"],
    "precautions": ["Get meningitis vaccine", "Seek immediate medical care if suspected", "Complete antibiotic course"],
    "when_to_seek_care": ["EMERGENCY – Call 911 for suspected meningitis", "High fever + stiff neck + headache", "Petechial rash", "Altered consciousness"],
    "sources": [{"title": "CDC – Meningitis", "url": "https://www.cdc.gov/meningitis/index.html"}],
    "confidence": "high"
  },
  "sepsis": {
    "keywords": ["sepsis", "blood poisoning", "systemic infection", "septic shock"],
    "summary": "A life-threatening response to infection that can lead to organ failure.",
    "symptoms": ["High fever or abnormally low body temperature", "Rapid heart rate", "Rapid breathing", "Confusion or disorientation", "Extreme pain", "Clammy or sweaty skin", "Low blood pressure"],
    "precautions": ["EMERGENCY – seek immediate care", "Prevent infections (hygiene, vaccines)", "Treat infections promptly"],
    "when_to_seek_care": ["ANY suspected sepsis – call 911", "Rapid deterioration with infection", "Extreme temperature + confusion + rapid heart rate"],
    "sources": [{"title": "CDC – Sepsis", "url": "https://www.cdc.gov/sepsis/index.html"}],
    "confidence": "high"
  },
  "food allergy": {
    "keywords": ["food allergy", "peanut allergy", "nut allergy", "shellfish allergy", "allergic to food"],
    "summary": "An immune system reaction that occurs after eating a certain food.",
    "symptoms": ["Tingling in mouth", "Hives or skin rash", "Swelling of lips, face, tongue", "Wheezing", "Nasal congestion", "Abdominal pain", "Diarrhea", "Nausea", "Dizziness"],
    "precautions": ["Strictly avoid trigger foods", "Read labels carefully", "Carry epinephrine auto-injector", "Inform restaurants", "Wear medical alert bracelet"],
    "when_to_seek_care": ["Anaphylaxis signs – use epinephrine and call 911", "Throat swelling", "Difficulty breathing", "Severe vomiting after eating"],
    "sources": [{"title": "FARE – Food Allergies", "url": "https://www.foodallergy.org/"}],
    "confidence": "high"
  },
  "lactose intolerance": {
    "keywords": ["lactose intolerance", "lactose", "dairy intolerance", "milk intolerance"],
    "summary": "Inability to fully digest lactose (sugar in milk) due to low lactase enzyme.",
    "symptoms": ["Diarrhea", "Gas", "Bloating", "Abdominal cramps", "Nausea", "Symptoms 30 minutes to 2 hours after dairy"],
    "precautions": ["Limit dairy products", "Use lactose-free products", "Take lactase enzyme supplements", "Read food labels"],
    "when_to_seek_care": ["Severe symptoms", "Blood in stool", "Weight loss", "Ruling out IBD"],
    "sources": [{"title": "Mayo Clinic – Lactose Intolerance", "url": "https://www.mayoclinic.org/diseases-conditions/lactose-intolerance/symptoms-causes/syc-20374232"}],
    "confidence": "high"
  },
  "obesity": {
    "keywords": ["obesity", "overweight", "BMI over 30", "excess weight", "morbid obesity"],
    "summary": "A complex disease involving an excessive amount of body fat.",
    "symptoms": ["BMI of 30 or higher", "Shortness of breath with activity", "Joint pain", "Excessive sweating", "Sleep apnea", "Skin problems", "Fatigue"],
    "precautions": ["Healthy balanced diet", "Regular physical activity", "Behavioral changes", "Medical management if needed", "Treat underlying causes"],
    "when_to_seek_care": ["BMI over 40", "Obesity-related health problems", "Metabolic syndrome", "Mental health impact"],
    "sources": [{"title": "CDC – Obesity", "url": "https://www.cdc.gov/obesity/index.html"}],
    "confidence": "high"
  },
  "malnutrition": {
    "keywords": ["malnutrition", "undernutrition", "nutrient deficiency", "starvation"],
    "summary": "Deficiencies, excesses, or imbalances in nutrient intake.",
    "symptoms": ["Unintended weight loss", "Fatigue", "Muscle weakness", "Poor wound healing", "Impaired immunity", "Hair loss", "Dry skin", "Swollen abdomen (kwashiorkor)", "Growth failure"],
    "precautions": ["Ensure adequate caloric and nutrient intake", "Nutritional supplements", "Treat underlying conditions", "Regular nutritional assessments"],
    "when_to_seek_care": ["Severe weight loss", "Extreme weakness", "Swelling", "Children with growth failure", "Inability to eat"],
    "sources": [{"title": "WHO – Malnutrition", "url": "https://www.who.int/news-room/fact-sheets/detail/malnutrition"}],
    "confidence": "high"
  },
  "vitamin D deficiency": {
    "keywords": ["vitamin D deficiency", "Vit D", "hypovitaminosis D", "rickets"],
    "summary": "Insufficient vitamin D levels affecting bone health and immune function.",
    "symptoms": ["Fatigue", "Bone pain", "Muscle weakness", "Mood changes", "Frequent infections", "Back pain", "Depression", "Hair loss", "Slow wound healing"],
    "precautions": ["Get sunlight exposure", "Eat vitamin D-rich foods", "Take supplements if recommended", "Regular blood tests"],
    "when_to_seek_care": ["Severe bone pain", "Muscle weakness affecting function", "Rickets in children", "Osteomalacia"],
    "sources": [{"title": "NIH – Vitamin D", "url": "https://ods.od.nih.gov/factsheets/VitaminD-Consumer/"}],
    "confidence": "high"
  },
  "iron deficiency": {
    "keywords": ["iron deficiency", "low iron", "iron deficiency anemia", "ferritin low"],
    "summary": "Insufficient iron levels, the most common cause of anemia worldwide.",
    "symptoms": ["Extreme fatigue", "Pale skin", "Weakness", "Shortness of breath", "Headache", "Dizziness", "Cold hands/feet", "Brittle nails", "Cravings for non-food items (pica)"],
    "precautions": ["Eat iron-rich foods (red meat, leafy greens, legumes)", "Vitamin C with iron foods", "Take supplements if prescribed", "Cook in cast iron", "Treat bleeding causes"],
    "when_to_seek_care": ["Severe fatigue affecting function", "Chest pain", "Rapid heartbeat", "Unexplained iron deficiency"],
    "sources": [{"title": "Mayo Clinic – Iron Deficiency Anemia", "url": "https://www.mayoclinic.org/diseases-conditions/iron-deficiency-anemia/symptoms-causes/syc-20355034"}],
    "confidence": "high"
  },
  "vitamin B12 deficiency": {
    "keywords": ["B12 deficiency", "vitamin B12", "cobalamin", "pernicious anemia", "megaloblastic anemia"],
    "summary": "Low levels of vitamin B12 affecting nerve function and red blood cell production.",
    "symptoms": ["Fatigue and weakness", "Numbness or tingling in hands/feet", "Balance problems", "Memory problems", "Pale or jaundiced skin", "Glossitis (inflamed tongue)", "Depression", "Vision disturbances"],
    "precautions": ["Eat B12-rich foods (meat, fish, dairy)", "Take supplements", "B12 injections if absorption problem", "Treat underlying conditions"],
    "when_to_seek_care": ["Neurological symptoms", "Severe anemia", "Memory or cognitive changes", "Balance problems"],
    "sources": [{"title": "NIH – Vitamin B12", "url": "https://ods.od.nih.gov/factsheets/VitaminB12-Consumer/"}],
    "confidence": "high"
  },
  "carpal tunnel syndrome": {
    "keywords": ["carpal tunnel", "wrist pain numbness", "median nerve compression", "hand tingling"],
    "summary": "Pressure on the median nerve in the wrist causing pain and numbness.",
    "symptoms": ["Numbness or tingling in hand/fingers", "Weak grip", "Wrist pain", "Pain radiating up the arm", "Shock-like sensations", "Clumsiness with fine motor tasks", "Symptoms worse at night"],
    "precautions": ["Wrist splints especially at night", "Ergonomic modifications", "Take breaks from repetitive tasks", "Stretch exercises", "Anti-inflammatory medications"],
    "when_to_seek_care": ["Persistent numbness", "Muscle wasting in thumb", "Weakness affecting function", "Symptoms not responding to conservative treatment"],
    "sources": [{"title": "Mayo Clinic – Carpal Tunnel", "url": "https://www.mayoclinic.org/diseases-conditions/carpal-tunnel-syndrome/symptoms-causes/syc-20355603"}],
    "confidence": "high"
  },
  "vertigo": {
    "keywords": ["vertigo", "BPPV", "dizziness spinning", "room spinning", "benign paroxysmal positional vertigo"],
    "summary": "A sensation of spinning or motion when you are not actually moving.",
    "symptoms": ["Spinning sensation", "Loss of balance", "Nausea and vomiting", "Abnormal eye movements", "Headache", "Sweating", "Ringing in the ear"],
    "precautions": ["Epley maneuver for BPPV", "Move slowly", "Avoid sudden position changes", "Anti-nausea medication", "Rest during attacks"],
    "when_to_seek_care": ["Sudden severe vertigo", "Vertigo with neurological symptoms", "Hearing loss", "Double vision", "Difficulty walking"],
    "sources": [{"title": "Mayo Clinic – Vertigo", "url": "https://www.mayoclinic.org/symptoms/dizziness/basics/causes/sym-20050788"}],
    "confidence": "high"
  },
  "tinnitus": {
    "keywords": ["tinnitus", "ringing in ears", "ear ringing", "buzzing in ears"],
    "summary": "Ringing, buzzing, or other sounds in one or both ears with no external source.",
    "symptoms": ["Ringing in ears", "Buzzing", "Roaring", "Clicking", "Hissing", "Humming", "Difficulty concentrating", "Sleep disturbances"],
    "precautions": ["Protect hearing from loud noises", "Reduce stress", "Sound masking devices", "Hearing aids if hearing loss present", "Limit alcohol and caffeine"],
    "when_to_seek_care": ["Sudden tinnitus", "Tinnitus in one ear only", "Associated hearing loss", "Pulsatile tinnitus", "Tinnitus with dizziness"],
    "sources": [{"title": "Mayo Clinic – Tinnitus", "url": "https://www.mayoclinic.org/diseases-conditions/tinnitus/symptoms-causes/syc-20350156"}],
    "confidence": "high"
  },
  "glaucoma": {
    "keywords": ["glaucoma", "intraocular pressure", "optic nerve damage", "peripheral vision loss"],
    "summary": "A group of eye conditions that damage the optic nerve, often due to elevated eye pressure.",
    "symptoms": ["Gradual peripheral vision loss", "Tunnel vision (advanced)", "Sudden eye pain (acute)", "Headache", "Nausea and vomiting (acute)", "Blurred vision", "Halos around lights"],
    "precautions": ["Regular eye exams", "Use prescribed eye drops", "Protect eyes from injury", "Inform family members (hereditary)"],
    "when_to_seek_care": ["Sudden eye pain and vision changes", "Emergency if acute angle-closure glaucoma", "Significant vision loss", "Side effects from eye drops"],
    "sources": [{"title": "NEI – Glaucoma", "url": "https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/glaucoma"}],
    "confidence": "high"
  },
  "cataracts": {
    "keywords": ["cataracts", "cloudy lens", "vision clouding", "cataract surgery"],
    "summary": "A clouding of the eye's natural lens causing vision impairment.",
    "symptoms": ["Clouded or blurred vision", "Increasing difficulty with night vision", "Sensitivity to light", "Halos around lights", "Frequent changes in glasses prescription", "Fading of colors", "Double vision"],
    "precautions": ["Protect eyes from UV rays", "Regular eye exams", "Manage diabetes", "Avoid smoking", "Surgical correction when needed"],
    "when_to_seek_care": ["Significant vision impairment affecting function", "Sudden vision changes", "Double vision", "Driving becoming unsafe"],
    "sources": [{"title": "NEI – Cataracts", "url": "https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/cataracts"}],
    "confidence": "high"
  },
  "macular degeneration": {
    "keywords": ["macular degeneration", "AMD", "age-related macular", "central vision loss"],
    "summary": "A disease causing deterioration of the central portion of the retina.",
    "symptoms": ["Blurred central vision", "Difficulty recognizing faces", "Need for increased light", "Difficulty reading fine print", "Straight lines appearing wavy", "Blind spot in central vision"],
    "precautions": ["Quit smoking", "Eat leafy greens and fish", "Wear UV-protective sunglasses", "Regular eye exams after 50", "Take AREDS supplements if recommended"],
    "when_to_seek_care": ["Sudden vision change", "Central vision loss", "New distortions in vision"],
    "sources": [{"title": "NEI – AMD", "url": "https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/age-related-macular-degeneration"}],
    "confidence": "high"
  },
  "prostate enlargement": {
    "keywords": ["BPH", "benign prostatic hyperplasia", "enlarged prostate", "prostate enlargement", "urinary hesitancy"],
    "summary": "Non-cancerous enlargement of the prostate gland common in older men.",
    "symptoms": ["Frequent urination", "Urgency to urinate", "Weak urine stream", "Dribbling after urination", "Incomplete bladder emptying", "Difficulty starting urination", "Nocturia (waking to urinate)"],
    "precautions": ["Limit fluids before bed", "Avoid antihistamines and decongestants", "Regular monitoring", "Take prescribed alpha-blockers", "Limit alcohol and caffeine"],
    "when_to_seek_care": ["Inability to urinate", "Blood in urine", "Painful urination", "Urinary tract infection", "Kidney problems"],
    "sources": [{"title": "Mayo Clinic – BPH", "url": "https://www.mayoclinic.org/diseases-conditions/benign-prostatic-hyperplasia/symptoms-causes/syc-20370087"}],
    "confidence": "high"
  },
  "erectile dysfunction": {
    "keywords": ["erectile dysfunction", "ED", "impotence", "sexual dysfunction male"],
    "summary": "The inability to get or keep an erection firm enough for sexual intercourse.",
    "symptoms": ["Trouble getting an erection", "Trouble keeping an erection", "Reduced sexual desire"],
    "precautions": ["Address underlying conditions (diabetes, hypertension)", "Limit alcohol", "Don't smoke", "Exercise regularly", "Discuss treatment options with doctor"],
    "when_to_seek_care": ["Concerns about erections", "Associated with heart disease risk factors", "Psychological impact", "Symptoms starting abruptly"],
    "sources": [{"title": "Mayo Clinic – Erectile Dysfunction", "url": "https://www.mayoclinic.org/diseases-conditions/erectile-dysfunction/symptoms-causes/syc-20355776"}],
    "confidence": "high"
  },
  "menopause": {
    "keywords": ["menopause", "perimenopause", "hot flashes", "irregular periods", "climacteric"],
    "summary": "Natural biological process marking the end of menstrual cycles.",
    "symptoms": ["Irregular periods", "Hot flashes", "Chills", "Night sweats", "Sleep problems", "Mood changes", "Dry skin", "Vaginal dryness", "Slowed metabolism", "Thinning hair"],
    "precautions": ["Hormone therapy if recommended", "Vaginal lubricants", "Calcium and Vitamin D supplementation", "Regular exercise", "Healthy diet"],
    "when_to_seek_care": ["Severe hot flashes affecting quality of life", "Vaginal bleeding after menopause", "Severe mood changes", "Symptoms affecting function"],
    "sources": [{"title": "Mayo Clinic – Menopause", "url": "https://www.mayoclinic.org/diseases-conditions/menopause/symptoms-causes/syc-20353397"}],
    "confidence": "high"
  },
  "preeclampsia": {
    "keywords": ["preeclampsia", "eclampsia", "pregnancy hypertension", "HELLP syndrome", "high BP pregnancy"],
    "summary": "A pregnancy complication characterized by high blood pressure and organ damage.",
    "symptoms": ["High blood pressure after 20 weeks", "Excess protein in urine", "Severe headache", "Vision changes", "Upper abdominal pain", "Swelling in face and hands", "Reduced urine output"],
    "precautions": ["Regular prenatal care", "Monitor blood pressure", "Low-dose aspirin if recommended", "Limit activity if advised"],
    "when_to_seek_care": ["High BP during pregnancy", "Severe headache in pregnancy", "Sudden face/hand swelling", "Vision changes", "Abdominal pain in pregnancy"],
    "sources": [{"title": "Mayo Clinic – Preeclampsia", "url": "https://www.mayoclinic.org/diseases-conditions/preeclampsia/symptoms-causes/syc-20355745"}],
    "confidence": "high"
  },
  "gestational diabetes": {
    "keywords": ["gestational diabetes", "pregnancy diabetes", "glucose intolerance pregnancy"],
    "summary": "High blood sugar that develops during pregnancy.",
    "symptoms": ["Often no symptoms", "Increased thirst", "Frequent urination", "Fatigue", "Blurred vision (sometimes)"],
    "precautions": ["Monitor blood sugar", "Follow diabetic diet", "Exercise regularly", "Insulin if needed", "Regular prenatal checkups"],
    "when_to_seek_care": ["Blood sugar not controlled with diet", "Signs of complications in baby", "Extreme thirst or urination"],
    "sources": [{"title": "CDC – Gestational Diabetes", "url": "https://www.cdc.gov/diabetes/basics/gestational.html"}],
    "confidence": "high"
  },
  "hernia": {
    "keywords": ["hernia", "inguinal hernia", "umbilical hernia", "abdominal hernia", "bulge abdomen"],
    "summary": "When an internal organ pushes through a weak spot in the surrounding muscle or tissue.",
    "symptoms": ["Visible bulge", "Discomfort or pain (especially when bending or lifting)", "Feeling of heaviness", "Heartburn (hiatal hernia)", "Difficulty swallowing (hiatal hernia)", "Groin pain"],
    "precautions": ["Avoid heavy lifting", "Maintain healthy weight", "Treat chronic cough or constipation", "Surgical repair when indicated"],
    "when_to_seek_care": ["Sudden severe pain", "Bulge becomes hard, tender, or discolored", "Nausea and vomiting", "Fever", "Strangulated hernia"],
    "sources": [{"title": "Mayo Clinic – Hernia", "url": "https://www.mayoclinic.org/diseases-conditions/inguinal-hernia/symptoms-causes/syc-20351547"}],
    "confidence": "high"
  },
  "hemorrhoids": {
    "keywords": ["hemorrhoids", "piles", "rectal bleeding", "anal itching", "anal pain"],
    "summary": "Swollen veins in the rectum or anus causing pain and bleeding.",
    "symptoms": ["Painless bleeding during bowel movements", "Itching or irritation in anal region", "Pain or discomfort", "Swelling around anus", "Leakage of feces"],
    "precautions": ["Eat high-fiber diet", "Drink plenty of fluids", "Don't strain on toilet", "Exercise regularly", "Use sitz baths", "Topical treatments"],
    "when_to_seek_care": ["Significant rectal bleeding", "Severe pain", "Protruding hemorrhoid not reducible", "Symptoms not improving"],
    "sources": [{"title": "Mayo Clinic – Hemorrhoids", "url": "https://www.mayoclinic.org/diseases-conditions/hemorrhoids/symptoms-causes/syc-20360268"}],
    "confidence": "high"
  },
  "back pain": {
    "keywords": ["back pain", "lower back pain", "lumbar pain", "sciatica", "herniated disc"],
    "summary": "Pain or discomfort in the back, ranging from mild aching to severe pain.",
    "symptoms": ["Muscle ache", "Stabbing or shooting pain", "Pain radiating down the leg (sciatica)", "Limited flexibility or range of motion", "Inability to stand up straight", "Pain worsening with bending/lifting"],
    "precautions": ["Stay active as tolerated", "Apply ice or heat", "Improve posture", "Strengthen core muscles", "Use ergonomic furniture", "Take prescribed pain relievers"],
    "when_to_seek_care": ["Bladder or bowel dysfunction", "Leg weakness or numbness", "Fever with back pain", "Pain after trauma", "Progressive worsening"],
    "sources": [{"title": "Mayo Clinic – Back Pain", "url": "https://www.mayoclinic.org/diseases-conditions/back-pain/symptoms-causes/syc-20369906"}],
    "confidence": "high"
  },
  "neck pain": {
    "keywords": ["neck pain", "cervical pain", "stiff neck", "cervicalgia", "neck stiffness"],
    "summary": "Pain in the neck often caused by muscle tension, arthritis, or injury.",
    "symptoms": ["Neck ache or stiffness", "Pain worsening with holding head in one position", "Muscle tightness and spasms", "Decreased ability to move head", "Headache", "Pain radiating to shoulders or arms"],
    "precautions": ["Maintain good posture", "Take regular breaks from screens", "Use supportive pillow", "Gentle stretches", "Apply heat or cold", "Ergonomic workspace"],
    "when_to_seek_care": ["Neck pain after trauma", "Radiating pain with numbness", "Fever with stiff neck", "Weakness in arms", "Severe sudden pain"],
    "sources": [{"title": "Mayo Clinic – Neck Pain", "url": "https://www.mayoclinic.org/diseases-conditions/neck-pain/symptoms-causes/syc-20375581"}],
    "confidence": "high"
  },
  "shoulder pain": {
    "keywords": ["shoulder pain", "rotator cuff", "frozen shoulder", "shoulder impingement", "shoulder injury"],
    "summary": "Pain in the shoulder region from various causes including rotator cuff issues.",
    "symptoms": ["Pain in shoulder joint", "Restricted range of motion", "Swelling or tenderness", "Pain worsening at night", "Weakness in arm", "Clicking or popping sensation"],
    "precautions": ["Rest affected shoulder", "Ice therapy", "Physical therapy", "Avoid overhead activities", "Anti-inflammatory medications"],
    "when_to_seek_care": ["Trauma-related shoulder injury", "Sudden severe pain", "Deformity", "Unable to move arm", "Fever with shoulder pain"],
    "sources": [{"title": "Mayo Clinic – Shoulder Pain", "url": "https://www.mayoclinic.org/symptoms/shoulder-pain/basics/when-to-see-doctor/sym-20050696"}],
    "confidence": "medium"
  },
  "knee pain": {
    "keywords": ["knee pain", "knee injury", "patellofemoral", "meniscus", "ACL", "knee swelling"],
    "summary": "Pain in the knee joint from injury, arthritis, or overuse.",
    "symptoms": ["Knee pain", "Swelling", "Stiffness", "Redness and warmth", "Weakness or instability", "Popping or crunching sensation", "Inability to fully extend/flex knee"],
    "precautions": ["RICE (Rest, Ice, Compress, Elevate)", "Physical therapy", "Maintain healthy weight", "Strengthen surrounding muscles", "Use knee brace if needed"],
    "when_to_seek_care": ["Severe pain", "Knee locked in position", "Significant swelling after injury", "Deformity", "Inability to bear weight"],
    "sources": [{"title": "Mayo Clinic – Knee Pain", "url": "https://www.mayoclinic.org/diseases-conditions/knee-pain/symptoms-causes/syc-20350849"}],
    "confidence": "medium"
  },
  "plantar fasciitis": {
    "keywords": ["plantar fasciitis", "heel pain", "morning heel pain", "foot pain bottom"],
    "summary": "Inflammation of the thick band of tissue that runs across the bottom of the foot.",
    "symptoms": ["Stabbing heel pain (worst in morning)", "Pain after long periods of standing", "Pain after exercise", "Heel tenderness", "Foot stiffness"],
    "precautions": ["Stretching exercises", "Supportive footwear", "Avoid walking barefoot on hard surfaces", "Ice therapy", "Night splints"],
    "when_to_seek_care": ["Severe pain affecting mobility", "Swelling or bruising", "Not improving after weeks", "Fever with foot pain"],
    "sources": [{"title": "Mayo Clinic – Plantar Fasciitis", "url": "https://www.mayoclinic.org/diseases-conditions/plantar-fasciitis/symptoms-causes/syc-20354846"}],
    "confidence": "high"
  },
  "tennis elbow": {
    "keywords": ["tennis elbow", "lateral epicondylitis", "elbow pain outside", "forearm pain"],
    "summary": "A painful condition involving the tendons that join the forearm muscles to the elbow.",
    "symptoms": ["Outer elbow pain and tenderness", "Pain worsening with gripping", "Weak grip strength", "Forearm aching", "Morning stiffness"],
    "precautions": ["Rest from aggravating activities", "Ice therapy", "Counterforce brace", "Physical therapy", "Modify grip technique"],
    "when_to_seek_care": ["Severe pain", "Not improving in 6-12 weeks", "Night pain", "Nerve symptoms"],
    "sources": [{"title": "Mayo Clinic – Tennis Elbow", "url": "https://www.mayoclinic.org/diseases-conditions/tennis-elbow/symptoms-causes/syc-20351987"}],
    "confidence": "high"
  },
  "herpes simplex": {
    "keywords": ["herpes simplex", "cold sores", "genital herpes", "HSV", "oral herpes"],
    "summary": "A viral infection causing sores around the mouth or genitals.",
    "symptoms": ["Painful sores or blisters (oral or genital)", "Itching or tingling before sores appear", "Flu-like symptoms with first episode", "Ulcers", "Scabs when healing"],
    "precautions": ["Antiviral medications", "Avoid contact when sores present", "Use condoms", "Don't share utensils or lip products", "Inform partners"],
    "when_to_seek_care": ["Genital herpes diagnosis", "Eye herpes", "Severe outbreaks", "Immunocompromised with herpes", "Herpes in newborn"],
    "sources": [{"title": "CDC – Herpes", "url": "https://www.cdc.gov/std/herpes/default.htm"}],
    "confidence": "high"
  },
  "chlamydia": {
    "keywords": ["chlamydia", "Chlamydia trachomatis", "STI", "STD", "genital discharge"],
    "summary": "A common sexually transmitted infection caused by Chlamydia trachomatis bacteria.",
    "symptoms": ["Often no symptoms", "Unusual discharge", "Burning on urination", "Pelvic pain (women)", "Testicular pain (men)", "Rectal symptoms"],
    "precautions": ["Use condoms", "Regular STI screening", "Notify partners", "Complete antibiotic treatment", "Retest 3 months after treatment"],
    "when_to_seek_care": ["Symptoms of STI", "Positive screening test", "Pelvic inflammatory disease symptoms", "Partner diagnosed"],
    "sources": [{"title": "CDC – Chlamydia", "url": "https://www.cdc.gov/std/chlamydia/default.htm"}],
    "confidence": "high"
  },
  "gonorrhea": {
    "keywords": ["gonorrhea", "gonorrhoea", "Neisseria gonorrhoeae", "STI gonorrhea", "clap"],
    "summary": "A sexually transmitted bacterial infection affecting genitals, rectum, and throat.",
    "symptoms": ["Painful urination", "Pus-like discharge", "Pelvic or abdominal pain (women)", "Testicular pain (men)", "Rectal discharge or pain", "Often no symptoms"],
    "precautions": ["Use condoms", "Regular STI testing", "Complete antibiotic treatment", "Notify partners"],
    "when_to_seek_care": ["Discharge from genitals", "Positive test", "Partner diagnosed", "Pelvic inflammatory disease"],
    "sources": [{"title": "CDC – Gonorrhea", "url": "https://www.cdc.gov/std/gonorrhea/default.htm"}],
    "confidence": "high"
  },
  "syphilis": {
    "keywords": ["syphilis", "Treponema pallidum", "STI syphilis", "chancre", "secondary syphilis"],
    "summary": "A bacterial sexually transmitted infection progressing through stages.",
    "symptoms": ["Stage 1: painless sore (chancre)", "Stage 2: rash (palms/soles), flu-like", "Latent: no symptoms", "Stage 3: organ damage", "Congenital if untreated in pregnancy"],
    "precautions": ["Use condoms", "Regular testing", "Penicillin treatment", "Notify partners", "Prenatal screening"],
    "when_to_seek_care": ["Any suspicious sore", "Unexplained rash", "Positive test", "Neurological symptoms in late stage"],
    "sources": [{"title": "CDC – Syphilis", "url": "https://www.cdc.gov/std/syphilis/default.htm"}],
    "confidence": "high"
  },
  "post-traumatic stress disorder": {
    "keywords": ["PTSD", "post-traumatic stress", "trauma", "flashbacks", "nightmares trauma"],
    "summary": "A mental health condition triggered by experiencing or witnessing a traumatic event.",
    "symptoms": ["Intrusive memories or flashbacks", "Nightmares", "Severe emotional distress to triggers", "Avoidance behavior", "Negative thoughts", "Emotional numbness", "Hypervigilance", "Sleep disturbances", "Irritability or anger outbursts"],
    "precautions": ["Seek professional trauma therapy", "Take prescribed medications", "Build support network", "Practice grounding techniques", "Avoid substance use"],
    "when_to_seek_care": ["Symptoms lasting more than a month", "Thoughts of self-harm", "Substance abuse", "Inability to function"],
    "sources": [{"title": "NIMH – PTSD", "url": "https://www.nimh.nih.gov/health/topics/post-traumatic-stress-disorder-ptsd"}],
    "confidence": "high"
  },
  "obsessive-compulsive disorder": {
    "keywords": ["OCD", "obsessive compulsive", "obsessions", "compulsions", "intrusive thoughts"],
    "summary": "A disorder featuring unreasonable thoughts (obsessions) and repetitive behaviors (compulsions).",
    "symptoms": ["Persistent, intrusive thoughts", "Fear of contamination", "Doubt and needing reassurance", "Symmetry obsessions", "Compulsive cleaning", "Counting or checking rituals", "Significant time consumed by obsessions/compulsions"],
    "precautions": ["CBT (cognitive-behavioral therapy)", "Exposure and response prevention (ERP)", "Take prescribed SSRIs", "Avoid reassurance-seeking", "Join support groups"],
    "when_to_seek_care": ["Obsessions/compulsions taking over 1 hour/day", "Significant distress", "Affecting work or relationships", "Suicidal thoughts"],
    "sources": [{"title": "NIMH – OCD", "url": "https://www.nimh.nih.gov/health/topics/obsessive-compulsive-disorder-ocd"}],
    "confidence": "high"
  },
  "eating disorders": {
    "keywords": ["anorexia", "bulimia", "eating disorder", "binge eating", "restrictive eating"],
    "summary": "Serious conditions related to persistent eating behaviors that negatively impact health.",
    "symptoms": ["Extreme restriction of food", "Obsessive concern about weight/body", "Binge eating followed by purging", "Use of laxatives or excessive exercise", "Distorted body image", "Physical complications (malnutrition, electrolyte imbalance)"],
    "precautions": ["Seek specialized eating disorder treatment", "Nutritional rehabilitation", "Psychotherapy (CBT, DBT)", "Medical monitoring", "Family-based treatment"],
    "when_to_seek_care": ["Medical instability", "Fainting", "Severe restriction", "Electrolyte imbalances", "Heart palpitations", "Suicidal thoughts"],
    "sources": [{"title": "NEDA – Eating Disorders", "url": "https://www.nationaleatingdisorders.org/"}],
    "confidence": "high"
  },
  "insomnia": {
    "keywords": ["insomnia", "sleep problems", "sleeplessness", "can't sleep", "difficulty falling asleep"],
    "summary": "A sleep disorder making it hard to fall or stay asleep.",
    "symptoms": ["Difficulty falling asleep", "Waking during the night", "Waking too early", "Not feeling rested", "Daytime tiredness", "Irritability", "Difficulty concentrating or remembering", "Increased errors or accidents"],
    "precautions": ["Maintain consistent sleep schedule", "Create comfortable sleep environment", "Limit caffeine and alcohol", "Avoid screens before bed", "Relaxation techniques", "CBT for insomnia (CBT-I)"],
    "when_to_seek_care": ["Insomnia lasting more than 3 months", "Significant daytime impairment", "Associated with depression or anxiety", "Suspected sleep apnea"],
    "sources": [{"title": "Mayo Clinic – Insomnia", "url": "https://www.mayoclinic.org/diseases-conditions/insomnia/symptoms-causes/syc-20355167"}],
    "confidence": "high"
  },
  "restless legs syndrome": {
    "keywords": ["restless legs", "RLS", "Willis-Ekbom disease", "creepy crawly legs sensation"],
    "summary": "A nervous system disorder causing an irresistible urge to move the legs.",
    "symptoms": ["Unpleasant sensations in legs", "Strong urge to move legs", "Symptoms worse at night or at rest", "Temporary relief from movement", "Sleep disruption", "Daytime fatigue"],
    "precautions": ["Regular exercise (not too close to bedtime)", "Good sleep hygiene", "Avoid caffeine and alcohol", "Iron supplementation if deficient", "Take prescribed medications"],
    "when_to_seek_care": ["Symptoms affecting sleep quality", "Symptoms during daytime", "RLS spreading to arms"],
    "sources": [{"title": "Mayo Clinic – RLS", "url": "https://www.mayoclinic.org/diseases-conditions/restless-legs-syndrome/symptoms-causes/syc-20377168"}],
    "confidence": "high"
  },
  "Bell's palsy": {
    "keywords": ["Bell's palsy", "facial palsy", "facial weakness sudden", "facial nerve paralysis"],
    "summary": "Sudden weakness or paralysis of muscles on one side of the face.",
    "symptoms": ["Sudden one-sided facial weakness or paralysis", "Drooping on one side", "Drooling", "Difficulty closing eye", "Altered taste", "Increased tear or saliva production", "Headache"],
    "precautions": ["Eye protection (patch/lubricating drops)", "Corticosteroids if prescribed early", "Antiviral medications", "Facial massage", "Protect cornea"],
    "when_to_seek_care": ["Seek care within 72 hours of onset for best outcomes", "Any new facial weakness", "Eye problems", "Severe pain"],
    "sources": [{"title": "Mayo Clinic – Bell's Palsy", "url": "https://www.mayoclinic.org/diseases-conditions/bells-palsy/symptoms-causes/syc-20370028"}],
    "confidence": "high"
  },
  "chronic fatigue syndrome": {
    "keywords": ["chronic fatigue syndrome", "CFS", "myalgic encephalomyelitis", "ME/CFS", "post-exertional malaise"],
    "summary": "A complex disorder characterized by extreme fatigue not improved by rest.",
    "symptoms": ["Extreme fatigue", "Sleep not refreshing", "Post-exertional malaise", "Cognitive impairment (brain fog)", "Orthostatic intolerance", "Muscle pain", "Joint pain", "Headaches", "Sore throat", "Enlarged lymph nodes"],
    "precautions": ["Pacing (avoid boom-bust cycle)", "Gentle activity within tolerance", "Sleep hygiene", "Symptom management", "Avoid overexertion"],
    "when_to_seek_care": ["Severe fatigue lasting 6+ months", "Significant functional impairment", "New neurological symptoms", "Worsening after illness"],
    "sources": [{"title": "CDC – ME/CFS", "url": "https://www.cdc.gov/me-cfs/index.html"}],
    "confidence": "high"
  },
  "alopecia": {
    "keywords": ["alopecia", "hair loss", "baldness", "androgenetic alopecia", "alopecia areata"],
    "summary": "Partial or complete loss of hair, from various causes.",
    "symptoms": ["Gradual thinning on top of head", "Circular or patchy bald spots", "Sudden loosening of hair", "Full-body hair loss", "Patches on the scalp or beard"],
    "precautions": ["Treat underlying medical causes", "Reduce stress", "Gentle hair care", "Topical minoxidil if appropriate", "Consider dermatology consultation"],
    "when_to_seek_care": ["Rapid or complete hair loss", "Associated with other symptoms (rash, fatigue)", "Significant psychological distress"],
    "sources": [{"title": "AAD – Hair Loss", "url": "https://www.aad.org/public/diseases/hair-loss/types/alopecia"}],
    "confidence": "medium"
  },
  "dandruff": {
    "keywords": ["dandruff", "seborrheic dermatitis", "flaky scalp", "scalp flaking"],
    "summary": "A skin condition causing flaking of the scalp skin.",
    "symptoms": ["White or yellow flakes on hair and shoulders", "Scalp itching", "Redness of scalp", "Greasy skin patches with white or yellowish scales"],
    "precautions": ["Use anti-dandruff shampoo", "Shampoo regularly", "Manage stress", "Avoid harsh hair products"],
    "when_to_seek_care": ["Severe scaling", "Spreading beyond scalp", "Intense itching", "Not responding to OTC treatment"],
    "sources": [{"title": "Mayo Clinic – Dandruff", "url": "https://www.mayoclinic.org/diseases-conditions/dandruff/symptoms-causes/syc-20353850"}],
    "confidence": "high"
  },
  "oral thrush": {
    "keywords": ["oral thrush", "oral candidiasis", "mouth yeast infection", "white patches mouth"],
    "summary": "A fungal infection (Candida) in the mouth or throat.",
    "symptoms": ["Creamy white lesions in mouth", "Slightly raised lesions", "Redness or soreness", "Difficulty swallowing", "Cotton-feeling in mouth", "Loss of taste"],
    "precautions": ["Antifungal medication", "Rinse mouth after using inhaled steroids", "Good oral hygiene", "Treat dentures", "Control diabetes"],
    "when_to_seek_care": ["Difficulty swallowing", "Spreading to esophagus", "Recurrent infections", "Immunocompromised"],
    "sources": [{"title": "Mayo Clinic – Oral Thrush", "url": "https://www.mayoclinic.org/diseases-conditions/oral-thrush/symptoms-causes/syc-20353533"}],
    "confidence": "high"
  },
  "tooth decay": {
    "keywords": ["tooth decay", "dental caries", "cavity", "cavities", "toothache"],
    "summary": "Damage to the tooth caused by bacteria producing acids from sugar.",
    "symptoms": ["Toothache", "Tooth sensitivity", "Visible holes or pits in teeth", "Brown, black, or white staining on tooth surface", "Pain when biting"],
    "precautions": ["Brush teeth twice daily with fluoride toothpaste", "Floss daily", "Limit sugary foods and drinks", "Regular dental checkups", "Dental sealants for children"],
    "when_to_seek_care": ["Toothache", "Sensitivity to hot/cold", "Visible decay", "Swelling around tooth", "Dental abscess"],
    "sources": [{"title": "Mayo Clinic – Cavities", "url": "https://www.mayoclinic.org/diseases-conditions/cavities/symptoms-causes/syc-20352892"}],
    "confidence": "high"
  },
  "gingivitis": {
    "keywords": ["gingivitis", "gum disease", "bleeding gums", "gum inflammation", "periodontitis"],
    "summary": "Inflammation of the gums, usually caused by plaque buildup.",
    "symptoms": ["Swollen or puffy gums", "Dusky red gums", "Gums that bleed easily", "Bad breath", "Receding gums", "Tender gums"],
    "precautions": ["Brush teeth twice daily", "Floss daily", "Use antiseptic mouthwash", "Regular dental cleanings", "Don't smoke"],
    "when_to_seek_care": ["Gums bleed consistently", "Persistent bad breath", "Loose teeth", "Painful gums", "Gum recession"],
    "sources": [{"title": "Mayo Clinic – Gingivitis", "url": "https://www.mayoclinic.org/diseases-conditions/gingivitis/symptoms-causes/syc-20354453"}],
    "confidence": "high"
  },
  "nausea": {
    "keywords": ["nausea", "feeling sick", "queasy", "upset stomach", "motion sickness"],
    "summary": "An unpleasant sensation in the stomach that may lead to vomiting.",
    "symptoms": ["Uneasy feeling in stomach", "Urge to vomit", "Sweating", "Dizziness", "Pallor", "Increased salivation"],
    "precautions": ["Eat small bland meals", "Sip fluids slowly", "Avoid greasy or spicy foods", "Fresh air", "Ginger tea or ginger candies", "Anti-nausea medication if needed"],
    "when_to_seek_care": ["Vomiting blood", "Severe abdominal pain", "Signs of dehydration", "Persistent vomiting more than 2 days", "Head injury with nausea"],
    "sources": [{"title": "Mayo Clinic – Nausea", "url": "https://www.mayoclinic.org/symptoms/nausea/basics/when-to-see-doctor/sym-20050736"}],
    "confidence": "medium"
  },
  "diarrhea": {
    "keywords": ["diarrhea", "loose stools", "watery stool", "runny stool", "bowel movement frequent"],
    "summary": "Loose, watery stools occurring more frequently than usual.",
    "symptoms": ["Loose or watery stools", "Abdominal cramps", "Abdominal pain", "Fever", "Blood in stool", "Bloating", "Nausea"],
    "precautions": ["Stay hydrated (oral rehydration solution)", "Eat bland foods (BRAT diet)", "Avoid dairy, fatty, high-fiber foods", "Wash hands frequently", "Probiotics may help"],
    "when_to_seek_care": ["Signs of dehydration", "Blood in stool", "Fever above 102°F", "Diarrhea lasting more than 3 days", "Severe abdominal pain"],
    "sources": [{"title": "Mayo Clinic – Diarrhea", "url": "https://www.mayoclinic.org/diseases-conditions/diarrhea/symptoms-causes/syc-20352669"}],
    "confidence": "medium"
  },
  "constipation": {
    "keywords": ["constipation", "infrequent bowel movements", "hard stools", "straining to defecate"],
    "summary": "Infrequent bowel movements or difficult passage of stools.",
    "symptoms": ["Fewer than 3 bowel movements per week", "Hard or lumpy stools", "Straining during bowel movements", "Feeling of blockage", "Feeling of incomplete emptying", "Abdominal discomfort"],
    "precautions": ["Increase dietary fiber", "Drink more water", "Exercise regularly", "Don't ignore urge to defecate", "Limit processed foods"],
    "when_to_seek_care": ["Blood in stool", "Constipation lasting more than 3 weeks", "Severe abdominal pain", "Unexplained weight loss", "New onset in older adults"],
    "sources": [{"title": "Mayo Clinic – Constipation", "url": "https://www.mayoclinic.org/diseases-conditions/constipation/symptoms-causes/syc-20354253"}],
    "confidence": "medium"
  },
  "fever": {
    "keywords": ["fever", "high temperature", "pyrexia", "febrile"],
    "summary": "A temporary increase in body temperature, usually due to illness.",
    "symptoms": ["Temperature above 38°C / 100.4°F", "Sweating", "Chills and shivering", "Headache", "Muscle aches", "Loss of appetite", "Irritability", "Dehydration", "General weakness"],
    "precautions": ["Rest", "Stay hydrated", "Take antipyretics (paracetamol/ibuprofen)", "Light clothing and cool environment", "Monitor temperature"],
    "when_to_seek_care": ["Fever above 103°F (39.4°C)", "Infants under 3 months with fever", "Fever lasting more than 3 days", "Fever with stiff neck or rash", "Confusion with fever"],
    "sources": [{"title": "Mayo Clinic – Fever", "url": "https://www.mayoclinic.org/diseases-conditions/fever/symptoms-causes/syc-20352759"}],
    "confidence": "medium"
  },
  "cough": {
    "keywords": ["cough", "dry cough", "wet cough", "persistent cough", "chronic cough"],
    "summary": "A reflex action to clear the throat and airways of mucus, irritants, or foreign material.",
    "symptoms": ["Dry or wet cough", "Sore throat", "Runny or stuffy nose", "Heartburn", "Postnasal drip", "Shortness of breath with cough"],
    "precautions": ["Identify and avoid cough triggers", "Stay hydrated", "Honey for soothing", "Elevate head when sleeping", "Treat underlying cause"],
    "when_to_seek_care": ["Coughing up blood", "Cough lasting more than 3 weeks", "Difficulty breathing", "Chest pain with cough", "Accompanied by high fever"],
    "sources": [{"title": "Mayo Clinic – Cough", "url": "https://www.mayoclinic.org/symptoms/cough/basics/when-to-see-doctor/sym-20050846"}],
    "confidence": "medium"
  },
  "fatigue": {
    "keywords": ["fatigue", "tiredness", "exhaustion", "chronic fatigue", "always tired"],
    "summary": "A feeling of persistent tiredness, weakness, or lack of energy.",
    "symptoms": ["Constant tiredness", "Lack of motivation", "Muscle weakness", "Difficulty concentrating", "Moodiness", "Headaches", "Dizziness"],
    "precautions": ["Get 7-9 hours of sleep", "Regular exercise", "Balanced diet", "Stay hydrated", "Limit alcohol and caffeine", "Manage stress"],
    "when_to_seek_care": ["Fatigue with chest pain", "Shortness of breath", "Significant unintentional weight loss", "Extreme fatigue lasting months", "Associated with depression or anxiety"],
    "sources": [{"title": "Mayo Clinic – Fatigue", "url": "https://www.mayoclinic.org/symptoms/fatigue/basics/when-to-see-doctor/sym-20050894"}],
    "confidence": "medium"
  },
  "headache": {
    "keywords": ["headache", "head pain", "tension headache", "cluster headache", "head pressure"],
    "summary": "Pain in any region of the head, with many possible causes.",
    "symptoms": ["Pressure or tightening sensation", "Dull aching head pain", "Tenderness in scalp, neck, and shoulder muscles", "One or both sides of head affected", "Sensitivity to light and sound"],
    "precautions": ["Rest in quiet, dark room", "Stay hydrated", "OTC pain relievers", "Cold or warm compress", "Manage stress triggers", "Regular sleep schedule"],
    "when_to_seek_care": ["Sudden severe headache (worst of life)", "Headache with fever and stiff neck", "Headache after head injury", "Progressive worsening", "Neurological symptoms"],
    "sources": [{"title": "Mayo Clinic – Headache", "url": "https://www.mayoclinic.org/symptoms/headache/basics/when-to-see-doctor/sym-20050800"}],
    "confidence": "medium"
  },
  "chest pain": {
    "keywords": ["chest pain", "chest tightness", "thoracic pain", "chest discomfort", "chest pressure"],
    "summary": "Pain or discomfort in the chest from various causes (cardiac and non-cardiac).",
    "symptoms": ["Pressure, fullness, or squeezing in chest", "Sharp stabbing pain", "Pain spreading to arm, neck, or jaw", "Difficulty breathing", "Cold sweat with pain", "Heartburn or sour taste"],
    "precautions": ["Always rule out cardiac causes first", "Do not ignore chest pain", "Call emergency services if suspected heart attack"],
    "when_to_seek_care": ["ANY chest pain – rule out heart attack immediately", "Chest pain with shortness of breath", "Pain spreading to arm or jaw", "Chest pain with nausea and sweat"],
    "sources": [{"title": "Mayo Clinic – Chest Pain", "url": "https://www.mayoclinic.org/symptoms/chest-pain/basics/when-to-see-doctor/sym-20050838"}],
    "confidence": "medium"
  },
  "shortness of breath": {
    "keywords": ["shortness of breath", "dyspnea", "breathlessness", "difficulty breathing", "can't breathe"],
    "summary": "An uncomfortable sensation of difficult or labored breathing.",
    "symptoms": ["Inability to get enough air", "Chest tightness", "Rapid breathing", "Labored breathing", "Gasping"],
    "precautions": ["Sit upright", "Calm breathing techniques", "Use inhaler if prescribed", "Avoid known triggers"],
    "when_to_seek_care": ["Sudden severe shortness of breath – call 911", "Shortness of breath at rest", "Associated with chest pain", "Bluish lips or fingernails", "After injury or trauma"],
    "sources": [{"title": "Mayo Clinic – Shortness of Breath", "url": "https://www.mayoclinic.org/symptoms/shortness-of-breath/basics/when-to-see-doctor/sym-20050890"}],
    "confidence": "medium"
  },
  "abdominal pain": {
    "keywords": ["abdominal pain", "stomach pain", "belly pain", "stomach ache", "tummy ache", "stomach cramps"],
    "summary": "Pain occurring anywhere in the abdomen, with many possible causes.",
    "symptoms": ["Pain anywhere in the abdomen", "Cramping", "Bloating", "Nausea", "Diarrhea", "Constipation", "Fever (with some causes)"],
    "precautions": ["Stay hydrated", "Eat bland foods", "Identify triggers", "Rest", "Avoid NSAIDs on empty stomach"],
    "when_to_seek_care": ["Severe sudden pain", "Fever with abdominal pain", "Blood in stool", "Vomiting blood", "Abdomen rigid or board-like", "Pain lasting more than 24 hours"],
    "sources": [{"title": "Mayo Clinic – Abdominal Pain", "url": "https://www.mayoclinic.org/symptoms/abdominal-pain/basics/when-to-see-doctor/sym-20050728"}],
    "confidence": "medium"
  },
  "weight loss unintentional": {
    "keywords": ["weight loss", "unintentional weight loss", "unexplained weight loss", "losing weight without trying"],
    "summary": "Unexplained or unintended weight loss without changing diet or exercise.",
    "symptoms": ["Losing 5%+ of body weight in 6-12 months without trying", "Fatigue", "Decreased appetite", "Muscle weakness"],
    "precautions": ["Track food intake", "Regular medical evaluation", "Rule out underlying conditions"],
    "when_to_seek_care": ["Significant unexplained weight loss", "Associated with cough, fever, or night sweats", "Blood in stool", "Abdominal pain"],
    "sources": [{"title": "Mayo Clinic – Weight Loss", "url": "https://www.mayoclinic.org/symptoms/unexplained-weight-loss/basics/when-to-see-doctor/sym-20050700"}],
    "confidence": "medium"
  },
  "swollen lymph nodes": {
    "keywords": ["swollen lymph nodes", "lymphadenopathy", "swollen glands", "enlarged lymph nodes"],
    "summary": "Swelling of lymph nodes, usually indicating an immune response.",
    "symptoms": ["Swollen, tender lumps under skin", "Commonly in neck, armpits, or groin", "Fever", "Night sweats", "Runny nose", "Sore throat", "Fatigue"],
    "precautions": ["Treat underlying infection", "Monitor for changes", "Rest and fluids", "Warm compress for comfort"],
    "when_to_seek_care": ["Hard, non-tender swollen nodes", "Growing for more than 2 weeks", "Night sweats and fever with swollen nodes", "Difficulty breathing or swallowing"],
    "sources": [{"title": "Mayo Clinic – Swollen Lymph Nodes", "url": "https://www.mayoclinic.org/diseases-conditions/swollen-lymph-nodes/symptoms-causes/syc-20353902"}],
    "confidence": "medium"
  },
  "nosebleed": {
    "keywords": ["nosebleed", "epistaxis", "bloody nose", "nasal bleeding"],
    "summary": "Bleeding from the inside of the nose.",
    "symptoms": ["Blood from one or both nostrils", "Blood draining down the back of the throat"],
    "precautions": ["Sit upright and lean slightly forward", "Pinch soft part of nose for 10-15 minutes", "Breathe through mouth", "Apply cold compress to nose bridge", "Don't tilt head back"],
    "when_to_seek_care": ["Heavy bleeding not stopping after 20 minutes", "Blood loss causing dizziness", "After head injury", "Blood-thinning medications", "Nosebleed with difficulty breathing"],
    "sources": [{"title": "Mayo Clinic – Nosebleed", "url": "https://www.mayoclinic.org/diseases-conditions/nosebleeds/symptoms-causes/syc-20353580"}],
    "confidence": "medium"
  },
  "allergic rhinitis": {
    "keywords": ["allergic rhinitis", "hay fever", "seasonal allergies", "pollen allergy", "dust allergy"],
    "summary": "An allergic response causing cold-like symptoms triggered by allergens.",
    "symptoms": ["Sneezing", "Runny or stuffy nose", "Itchy eyes, nose, or throat", "Watery, red, swollen eyes", "Postnasal drip", "Fatigue", "Headache"],
    "precautions": ["Avoid known allergens", "Check pollen counts", "Keep windows closed during high pollen", "Take antihistamines", "Nasal corticosteroid sprays", "Allergy testing and immunotherapy"],
    "when_to_seek_care": ["Symptoms not controlled with OTC medications", "Asthma worsening with allergies", "Recurrent sinus infections", "Considering immunotherapy"],
    "sources": [{"title": "AAAAI – Allergic Rhinitis", "url": "https://www.aaaai.org/tools-for-the-public/conditions-library/allergies/rhinitis"}],
    "confidence": "high"
  },
  "athlete's foot": {
    "keywords": ["athlete's foot", "tinea pedis", "foot fungus", "fungal foot infection", "itchy feet"],
    "summary": "A fungal infection affecting the skin on the feet.",
    "symptoms": ["Itching, stinging, burning between toes", "Blistering, peeling skin", "Dry skin on sole and side of foot", "Raw skin", "Discolored, thick, crumbly nails"],
    "precautions": ["Keep feet dry", "Wear moisture-wicking socks", "Don't walk barefoot in public areas", "Use antifungal powder", "Alternate shoes", "Use antifungal cream"],
    "when_to_seek_care": ["Spreading infection", "Secondary bacterial infection", "Diabetic with foot infection", "Not responding to treatment"],
    "sources": [{"title": "Mayo Clinic – Athlete's Foot", "url": "https://www.mayoclinic.org/diseases-conditions/athletes-foot/symptoms-causes/syc-20353841"}],
    "confidence": "high"
  },
  "nail fungus": {
    "keywords": ["nail fungus", "onychomycosis", "fungal nail", "yellow thick nails", "toenail fungus"],
    "summary": "A fungal infection that begins as a white or yellow-brown spot under nails.",
    "symptoms": ["Thickened nails", "Whitish to yellow-brown discoloration", "Brittle, crumbly, or ragged nails", "Distorted shape", "Dark color (debris under nail)", "Slightly foul smell"],
    "precautions": ["Keep nails trimmed and clean", "Wear breathable socks", "Antifungal nail treatments", "Don't share nail tools", "Wear sandals in public areas"],
    "when_to_seek_care": ["Spreading to other nails", "Diabetic patient with nail infection", "Pain from infected nail", "Prescription antifungal needed"],
    "sources": [{"title": "Mayo Clinic – Nail Fungus", "url": "https://www.mayoclinic.org/diseases-conditions/nail-fungus/symptoms-causes/syc-20353294"}],
    "confidence": "high"
  },
  "warts": {
    "keywords": ["warts", "verruca", "HPV skin wart", "plantar wart", "genital wart"],
    "summary": "Small, rough growths caused by the human papillomavirus (HPV).",
    "symptoms": ["Rough, grainy growth on skin", "Flesh-colored bump", "Tiny black dots (clotted blood vessels)", "Tender when pressed (plantar warts)", "Flat lesions (flat warts)"],
    "precautions": ["Avoid touching warts and then other body areas", "Don't share towels", "Wear sandals in public showers", "Use OTC treatments", "HPV vaccine for genital warts"],
    "when_to_seek_care": ["Wart on face or genitals", "Painful wart", "Not responding to OTC treatment", "Rapidly multiplying", "Immunocompromised patient"],
    "sources": [{"title": "Mayo Clinic – Warts", "url": "https://www.mayoclinic.org/diseases-conditions/common-warts/symptoms-causes/syc-20371125"}],
    "confidence": "high"
  },
  "cold sore": {
    "keywords": ["cold sore", "fever blister", "oral herpes", "lip sore", "HSV1"],
    "summary": "Fluid-filled blisters near the mouth caused by HSV-1 virus.",
    "symptoms": ["Tingling or burning before blister appears", "Fluid-filled blisters near lips", "Oozing blisters that scab", "Pain around mouth area", "Fever (first episode)"],
    "precautions": ["Antiviral cream or medication", "Avoid touching and spreading to eyes", "Don't share utensils or lip products", "Sun protection for lips"],
    "when_to_seek_care": ["Frequent outbreaks", "Spreading to eyes", "Immunocompromised", "Severe or prolonged outbreak"],
    "sources": [{"title": "Mayo Clinic – Cold Sores", "url": "https://www.mayoclinic.org/diseases-conditions/cold-sore/symptoms-causes/syc-20371017"}],
    "confidence": "high"
  },
  "sunburn": {
    "keywords": ["sunburn", "UV burn", "sun damaged skin", "peeling skin sun"],
    "summary": "Redness and pain caused by too much ultraviolet (UV) radiation from the sun.",
    "symptoms": ["Redness of skin", "Skin that feels warm or hot", "Pain", "Blisters (severe)", "Swelling", "Peeling skin (days later)", "Headache, fever, nausea (sun poisoning)"],
    "precautions": ["Apply soothing aloe vera gel", "Cool compresses", "Drink extra water", "Take pain reliever", "Avoid further sun exposure", "Use moisturizer"],
    "when_to_seek_care": ["Large blistering burns", "Fever over 103°F", "Confusion", "Severe pain", "Infant or young child with sunburn"],
    "sources": [{"title": "Mayo Clinic – Sunburn", "url": "https://www.mayoclinic.org/diseases-conditions/sunburn/symptoms-causes/syc-20355922"}],
    "confidence": "high"
  },
  "burns": {
    "keywords": ["burns", "thermal burn", "fire burn", "chemical burn", "scalding"],
    "summary": "Damage to skin or deeper tissues from heat, chemicals, electricity, or radiation.",
    "symptoms": ["First degree: redness, minor swelling, pain", "Second degree: blisters, deeper redness, wet skin", "Third degree: white or charred skin, little pain (nerve damage)"],
    "precautions": ["Cool burn with running water (not ice) for 20 minutes", "Remove jewelry", "Cover loosely with clean bandage", "Don't break blisters", "Seek medical attention for serious burns"],
    "when_to_seek_care": ["Burns larger than 3 inches", "Burns on hands, feet, face, genitals, over joints", "Deep burns", "Electrical or chemical burns", "Burns with inhalation injury"],
    "sources": [{"title": "Mayo Clinic – Burns", "url": "https://www.mayoclinic.org/diseases-conditions/burns/symptoms-causes/syc-20370539"}],
    "confidence": "high"
  },
  "frostbite": {
    "keywords": ["frostbite", "freezing injury", "frost bite", "cold injury"],
    "summary": "Injury to body tissue caused by freezing, affecting fingers, toes, nose, and ears.",
    "symptoms": ["Cold, hard, waxy skin", "Numbness in affected area", "Skin turns red, then white or grayish-yellow", "Large blisters after rewarming", "Stiffness"],
    "precautions": ["Get to a warm area", "Don't walk on frostbitten feet if avoidable", "Don't rub frostbitten skin", "Remove wet or tight clothing", "Rewarm slowly in warm (not hot) water"],
    "when_to_seek_care": ["Any suspected frostbite – seek medical care", "Skin remains hard after rewarming", "Blisters develop", "Signs of infection"],
    "sources": [{"title": "Mayo Clinic – Frostbite", "url": "https://www.mayoclinic.org/diseases-conditions/frostbite/symptoms-causes/syc-20372656"}],
    "confidence": "high"
  },
  "heat stroke": {
    "keywords": ["heat stroke", "hyperthermia", "heat exhaustion", "overheating", "sunstroke"],
    "summary": "A condition caused by body overheating, usually due to prolonged exposure to high temperatures.",
    "symptoms": ["High body temperature (above 104°F)", "Altered mental state or confusion", "Hot, dry skin (heat stroke) or heavy sweating", "Nausea and vomiting", "Rapid breathing", "Racing heart rate", "Headache"],
    "precautions": ["EMERGENCY – heat stroke requires immediate care", "Move to cool area", "Cool with wet cloths or ice packs", "Fan the person", "Give cool fluids if conscious and not confused"],
    "when_to_seek_care": ["Any suspected heat stroke – call 911", "Temperature above 104°F", "Confusion or unconsciousness", "Seizures"],
    "sources": [{"title": "Mayo Clinic – Heat Stroke", "url": "https://www.mayoclinic.org/diseases-conditions/heat-stroke/symptoms-causes/syc-20353581"}],
    "confidence": "high"
  },
  "drowning near-drowning": {
    "keywords": ["drowning", "near drowning", "submersion injury", "water inhalation"],
    "summary": "Respiratory impairment from submersion or immersion in water.",
    "symptoms": ["Difficulty breathing after water exposure", "Coughing", "Vomiting", "Confusion or altered consciousness", "Extreme fatigue"],
    "precautions": ["Call 911 immediately", "Begin CPR if not breathing", "Don't leave person alone", "Keep person warm"],
    "when_to_seek_care": ["ANY water submersion – always seek care even if they seem fine", "Delayed symptoms may occur"],
    "sources": [{"title": "CDC – Drowning", "url": "https://www.cdc.gov/drowning/data/index.html"}],
    "confidence": "high"
  },
  "poisoning": {
    "keywords": ["poisoning", "overdose", "toxic ingestion", "poison", "accidental ingestion"],
    "summary": "Harm caused by swallowing, touching, or inhaling a harmful substance.",
    "symptoms": ["Nausea and vomiting", "Abdominal pain", "Drowsiness or unconsciousness", "Difficulty breathing", "Burns around mouth", "Seizures", "Rapid or slow heartbeat"],
    "precautions": ["Call Poison Control immediately", "Don't induce vomiting unless told to", "Keep substance container", "Follow emergency instructions"],
    "when_to_seek_care": ["ANY suspected poisoning – call Poison Control (1-800-222-1222 in US) or 911", "Unconscious person", "Seizures", "Difficulty breathing"],
    "sources": [{"title": "Poison Control", "url": "https://www.poison.org/"}],
    "confidence": "high"
  },
  "fracture": {
    "keywords": ["fracture", "broken bone", "bone fracture", "stress fracture", "broken arm", "broken leg"],
    "summary": "A break in the continuity of a bone.",
    "symptoms": ["Severe pain at injury site", "Swelling and bruising", "Visible deformity", "Tenderness to touch", "Inability to use affected area", "Numbness (nerve involvement)"],
    "precautions": ["Immobilize the area", "Apply ice wrapped in cloth", "Elevate if possible", "Seek emergency care", "Don't attempt to straighten deformed bone"],
    "when_to_seek_care": ["ANY suspected fracture – seek emergency care", "Open fracture (bone visible)", "Numbness or weakness below injury", "Severe pain"],
    "sources": [{"title": "Mayo Clinic – Broken Bone", "url": "https://www.mayoclinic.org/diseases-conditions/broken-leg/symptoms-causes/syc-20355412"}],
    "confidence": "high"
  },
  "sprain": {
    "keywords": ["sprain", "ankle sprain", "ligament injury", "twisted ankle", "joint sprain"],
    "summary": "Stretching or tearing of ligaments, usually from sudden twisting.",
    "symptoms": ["Pain", "Swelling", "Bruising", "Limited range of motion", "Instability in the joint", "Hearing a pop at time of injury"],
    "precautions": ["RICE method (Rest, Ice, Compression, Elevation)", "Avoid putting weight on joint", "OTC pain relief", "Use crutches if needed"],
    "when_to_seek_care": ["Unable to bear weight", "Severe pain", "Visible deformity", "Numbness", "No improvement in 2-3 days"],
    "sources": [{"title": "Mayo Clinic – Sprains", "url": "https://www.mayoclinic.org/diseases-conditions/sprains/symptoms-causes/syc-20377938"}],
    "confidence": "high"
  },
  "head injury": {
    "keywords": ["head injury", "concussion", "traumatic brain injury", "TBI", "head trauma"],
    "summary": "Injury to the brain, skull, or scalp.",
    "symptoms": ["Headache", "Confusion", "Nausea or vomiting", "Memory problems", "Loss of consciousness", "Dizziness", "Slurred speech", "Seizures"],
    "precautions": ["Seek immediate evaluation", "Rest from physical and cognitive activity", "Avoid alcohol", "Don't return to sports without clearance"],
    "when_to_seek_care": ["Loss of consciousness", "Repeated vomiting", "One pupil larger than other", "Extreme drowsiness", "Slurred speech", "Seizures", "Clear fluid from nose or ear"],
    "sources": [{"title": "CDC – Concussion", "url": "https://www.cdc.gov/headsup/basics/concussion_whatis.html"}],
    "confidence": "high"
  },
  "eye injury": {
    "keywords": ["eye injury", "eye trauma", "chemical in eye", "foreign body eye", "eye pain"],
    "summary": "Injury to the eye from trauma, foreign bodies, chemicals, or other causes.",
    "symptoms": ["Pain in eye", "Redness", "Watering", "Sensitivity to light", "Blurred vision", "Visible foreign object"],
    "precautions": ["Don't rub injured eye", "Flush with water for chemical injuries (20+ minutes)", "Cover eye loosely", "Seek immediate care"],
    "when_to_seek_care": ["Chemical exposure to eye", "Penetrating eye injury", "Sudden vision change", "Severe pain", "Cannot remove visible object"],
    "sources": [{"title": "AAO – Eye Injuries", "url": "https://www.aao.org/eye-health/tips-prevention/injuries"}],
    "confidence": "high"
  },
  "insect bite": {
    "keywords": ["insect bite", "bee sting", "wasp sting", "mosquito bite", "tick bite"],
    "summary": "Reactions to bites or stings from insects including mosquitoes, bees, and ticks.",
    "symptoms": ["Localized pain", "Redness and swelling", "Itching or burning", "Allergic reactions (hives, throat swelling)", "Blister formation"],
    "precautions": ["Remove stinger if present (scrape, don't pinch)", "Wash the area", "Apply ice", "Antihistamine for itching", "Monitor for allergic reaction"],
    "when_to_seek_care": ["Anaphylaxis signs", "Spreading redness from tick bite", "Fever after tick bite", "Infection signs", "Stings in mouth or throat"],
    "sources": [{"title": "Mayo Clinic – Bee Stings", "url": "https://www.mayoclinic.org/diseases-conditions/bee-stings/symptoms-causes/syc-20353869"}],
    "confidence": "medium"
  },
  "snake bite": {
    "keywords": ["snake bite", "venomous snake", "snake envenomation"],
    "summary": "A bite from a snake, which may or may not be venomous.",
    "symptoms": ["Two puncture wounds", "Pain and swelling at bite site", "Redness and bruising", "Nausea and vomiting", "Difficulty breathing", "Blurred vision", "Numbness or tingling"],
    "precautions": ["Call 911 immediately", "Keep person calm and still", "Immobilize affected limb below heart level", "Remove tight clothing and jewelry", "Don't suck out venom or apply tourniquet"],
    "when_to_seek_care": ["ANY snake bite – call 911 and seek emergency care immediately", "Assume venomous until proven otherwise"],
    "sources": [{"title": "CDC – Snake Bites", "url": "https://www.cdc.gov/niosh/topics/snakebite/default.html"}],
    "confidence": "high"
  },
  "dog bite": {
    "keywords": ["dog bite", "animal bite", "cat bite", "bite wound"],
    "summary": "A wound caused by the bite of an animal, carrying infection risk.",
    "symptoms": ["Puncture wounds or lacerations", "Pain and swelling", "Bleeding", "Bruising", "Risk of infection"],
    "precautions": ["Wash wound thoroughly with soap and water for 15 minutes", "Apply pressure to stop bleeding", "Seek medical care", "Report bite", "Assess rabies risk"],
    "when_to_seek_care": ["Deep puncture wound", "Wound won't stop bleeding", "Bite to face, hands, or genitals", "Any animal bite – assess for rabies", "Signs of infection"],
    "sources": [{"title": "Mayo Clinic – Animal Bites", "url": "https://www.mayoclinic.org/first-aid/first-aid-animal-bites/basics/art-20056591"}],
    "confidence": "high"
  },
  "electrocution": {
    "keywords": ["electrocution", "electric shock", "electrical injury", "electric burn"],
    "summary": "Injury caused by passing electric current through the body.",
    "symptoms": ["Burns at entry and exit points", "Cardiac arrhythmia", "Muscle pain and contractions", "Numbness", "Confusion", "Unconsciousness"],
    "precautions": ["Ensure person is away from electrical source before touching", "Call 911 immediately", "Begin CPR if needed", "Treat burns"],
    "when_to_seek_care": ["ANY electrical injury – emergency care required", "Loss of consciousness", "Cardiac symptoms", "Burns"],
    "sources": [{"title": "Mayo Clinic – Electrical Injury", "url": "https://www.mayoclinic.org/diseases-conditions/electrical-injury/symptoms-causes/syc-20370765"}],
    "confidence": "high"
  },
  "hemorrhagic fever": {
    "keywords": ["hemorrhagic fever", "Ebola", "Marburg", "Lassa fever", "viral hemorrhagic fever"],
    "summary": "A group of illnesses caused by viruses that cause fever and bleeding disorders.",
    "symptoms": ["High fever", "Severe headache", "Muscle pain", "Weakness", "Fatigue", "Bleeding from various sites", "Vomiting", "Diarrhea"],
    "precautions": ["Seek immediate emergency care", "Isolation precautions", "Supportive treatment"],
    "when_to_seek_care": ["Fever with bleeding after travel to endemic areas", "ANY suspected hemorrhagic fever – emergency"],
    "sources": [{"title": "CDC – Viral Hemorrhagic Fevers", "url": "https://www.cdc.gov/vhf/index.html"}],
    "confidence": "medium"
  },
  "cholera": {
    "keywords": ["cholera", "Vibrio cholerae", "rice water stools", "severe diarrhea dehydration"],
    "summary": "An acute bacterial diarrheal disease caused by Vibrio cholerae bacteria.",
    "symptoms": ["Sudden onset profuse watery diarrhea (rice water stools)", "Nausea and vomiting", "Rapid dehydration", "Muscle cramps", "Sunken eyes", "Dry mouth"],
    "precautions": ["Oral rehydration therapy immediately", "Seek medical care urgently", "Drink only safe water", "Wash hands with soap", "Cholera vaccination in endemic areas"],
    "when_to_seek_care": ["ANY suspected cholera – seek emergency care", "Signs of severe dehydration", "Unable to take oral fluids"],
    "sources": [{"title": "WHO – Cholera", "url": "https://www.who.int/news-room/fact-sheets/detail/cholera"}],
    "confidence": "high"
  },
  "leprosy": {
    "keywords": ["leprosy", "Hansen's disease", "Mycobacterium leprae", "skin numbness patches"],
    "summary": "A chronic bacterial infection affecting skin, nerves, and mucous membranes.",
    "symptoms": ["Pale or reddish skin patches with loss of sensation", "Numbness in patches", "Weakness in hands and feet", "Enlarged peripheral nerves", "Eye problems", "Muscle weakness"],
    "precautions": ["Complete multidrug therapy as prescribed", "Regular monitoring", "Foot care", "Eye care", "Social support"],
    "when_to_seek_care": ["Skin patches with loss of sensation", "Nerve-related weakness", "Eye problems", "Any suspected leprosy"],
    "sources": [{"title": "WHO – Leprosy", "url": "https://www.who.int/news-room/fact-sheets/detail/leprosy"}],
    "confidence": "high"
  },
  "plague": {
    "keywords": ["plague", "bubonic plague", "Yersinia pestis", "flea bite swollen lymph"],
    "summary": "A serious bacterial infection caused by Yersinia pestis, typically transmitted by fleas.",
    "symptoms": ["Sudden fever, chills", "Headache and weakness", "Swollen, painful lymph nodes (buboes)", "Cough with bloody mucus (pneumonic)", "Abdominal pain"],
    "precautions": ["Avoid contact with dead rodents", "Flea control", "Antibiotics if exposed", "Seek immediate medical care"],
    "when_to_seek_care": ["ANY suspected plague – emergency", "Swollen lymph nodes with fever", "After rodent or flea exposure in endemic area"],
    "sources": [{"title": "CDC – Plague", "url": "https://www.cdc.gov/plague/index.html"}],
    "confidence": "medium"
  },
  "anthrax": {
    "keywords": ["anthrax", "Bacillus anthracis", "cutaneous anthrax", "inhalation anthrax"],
    "summary": "A serious infection caused by the spore-forming bacteria Bacillus anthracis.",
    "symptoms": ["Cutaneous: skin sore with black center", "Inhalation: flu-like then severe breathing difficulty", "Gastrointestinal: nausea, bloody diarrhea"],
    "precautions": ["Anthrax vaccine for at-risk populations", "Antibiotics if exposed", "Seek immediate care if suspected"],
    "when_to_seek_care": ["ANY suspected anthrax – emergency", "Suspicious skin sore with black center"],
    "sources": [{"title": "CDC – Anthrax", "url": "https://www.cdc.gov/anthrax/index.html"}],
    "confidence": "medium"
  },
  "Zika virus": {
    "keywords": ["Zika", "Zika virus", "Zika fever", "microcephaly"],
    "summary": "A mosquito-borne viral infection usually causing mild illness but serious birth defects.",
    "symptoms": ["Mild fever", "Rash", "Conjunctivitis", "Muscle and joint pain", "Headache", "Often no symptoms"],
    "precautions": ["Prevent mosquito bites", "Use repellent", "Avoid travel to endemic areas if pregnant", "Use condoms"],
    "when_to_seek_care": ["Pregnant women with possible Zika exposure", "Guillain-Barré syndrome symptoms"],
    "sources": [{"title": "WHO – Zika Virus", "url": "https://www.who.int/news-room/fact-sheets/detail/zika-virus"}],
    "confidence": "high"
  },
  "West Nile virus": {
    "keywords": ["West Nile", "West Nile virus", "WNV", "mosquito encephalitis"],
    "summary": "A mosquito-borne viral infection, most cases are mild but can cause encephalitis.",
    "symptoms": ["Most: no symptoms or mild flu-like illness", "Severe: high fever, headache, neck stiffness, disorientation", "Coma, tremors, vision loss"],
    "precautions": ["Use insect repellent", "Wear protective clothing", "Avoid peak mosquito hours", "Eliminate standing water"],
    "when_to_seek_care": ["Severe headache with fever", "Neck stiffness", "Confusion", "Weakness", "After mosquito exposure in endemic area"],
    "sources": [{"title": "CDC – West Nile Virus", "url": "https://www.cdc.gov/westnile/index.html"}],
    "confidence": "medium"
  },
  "Japanese encephalitis": {
    "keywords": ["Japanese encephalitis", "JE", "mosquito brain infection", "encephalitis Asia"],
    "summary": "A mosquito-borne viral brain infection prevalent in Asian countries.",
    "symptoms": ["High fever", "Headache", "Vomiting", "Confusion", "Difficulty moving", "Seizures", "Coma"],
    "precautions": ["Get JE vaccine before travel to endemic areas", "Use mosquito repellent", "Wear protective clothing"],
    "when_to_seek_care": ["High fever with altered consciousness after travel in Asia", "Seizures", "Stiff neck with fever"],
    "sources": [{"title": "WHO – Japanese Encephalitis", "url": "https://www.who.int/news-room/fact-sheets/detail/japanese-encephalitis"}],
    "confidence": "medium"
  },
  "rotavirus": {
    "keywords": ["rotavirus", "rotavirus diarrhea", "infant diarrhea viral"],
    "summary": "A highly contagious viral cause of diarrhea, most severe in infants and young children.",
    "symptoms": ["Watery diarrhea", "Vomiting", "Fever", "Abdominal pain", "Dehydration"],
    "precautions": ["Rotavirus vaccination", "Hand washing", "Oral rehydration", "Avoid contact with infected children"],
    "when_to_seek_care": ["Signs of dehydration in infant", "Unable to keep fluids down", "Blood in stool", "Extreme lethargy"],
    "sources": [{"title": "CDC – Rotavirus", "url": "https://www.cdc.gov/rotavirus/index.html"}],
    "confidence": "high"
  },
  "norovirus": {
    "keywords": ["norovirus", "stomach virus", "winter vomiting bug", "cruise ship illness"],
    "summary": "A very contagious virus causing vomiting and diarrhea.",
    "symptoms": ["Sudden nausea", "Vomiting", "Diarrhea", "Stomach cramps", "Low-grade fever", "Body aches", "Headache"],
    "precautions": ["Wash hands with soap and water", "Clean and disinfect surfaces", "Wash fruits and vegetables", "Avoid preparing food when ill", "Stay home until 48 hours after last symptoms"],
    "when_to_seek_care": ["Severe dehydration", "Blood in stool", "Symptoms not improving after 3 days", "Infants, elderly, immunocompromised"],
    "sources": [{"title": "CDC – Norovirus", "url": "https://www.cdc.gov/norovirus/index.html"}],
    "confidence": "high"
  },
  "mononucleosis": {
    "keywords": ["mononucleosis", "mono", "kissing disease", "Epstein-Barr virus", "glandular fever"],
    "summary": "An infectious disease caused by the Epstein-Barr virus.",
    "symptoms": ["Extreme fatigue", "Sore throat", "Fever", "Swollen lymph nodes in neck and armpits", "Swollen tonsils", "Headache", "Skin rash", "Soft, swollen spleen"],
    "precautions": ["Rest", "Avoid contact sports (risk of spleen rupture)", "Drink plenty of fluids", "Take OTC pain relievers", "Avoid alcohol"],
    "when_to_seek_care": ["Severe difficulty swallowing", "Extreme weakness", "Spleen pain", "Difficulty breathing", "Worsening symptoms"],
    "sources": [{"title": "Mayo Clinic – Mono", "url": "https://www.mayoclinic.org/diseases-conditions/mononucleosis/symptoms-causes/syc-20350328"}],
    "confidence": "high"
  },
  "strep throat": {
    "keywords": ["strep throat", "streptococcal pharyngitis", "bacterial throat infection", "Group A strep"],
    "summary": "A bacterial throat infection caused by Group A Streptococcus.",
    "symptoms": ["Sore throat (severe)", "Painful swallowing", "Fever above 101°F", "Swollen, tender lymph nodes in neck", "Red and swollen tonsils", "White patches on tonsils", "Headache"],
    "precautions": ["Complete full antibiotic course", "Rest and fluids", "Avoid spreading (wash hands, cover mouth)", "Stay home until 24 hours on antibiotics"],
    "when_to_seek_care": ["Very sore throat with fever", "White patches on tonsils", "Difficulty swallowing or breathing", "Suspected strep exposure"],
    "sources": [{"title": "CDC – Strep Throat", "url": "https://www.cdc.gov/group-a-strep/strep-throat/index.html"}],
    "confidence": "high"
  },
  "croup": {
    "keywords": ["croup", "barking cough", "seal cough", "stridor children", "laryngotracheobronchitis"],
    "summary": "A respiratory condition causing a characteristic barking cough in children.",
    "symptoms": ["Barking cough", "Hoarse voice", "Noisy breathing (stridor)", "Fever", "Runny nose", "Worse at night"],
    "precautions": ["Breathe cool night air", "Comfort child", "Humidifier", "OTC fever reducer", "Keep calm (crying worsens symptoms)"],
    "when_to_seek_care": ["Stridor at rest", "Child turning blue", "High fever", "Drooling or difficulty swallowing", "Extreme distress"],
    "sources": [{"title": "Mayo Clinic – Croup", "url": "https://www.mayoclinic.org/diseases-conditions/croup/symptoms-causes/syc-20350348"}],
    "confidence": "high"
  },
  "epiglottitis": {
    "keywords": ["epiglottitis", "epiglottis infection", "drooling difficulty swallowing fever"],
    "summary": "A life-threatening inflammation of the epiglottis (flap at base of tongue).",
    "symptoms": ["Severe sore throat", "Drooling", "Difficulty swallowing", "Muffled voice", "High fever", "Leaning forward to breathe better", "Stridor"],
    "precautions": ["EMERGENCY – call 911", "Don't look in throat with tongue depressor", "Keep person calm"],
    "when_to_seek_care": ["ANY suspected epiglottitis – call 911 immediately", "Drooling with difficulty breathing", "Stridor with high fever"],
    "sources": [{"title": "Mayo Clinic – Epiglottitis", "url": "https://www.mayoclinic.org/diseases-conditions/epiglottitis/symptoms-causes/syc-20372227"}],
    "confidence": "high"
  },
  "laryngitis": {
    "keywords": ["laryngitis", "hoarse voice", "voice loss", "lost voice", "throat infection"],
    "summary": "Inflammation of the larynx (voice box) causing hoarseness.",
    "symptoms": ["Hoarseness", "Weak or loss of voice", "Tickling sensation in throat", "Sore throat", "Dry throat", "Dry cough"],
    "precautions": ["Rest voice", "Stay hydrated", "Breathe moist air", "Avoid throat clearing", "No whispering (strains voice)"],
    "when_to_seek_care": ["Hoarseness lasting more than 3 weeks", "Blood in mucus", "Difficulty breathing", "Swallowing difficulties", "Lump in neck"],
    "sources": [{"title": "Mayo Clinic – Laryngitis", "url": "https://www.mayoclinic.org/diseases-conditions/laryngitis/symptoms-causes/syc-20374262"}],
    "confidence": "high"
  },
  "pharyngitis": {
    "keywords": ["pharyngitis", "sore throat bacterial", "throat pain swallowing", "throat inflammation"],
    "summary": "Inflammation of the back of the throat (pharynx) causing sore throat.",
    "symptoms": ["Sore throat", "Painful or difficult swallowing", "Red and swollen tonsils", "Voice changes", "Mild fever", "Runny nose", "Cough"],
    "precautions": ["Rest and fluids", "Salt water gargle", "OTC pain relievers", "Lozenges", "Antibiotics if bacterial (strep)"],
    "when_to_seek_care": ["Severe difficulty swallowing", "High fever", "White patches on throat", "Symptoms lasting more than 1 week"],
    "sources": [{"title": "Mayo Clinic – Sore Throat", "url": "https://www.mayoclinic.org/diseases-conditions/sore-throat/symptoms-causes/syc-20351635"}],
    "confidence": "high"
  },
  "tonsillitis": {
    "keywords": ["tonsillitis", "tonsil infection", "inflamed tonsils", "peritonsillar abscess"],
    "summary": "Inflammation of the tonsils, usually from a viral or bacterial infection.",
    "symptoms": ["Swollen tonsils", "Sore throat", "Difficulty swallowing", "Fever", "Yellow or white coating on tonsils", "Swollen lymph nodes in neck", "Headache", "Bad breath"],
    "precautions": ["Rest and fluids", "OTC pain relievers", "Antibiotics if bacterial", "Salt water gargle", "Soft foods"],
    "when_to_seek_care": ["Difficulty breathing or swallowing", "Drooling", "High fever", "Severe neck stiffness", "Recurrent tonsillitis"],
    "sources": [{"title": "Mayo Clinic – Tonsillitis", "url": "https://www.mayoclinic.org/diseases-conditions/tonsillitis/symptoms-causes/syc-20350728"}],
    "confidence": "high"
  },
  "dental abscess": {
    "keywords": ["dental abscess", "tooth abscess", "gum abscess", "tooth infection"],
    "summary": "A pocket of pus caused by bacterial infection in a tooth or surrounding gums.",
    "symptoms": ["Severe, persistent, throbbing toothache", "Sensitivity to temperature", "Fever", "Swelling in face or cheek", "Swollen lymph nodes under jaw", "Foul taste", "Difficulty opening mouth"],
    "precautions": ["See dentist immediately", "Rinse with warm salt water", "OTC pain relief", "Don't puncture abscess"],
    "when_to_seek_care": ["Fever with dental pain", "Swelling spreading to neck or floor of mouth", "Difficulty breathing or swallowing", "Tooth pain – see dentist"],
    "sources": [{"title": "Mayo Clinic – Dental Abscess", "url": "https://www.mayoclinic.org/diseases-conditions/tooth-abscess/symptoms-causes/syc-20352861"}],
    "confidence": "high"
  },
  "mouth ulcers": {
    "keywords": ["mouth ulcers", "canker sores", "aphthous ulcers", "oral ulcers", "mouth sores"],
    "summary": "Painful sores inside the mouth, usually on gums, inner cheeks, or tongue.",
    "symptoms": ["Painful round or oval sores", "White or yellow center with red border", "Tingling before ulcer appears", "Difficulty eating or drinking due to pain"],
    "precautions": ["Rinse with salt water", "Avoid spicy and acidic foods", "Topical gels or ointments", "Soft toothbrush", "Vitamin B12, zinc, folic acid if deficient"],
    "when_to_seek_care": ["Unusually large sores", "More than 3 at a time", "Lasting more than 3 weeks", "Fever with sores", "Spreading to lips"],
    "sources": [{"title": "Mayo Clinic – Canker Sore", "url": "https://www.mayoclinic.org/diseases-conditions/canker-sore/symptoms-causes/syc-20370615"}],
    "confidence": "high"
  },
  "halitosis": {
    "keywords": ["bad breath", "halitosis", "mouth odor", "breath odor"],
    "summary": "Persistent bad breath from poor dental hygiene or underlying conditions.",
    "symptoms": ["Unpleasant mouth odor", "Dry mouth", "White coating on tongue"],
    "precautions": ["Brush teeth and tongue twice daily", "Floss daily", "Stay hydrated", "Mouthwash", "Regular dental checkups", "Treat underlying conditions"],
    "when_to_seek_care": ["Persistent bad breath despite good hygiene", "Associated with gum pain or bleeding", "Symptoms of sinus or throat infection"],
    "sources": [{"title": "Mayo Clinic – Bad Breath", "url": "https://www.mayoclinic.org/diseases-conditions/bad-breath/symptoms-causes/syc-20350922"}],
    "confidence": "medium"
  },
  "COPD": {
    "keywords": ["COPD", "chronic obstructive pulmonary disease", "emphysema", "chronic bronchitis", "smoking lung disease"],
    "summary": "A chronic inflammatory lung disease causing obstructed airflow.",
    "symptoms": ["Shortness of breath (especially with activity)", "Wheezing", "Chest tightness", "Chronic cough (often with mucus)", "Frequent respiratory infections", "Fatigue", "Swelling in ankles", "Bluish lips or fingertips"],
    "precautions": ["Quit smoking", "Use inhalers as prescribed", "Pulmonary rehabilitation", "Get flu and pneumonia vaccines", "Avoid air pollutants"],
    "when_to_seek_care": ["Sudden worsening of breathing", "Bluish lips", "Confusion or lethargy", "Frequent exacerbations", "Inability to manage symptoms"],
    "sources": [{"title": "GOLD – COPD", "url": "https://goldcopd.org/"}],
    "confidence": "high"
  },
  "pulmonary embolism": {
    "keywords": ["pulmonary embolism", "PE", "blood clot lung", "lung clot"],
    "summary": "A blood clot that travels to the lungs, blocking blood flow.",
    "symptoms": ["Sudden shortness of breath", "Chest pain (sharp, worsens with deep breath)", "Rapid heart rate", "Coughing up blood", "Feeling faint or dizzy", "Leg swelling or pain (DVT)"],
    "precautions": ["EMERGENCY – call 911", "Don't wait to seek care", "Previous history: take anticoagulants as prescribed"],
    "when_to_seek_care": ["ANY suspected pulmonary embolism – call 911 immediately"],
    "sources": [{"title": "Mayo Clinic – Pulmonary Embolism", "url": "https://www.mayoclinic.org/diseases-conditions/pulmonary-embolism/symptoms-causes/syc-20354647"}],
    "confidence": "high"
  },
  "atrial fibrillation": {
    "keywords": ["atrial fibrillation", "AFib", "AF", "irregular heartbeat", "palpitations"],
    "summary": "An irregular and often very rapid heart rhythm affecting blood flow.",
    "symptoms": ["Irregular heartbeat (palpitations)", "Fluttering in chest", "Shortness of breath", "Weakness and fatigue", "Reduced ability to exercise", "Dizziness", "Chest pain"],
    "precautions": ["Take prescribed anticoagulants", "Heart rate control medications", "Regular cardiology follow-up", "Limit alcohol", "Manage thyroid disease and hypertension"],
    "when_to_seek_care": ["New onset palpitations", "Chest pain", "Shortness of breath", "Signs of stroke", "Rapid heart rate not controlled"],
    "sources": [{"title": "AHA – AFib", "url": "https://www.heart.org/en/health-topics/atrial-fibrillation"}],
    "confidence": "high"
  },
  "heart failure": {
    "keywords": ["heart failure", "congestive heart failure", "CHF", "fluid in lungs", "left heart failure"],
    "summary": "A chronic condition where the heart doesn't pump blood effectively.",
    "symptoms": ["Shortness of breath", "Fatigue and weakness", "Swelling in legs, ankles, and feet", "Rapid or irregular heartbeat", "Reduced ability to exercise", "Persistent cough with pink mucus", "Nausea", "Sudden weight gain from fluid"],
    "precautions": ["Take prescribed medications", "Low-sodium diet", "Daily weight monitoring", "Limit fluids if advised", "Regular cardiology checkups"],
    "when_to_seek_care": ["Sudden shortness of breath", "Rapid weight gain (2-3 lbs in a day)", "Severe swelling", "Chest pain", "Fainting"],
    "sources": [{"title": "AHA – Heart Failure", "url": "https://www.heart.org/en/health-topics/heart-failure"}],
    "confidence": "high"
  },
  "peripheral artery disease": {
    "keywords": ["peripheral artery disease", "PAD", "leg claudication", "poor circulation legs"],
    "summary": "Narrowed arteries reduce blood flow to the limbs.",
    "symptoms": ["Painful cramping in legs when walking (claudication)", "Leg numbness or weakness", "Cold lower leg or foot", "Sores on toes, feet, or legs", "Hair loss on leg", "Weak pulse in legs", "Shiny skin on legs"],
    "precautions": ["Quit smoking", "Exercise program", "Control diabetes and blood pressure", "Medications as prescribed", "Foot care"],
    "when_to_seek_care": ["Sores not healing", "Severe leg pain at rest", "Signs of critical limb ischemia", "Sudden worsening"],
    "sources": [{"title": "Mayo Clinic – PAD", "url": "https://www.mayoclinic.org/diseases-conditions/peripheral-artery-disease/symptoms-causes/syc-20350557"}],
    "confidence": "high"
  },
  "varicose veins": {
    "keywords": ["varicose veins", "spider veins", "varicosities", "leg veins bulging"],
    "summary": "Twisted, enlarged veins near the surface of the skin.",
    "symptoms": ["Dark purple or blue veins", "Bulging, cord-like veins", "Aching or heaviness in legs", "Burning, throbbing, muscle cramping", "Itching around veins", "Skin discoloration around vein"],
    "precautions": ["Exercise", "Elevate legs", "Compression stockings", "Avoid long periods of standing or sitting", "Maintain healthy weight"],
    "when_to_seek_care": ["Severe pain", "Skin ulcers near varicose veins", "Significant swelling", "Bleeding from varicose veins"],
    "sources": [{"title": "Mayo Clinic – Varicose Veins", "url": "https://www.mayoclinic.org/diseases-conditions/varicose-veins/symptoms-causes/syc-20350643"}],
    "confidence": "high"
  },
  "aortic aneurysm": {
    "keywords": ["aortic aneurysm", "abdominal aortic aneurysm", "AAA", "aortic dissection"],
    "summary": "A bulge in the wall of the aorta that can rupture if untreated.",
    "symptoms": ["Often no symptoms", "Deep, constant pain in abdomen or back", "Pulsating feeling in abdomen", "Sudden severe back or abdominal pain if ruptured"],
    "precautions": ["Regular monitoring if diagnosed", "Control blood pressure", "Quit smoking", "Avoid strenuous activity if large aneurysm"],
    "when_to_seek_care": ["Sudden severe abdominal or back pain – emergency", "Tearing or ripping pain", "Signs of internal bleeding"],
    "sources": [{"title": "Mayo Clinic – Aortic Aneurysm", "url": "https://www.mayoclinic.org/diseases-conditions/aortic-aneurysm/symptoms-causes/syc-20369472"}],
    "confidence": "high"
  },
  "endocarditis": {
    "keywords": ["endocarditis", "heart valve infection", "infective endocarditis", "IE"],
    "summary": "Inflammation of the inner lining of the heart chambers and valves.",
    "symptoms": ["Fever and chills", "New or changed heart murmur", "Fatigue", "Muscle and joint pain", "Night sweats", "Shortness of breath", "Small red spots on skin", "Blood in urine"],
    "precautions": ["Antibiotics before dental procedures (if high risk)", "Good dental hygiene", "Avoid body piercing with high-risk heart conditions", "Antibiotic prophylaxis"],
    "when_to_seek_care": ["Fever with known heart condition", "New heart murmur", "Embolic events (stroke, organ damage)", "Worsening symptoms"],
    "sources": [{"title": "Mayo Clinic – Endocarditis", "url": "https://www.mayoclinic.org/diseases-conditions/endocarditis/symptoms-causes/syc-20352576"}],
    "confidence": "high"
  },
  "pericarditis": {
    "keywords": ["pericarditis", "heart sac inflammation", "sharp chest pain sitting forward"],
    "summary": "Inflammation of the pericardium (the sac surrounding the heart).",
    "symptoms": ["Sharp, stabbing chest pain", "Pain worse when lying down or breathing in", "Pain relieved by sitting forward", "Fever", "Shortness of breath", "Palpitations"],
    "precautions": ["Rest", "Anti-inflammatory medications", "Avoid strenuous activity", "Complete prescribed medications"],
    "when_to_seek_care": ["Chest pain – rule out heart attack", "Shortness of breath", "High fever", "Signs of cardiac tamponade (low BP, rapid heart rate)"],
    "sources": [{"title": "Mayo Clinic – Pericarditis", "url": "https://www.mayoclinic.org/diseases-conditions/pericarditis/symptoms-causes/syc-20352510"}],
    "confidence": "high"
  },
  "cirrhosis": {
    "keywords": ["cirrhosis", "liver cirrhosis", "liver scarring", "hepatic cirrhosis", "end stage liver"],
    "summary": "Advanced scarring of the liver due to various liver diseases.",
    "symptoms": ["Fatigue", "Easy bruising", "Jaundice", "Itchy skin", "Spider angiomas on skin", "Redness in palms", "Swollen abdomen (ascites)", "Confusion (hepatic encephalopathy)"],
    "precautions": ["Abstain from alcohol", "Avoid hepatotoxic medications", "Regular medical monitoring", "Treat complications", "Liver transplant evaluation if needed"],
    "when_to_seek_care": ["Confusion or disorientation", "Vomiting blood", "Black or tarry stools", "Severe abdominal pain", "Rapid weight gain from fluid"],
    "sources": [{"title": "Mayo Clinic – Cirrhosis", "url": "https://www.mayoclinic.org/diseases-conditions/cirrhosis/symptoms-causes/syc-20351487"}],
    "confidence": "high"
  },
  "fatty liver disease": {
    "keywords": ["fatty liver", "NAFLD", "non-alcoholic fatty liver", "liver steatosis", "steatohepatitis"],
    "summary": "Buildup of excess fat in the liver not caused by alcohol.",
    "symptoms": ["Often no symptoms", "Fatigue", "Right upper abdominal pain", "Enlarged liver", "Weight loss (advanced stage)"],
    "precautions": ["Lose weight gradually", "Avoid alcohol", "Control diabetes and cholesterol", "Exercise regularly", "Avoid hepatotoxic supplements"],
    "when_to_seek_care": ["Jaundice", "Abdominal swelling", "Confusion", "Unexplained fatigue with liver risk factors"],
    "sources": [{"title": "Mayo Clinic – NAFLD", "url": "https://www.mayoclinic.org/diseases-conditions/nonalcoholic-fatty-liver-disease/symptoms-causes/syc-20354567"}],
    "confidence": "high"
  },
  "Wilson's disease": {
    "keywords": ["Wilson's disease", "copper accumulation", "liver copper", "hepatolenticular degeneration"],
    "summary": "A genetic disorder causing copper to accumulate in organs.",
    "symptoms": ["Fatigue and malaise", "Jaundice", "Golden-brown eye discoloration (Kayser-Fleischer rings)", "Tremors", "Difficulty with speech or swallowing", "Behavioral changes", "Liver disease symptoms"],
    "precautions": ["Copper-chelating agents as prescribed", "Low-copper diet", "Avoid copper supplements and shellfish", "Regular monitoring"],
    "when_to_seek_care": ["Neurological symptoms in young adult", "Liver disease without obvious cause", "Eye ring on examination"],
    "sources": [{"title": "Mayo Clinic – Wilson's Disease", "url": "https://www.mayoclinic.org/diseases-conditions/wilsons-disease/symptoms-causes/syc-20353251"}],
    "confidence": "medium"
  },
  "Cushing's syndrome": {
    "keywords": ["Cushing's syndrome", "Cushing syndrome", "cortisol excess", "hypercortisolism"],
    "summary": "A condition caused by prolonged exposure to high levels of cortisol.",
    "symptoms": ["Weight gain (especially trunk)", "Buffalo hump (fat behind neck)", "Moon face", "Pink or purple stretch marks", "Thin, fragile skin", "Slow healing", "Acne", "Fatigue", "Muscle weakness"],
    "precautions": ["Taper steroids under medical supervision", "Surgical treatment if tumor present", "Regular follow-up", "Bone density monitoring"],
    "when_to_seek_care": ["New unexplained weight gain with typical features", "Progressive muscle weakness", "High blood sugar or pressure"],
    "sources": [{"title": "Mayo Clinic – Cushing's Syndrome", "url": "https://www.mayoclinic.org/diseases-conditions/cushings-syndrome/symptoms-causes/syc-20351310"}],
    "confidence": "medium"
  },
  "Addison's disease": {
    "keywords": ["Addison's disease", "adrenal insufficiency", "adrenal fatigue", "low cortisol"],
    "summary": "Insufficient production of hormones by the adrenal glands.",
    "symptoms": ["Fatigue and muscle weakness", "Weight loss", "Darkening of skin", "Low blood pressure", "Salt craving", "Nausea and vomiting", "Abdominal pain"],
    "precautions": ["Hormone replacement therapy", "Stress dosing during illness", "Carry emergency injection kit", "Medical alert bracelet"],
    "when_to_seek_care": ["Adrenal crisis (severe weakness, vomiting, low BP) – emergency", "Darkening skin unexplained", "Persistent fatigue and weight loss"],
    "sources": [{"title": "Mayo Clinic – Addison's Disease", "url": "https://www.mayoclinic.org/diseases-conditions/addisons-disease/symptoms-causes/syc-20350293"}],
    "confidence": "medium"
  },
  "pheochromocytoma": {
    "keywords": ["pheochromocytoma", "adrenal tumor", "hypertensive crisis episodes", "pheo"],
    "summary": "A rare adrenal gland tumor causing dangerous spikes in blood pressure.",
    "symptoms": ["Episodic hypertension", "Severe headache during episodes", "Rapid or forceful heartbeat", "Sweating", "Pallor", "Tremor", "Nausea"],
    "precautions": ["Medical evaluation and treatment", "Avoid triggers (stress, certain medications)", "Surgical removal when planned"],
    "when_to_seek_care": ["Hypertensive crisis", "Severe episodic headache with sweating", "Suspected based on symptoms"],
    "sources": [{"title": "Mayo Clinic – Pheochromocytoma", "url": "https://www.mayoclinic.org/diseases-conditions/pheochromocytoma/symptoms-causes/syc-20353480"}],
    "confidence": "medium"
  },
  "acromegaly": {
    "keywords": ["acromegaly", "growth hormone excess", "enlarged hands feet face", "pituitary adenoma GH"],
    "summary": "A hormonal disorder from excess growth hormone, usually from a pituitary tumor.",
    "symptoms": ["Enlarged hands and feet", "Facial changes (prominent jaw, enlarged nose/lips)", "Oily skin", "Joint pain", "Deepened voice", "Enlarged organs", "Carpal tunnel symptoms"],
    "precautions": ["Surgical treatment of pituitary tumor", "Medications to control GH", "Regular monitoring"],
    "when_to_seek_care": ["Progressive changes in appearance", "Carpal tunnel with acromegaly features", "Vision changes from tumor"],
    "sources": [{"title": "Mayo Clinic – Acromegaly", "url": "https://www.mayoclinic.org/diseases-conditions/acromegaly/symptoms-causes/syc-20351222"}],
    "confidence": "medium"
  },
  "pituitary adenoma": {
    "keywords": ["pituitary adenoma", "pituitary tumor", "hyperprolactinemia", "prolactinoma"],
    "summary": "A noncancerous tumor of the pituitary gland affecting hormone secretion.",
    "symptoms": ["Headache", "Vision problems (bitemporal hemianopia)", "Fatigue", "Hormonal imbalances", "Galactorrhea (unexpected breast milk)", "Sexual dysfunction", "Irregular periods"],
    "precautions": ["Medication for hormone-secreting tumors", "Surgery if indicated", "Regular MRI monitoring"],
    "when_to_seek_care": ["Vision problems (especially tunnel vision)", "Severe headache", "Unexplained hormonal symptoms", "Galactorrhea"],
    "sources": [{"title": "Mayo Clinic – Pituitary Tumors", "url": "https://www.mayoclinic.org/diseases-conditions/pituitary-tumors/symptoms-causes/syc-20350548"}],
    "confidence": "medium"
  },
  "insect sting allergy": {
    "keywords": ["insect sting allergy", "bee sting allergy", "venom allergy", "allergic sting reaction"],
    "summary": "An allergic reaction to insect venom causing potentially life-threatening anaphylaxis.",
    "symptoms": ["Hives or itching spreading beyond sting site", "Throat tightening", "Difficulty breathing", "Rapid pulse", "Nausea or vomiting", "Dizziness", "Loss of consciousness"],
    "precautions": ["Carry epinephrine auto-injector", "Wear long sleeves outdoors", "Avoid strong fragrances", "Consider venom immunotherapy", "Wear medical alert bracelet"],
    "when_to_seek_care": ["ANY severe allergic reaction to insect sting", "Use epinephrine and call 911"],
    "sources": [{"title": "AAAAI – Insect Sting Allergy", "url": "https://www.aaaai.org/tools-for-the-public/conditions-library/allergies/insect-sting-allergy"}],
    "confidence": "high"
  },
  "drug allergy": {
    "keywords": ["drug allergy", "medication allergy", "penicillin allergy", "drug reaction"],
    "summary": "An immune reaction to a medication causing allergic symptoms.",
    "symptoms": ["Skin rash", "Hives", "Itching", "Fever", "Swelling", "Shortness of breath", "Anaphylaxis (severe cases)", "Stevens-Johnson syndrome (rare, severe)"],
    "precautions": ["Note and report all drug allergies", "Wear medical alert bracelet", "Carry epinephrine if severe allergy", "Ask about cross-reactive drugs"],
    "when_to_seek_care": ["Anaphylaxis signs", "Blistering rash (Stevens-Johnson)", "Breathing difficulty", "Fever with rash after new medication"],
    "sources": [{"title": "Mayo Clinic – Drug Allergy", "url": "https://www.mayoclinic.org/diseases-conditions/drug-allergy/symptoms-causes/syc-20371835"}],
    "confidence": "high"
  },
  "contact dermatitis": {
    "keywords": ["contact dermatitis", "allergic contact dermatitis", "contact rash", "skin irritant reaction"],
    "summary": "A red, itchy rash caused by direct contact with a substance.",
    "symptoms": ["Red rash", "Itching", "Burning or stinging", "Blisters that ooze", "Dry, cracked skin", "Swelling"],
    "precautions": ["Identify and avoid contact with irritant/allergen", "Wash area with soap and water", "Apply hydrocortisone cream", "Take antihistamines"],
    "when_to_seek_care": ["Widespread or severe rash", "Signs of infection", "Rash on face or genitals", "Not improving after several days"],
    "sources": [{"title": "Mayo Clinic – Contact Dermatitis", "url": "https://www.mayoclinic.org/diseases-conditions/contact-dermatitis/symptoms-causes/syc-20352742"}],
    "confidence": "high"
  },
  "rosacea": {
    "keywords": ["rosacea", "facial redness", "facial flushing", "red face chronic"],
    "summary": "A common skin condition causing redness and visible blood vessels in the face.",
    "symptoms": ["Facial redness", "Swollen red bumps", "Eye problems (ocular rosacea)", "Enlarged nose (rhinophyma)", "Flushing", "Burning sensation"],
    "precautions": ["Identify and avoid triggers (alcohol, spicy food, sun)", "Sunscreen daily", "Topical medications", "Gentle skin care products"],
    "when_to_seek_care": ["Eye problems (redness, burning, sensitivity)", "Thickening skin on nose", "Not responding to treatment"],
    "sources": [{"title": "Mayo Clinic – Rosacea", "url": "https://www.mayoclinic.org/diseases-conditions/rosacea/symptoms-causes/syc-20353815"}],
    "confidence": "high"
  },
  "vitiligo": {
    "keywords": ["vitiligo", "skin depigmentation", "white patches skin", "loss of skin color"],
    "summary": "A disease causing loss of skin pigment, resulting in white patches.",
    "symptoms": ["White patches on skin", "Premature whitening or greying of hair", "Loss of color in mucous membranes", "Loss of color in inner layer of eye"],
    "precautions": ["Sun protection (depigmented areas burn easily)", "Sunscreen and protective clothing", "Camouflage makeup", "Repigmentation therapies if desired"],
    "when_to_seek_care": ["Rapidly spreading", "Associated eye symptoms", "Significant psychological impact", "Associated autoimmune symptoms"],
    "sources": [{"title": "Mayo Clinic – Vitiligo", "url": "https://www.mayoclinic.org/diseases-conditions/vitiligo/symptoms-causes/syc-20355912"}],
    "confidence": "high"
  },
  "skin cancer": {
    "keywords": ["skin cancer", "melanoma", "basal cell carcinoma", "squamous cell carcinoma", "mole changes"],
    "summary": "Abnormal growth of skin cells, most often developing on sun-exposed skin.",
    "symptoms": ["New growth or change in existing mole (ABCDE rule)", "Asymmetry", "Border irregularity", "Color variation", "Diameter >6mm", "Evolving shape, size, color", "Sore that doesn't heal"],
    "precautions": ["Apply sunscreen daily (SPF 30+)", "Avoid UV tanning beds", "Wear protective clothing", "Monthly skin self-exams", "Annual dermatologist screening"],
    "when_to_seek_care": ["New or changing skin lesion", "Sore that doesn't heal", "Any ABCDE criteria", "Suspicious growths"],
    "sources": [{"title": "Skin Cancer Foundation", "url": "https://www.skincancer.org/"}],
    "confidence": "high"
  },
  "breast cancer": {
    "keywords": ["breast cancer", "breast lump", "breast tumor", "mammogram abnormal"],
    "summary": "Cancer originating in breast cells.",
    "symptoms": ["Lump in breast or armpit", "Thickening of breast skin", "Nipple discharge", "Nipple inversion", "Redness or pitting of breast skin", "Change in breast size or shape"],
    "precautions": ["Monthly breast self-exams", "Annual mammograms after 40-50", "Know family history", "Limit alcohol", "Regular medical checkups"],
    "when_to_seek_care": ["New breast lump", "Skin changes on breast", "Bloody nipple discharge", "Persistent breast pain", "Lymph node swelling"],
    "sources": [{"title": "ACS – Breast Cancer", "url": "https://www.cancer.org/cancer/breast-cancer.html"}],
    "confidence": "high"
  },
  "prostate cancer": {
    "keywords": ["prostate cancer", "prostate PSA", "prostate tumor", "prostatectomy"],
    "summary": "Cancer in the prostate gland, common in older men.",
    "symptoms": ["Often no early symptoms", "Urinary problems", "Blood in urine or semen", "Bone pain (advanced)", "Erectile dysfunction", "Unexplained weight loss"],
    "precautions": ["Regular PSA screening (discuss with doctor)", "Healthy diet", "Regular exercise", "Regular medical checkups"],
    "when_to_seek_care": ["Urinary symptoms", "Blood in urine or semen", "Bone pain", "Unexplained weight loss"],
    "sources": [{"title": "ACS – Prostate Cancer", "url": "https://www.cancer.org/cancer/prostate-cancer.html"}],
    "confidence": "high"
  },
  "lung cancer": {
    "keywords": ["lung cancer", "pulmonary cancer", "lung tumor", "bronchogenic carcinoma"],
    "summary": "Cancer originating in the lungs.",
    "symptoms": ["Persistent cough", "Coughing up blood", "Shortness of breath", "Chest pain", "Hoarseness", "Weight loss", "Bone pain", "Headache"],
    "precautions": ["Stop smoking", "Avoid secondhand smoke", "Test home for radon", "Use protective equipment", "Annual CT scan for high-risk individuals"],
    "when_to_seek_care": ["Persistent cough", "Coughing blood", "New chest pain", "Unexplained weight loss"],
    "sources": [{"title": "ACS – Lung Cancer", "url": "https://www.cancer.org/cancer/lung-cancer.html"}],
    "confidence": "high"
  },
  "colorectal cancer": {
    "keywords": ["colorectal cancer", "colon cancer", "rectal cancer", "bowel cancer", "colon polyp"],
    "summary": "Cancer of the colon or rectum.",
    "symptoms": ["Change in bowel habits", "Blood in stool", "Persistent abdominal discomfort", "Feeling of incomplete evacuation", "Weakness and fatigue", "Unexplained weight loss"],
    "precautions": ["Regular colonoscopy after age 45", "Eat high-fiber diet", "Limit red and processed meat", "Exercise regularly", "Limit alcohol and don't smoke"],
    "when_to_seek_care": ["Blood in stool", "Significant change in bowel habits", "Abdominal pain", "Unexplained weight loss"],
    "sources": [{"title": "ACS – Colorectal Cancer", "url": "https://www.cancer.org/cancer/colon-rectal-cancer.html"}],
    "confidence": "high"
  },
  "cervical cancer": {
    "keywords": ["cervical cancer", "HPV cancer", "Pap smear abnormal", "cervical dysplasia"],
    "summary": "Cancer of the cervix, often caused by high-risk HPV strains.",
    "symptoms": ["Often no early symptoms", "Vaginal bleeding after sex, menopause, or between periods", "Watery, bloody vaginal discharge", "Pelvic pain during sex"],
    "precautions": ["Regular Pap smears and HPV tests", "HPV vaccination", "Safe sex practices", "Don't smoke"],
    "when_to_seek_care": ["Abnormal Pap smear result", "Unusual vaginal bleeding", "Vaginal discharge with odor"],
    "sources": [{"title": "WHO – Cervical Cancer", "url": "https://www.who.int/news-room/fact-sheets/detail/cervical-cancer"}],
    "confidence": "high"
  },
  "ovarian cancer": {
    "keywords": ["ovarian cancer", "ovarian tumor", "pelvic mass", "BRCA ovarian"],
    "summary": "Cancer originating in the ovaries.",
    "symptoms": ["Bloating", "Pelvic or abdominal pain", "Difficulty eating or feeling full quickly", "Urinary symptoms (urgency, frequency)", "Fatigue", "Back pain", "Constipation"],
    "precautions": ["Know family history (BRCA genes)", "Regular gynecological exams", "Discuss screening if high risk"],
    "when_to_seek_care": ["Persistent bloating", "Pelvic pain", "Difficulty eating", "Urinary symptoms with pelvic pain"],
    "sources": [{"title": "ACS – Ovarian Cancer", "url": "https://www.cancer.org/cancer/ovarian-cancer.html"}],
    "confidence": "high"
  },
  "leukemia": {
    "keywords": ["leukemia", "blood cancer", "bone marrow cancer", "white blood cell cancer", "CLL", "CML", "AML", "ALL"],
    "summary": "Cancer of blood-forming tissues, including bone marrow and lymphatic system.",
    "symptoms": ["Fatigue and weakness", "Frequent infections", "Weight loss", "Swollen lymph nodes", "Easy bruising or bleeding", "Fever or chills", "Bone pain", "Night sweats"],
    "precautions": ["Seek early diagnosis", "Chemotherapy and other treatments", "Infection prevention", "Regular monitoring"],
    "when_to_seek_care": ["Unexplained weight loss with fatigue", "Frequent infections", "Unusual bruising or bleeding", "Enlarged lymph nodes", "Night sweats with weight loss"],
    "sources": [{"title": "ACS – Leukemia", "url": "https://www.cancer.org/cancer/leukemia.html"}],
    "confidence": "high"
  },
  "lymphoma": {
    "keywords": ["lymphoma", "Hodgkin's lymphoma", "non-Hodgkin lymphoma", "lymph node cancer"],
    "summary": "Cancer that begins in infection-fighting cells of the immune system (lymphocytes).",
    "symptoms": ["Swollen lymph nodes (painless)", "Fatigue", "Fever", "Night sweats", "Weight loss", "Itching", "Shortness of breath"],
    "precautions": ["Seek medical evaluation for persistent lymph node swelling", "Treatment includes chemotherapy or radiation", "Regular monitoring"],
    "when_to_seek_care": ["Painless swollen lymph nodes lasting weeks", "Night sweats with weight loss", "Persistent fatigue with fever"],
    "sources": [{"title": "ACS – Lymphoma", "url": "https://www.cancer.org/cancer/hodgkin-lymphoma.html"}],
    "confidence": "high"
  },
  "myeloma": {
    "keywords": ["myeloma", "multiple myeloma", "plasma cell cancer", "bone marrow cancer myeloma"],
    "summary": "A cancer of plasma cells that accumulate in bone marrow.",
    "symptoms": ["Bone pain (especially back or chest)", "Fatigue and weakness", "Frequent infections", "Weight loss", "Kidney problems", "Elevated calcium"],
    "precautions": ["Chemotherapy and targeted therapy", "Bone-strengthening medications", "Hydration", "Regular monitoring"],
    "when_to_seek_care": ["Persistent unexplained bone pain", "Frequent infections with bone pain", "Kidney problems with bone pain"],
    "sources": [{"title": "ACS – Multiple Myeloma", "url": "https://www.cancer.org/cancer/multiple-myeloma.html"}],
    "confidence": "medium"
  },
  "thyroid cancer": {
    "keywords": ["thyroid cancer", "papillary thyroid cancer", "thyroid nodule", "thyroid tumor"],
    "summary": "Cancer originating in the thyroid gland cells.",
    "symptoms": ["Lump in neck", "Changes in voice (hoarseness)", "Difficulty swallowing", "Pain in neck and throat", "Swollen lymph nodes in neck"],
    "precautions": ["Regular thyroid examination", "Ultrasound and biopsy if nodule found", "Surgical treatment", "Thyroid hormone therapy post-surgery"],
    "when_to_seek_care": ["Neck lump", "Hoarseness lasting weeks", "Difficulty swallowing", "Neck pain with swollen nodes"],
    "sources": [{"title": "ACS – Thyroid Cancer", "url": "https://www.cancer.org/cancer/thyroid-cancer.html"}],
    "confidence": "high"
  },
  "bladder cancer": {
    "keywords": ["bladder cancer", "blood in urine cancer", "urothelial carcinoma", "bladder tumor"],
    "summary": "Cancer that begins in the cells of the bladder.",
    "symptoms": ["Blood in urine (hematuria)", "Frequent urination", "Painful urination", "Back or pelvic pain", "Urinary urgency"],
    "precautions": ["Stop smoking", "Avoid chemical exposure", "Drink plenty of water", "Regular medical checkups"],
    "when_to_seek_care": ["Blood in urine", "Unexplained urinary symptoms", "Pelvic pain with urinary issues"],
    "sources": [{"title": "ACS – Bladder Cancer", "url": "https://www.cancer.org/cancer/bladder-cancer.html"}],
    "confidence": "high"
  },
  "kidney cancer": {
    "keywords": ["kidney cancer", "renal cell carcinoma", "renal carcinoma", "kidney tumor"],
    "summary": "Cancer originating in the kidneys.",
    "symptoms": ["Blood in urine", "Back or side pain (flank)", "Mass in side or back", "Fatigue", "Weight loss", "Fever", "Anemia"],
    "precautions": ["Stop smoking", "Maintain healthy weight", "Control blood pressure", "Regular checkups"],
    "when_to_seek_care": ["Blood in urine", "Unexplained flank pain", "Mass in abdomen", "Weight loss with urinary symptoms"],
    "sources": [{"title": "ACS – Kidney Cancer", "url": "https://www.cancer.org/cancer/kidney-cancer.html"}],
    "confidence": "high"
  },
  "pancreatic cancer": {
    "keywords": ["pancreatic cancer", "cancer of the pancreas", "exocrine pancreatic cancer"],
    "summary": "Cancer that begins in the tissues of the pancreas.",
    "symptoms": ["Jaundice", "Abdominal pain radiating to back", "Weight loss and poor appetite", "Nausea and vomiting", "New-onset diabetes", "Depression", "Blood clots"],
    "precautions": ["Quit smoking", "Maintain healthy weight", "Limit alcohol", "Know family history"],
    "when_to_seek_care": ["Jaundice", "Unexplained weight loss", "Abdominal pain radiating to back", "New diabetes with weight loss"],
    "sources": [{"title": "ACS – Pancreatic Cancer", "url": "https://www.cancer.org/cancer/pancreatic-cancer.html"}],
    "confidence": "high"
  },
  "liver cancer": {
    "keywords": ["liver cancer", "hepatocellular carcinoma", "HCC", "hepatoma"],
    "summary": "Cancer that begins in the liver cells.",
    "symptoms": ["Weight loss", "Upper abdominal pain", "Nausea and vomiting", "General weakness", "Jaundice", "White, chalky stools", "Swollen abdomen"],
    "precautions": ["Hepatitis B and C treatment", "Avoid excessive alcohol", "Maintain healthy weight", "Regular screening if cirrhosis"],
    "when_to_seek_care": ["Jaundice", "Upper abdominal mass", "Worsening liver disease symptoms"],
    "sources": [{"title": "ACS – Liver Cancer", "url": "https://www.cancer.org/cancer/liver-cancer.html"}],
    "confidence": "high"
  },
  "stomach cancer": {
    "keywords": ["stomach cancer", "gastric cancer", "gastric adenocarcinoma"],
    "summary": "Cancer that begins in the cells lining the stomach.",
    "symptoms": ["Early: no symptoms", "Indigestion or heartburn", "Feeling full quickly", "Nausea", "Stomach pain", "Unexplained weight loss", "Blood in stool or vomit"],
    "precautions": ["Treat H. pylori infection", "Eat more fruits and vegetables", "Limit salt-preserved foods", "Don't smoke", "Maintain healthy weight"],
    "when_to_seek_care": ["Persistent indigestion", "Blood in stool or vomit", "Unexplained weight loss", "Abdominal mass"],
    "sources": [{"title": "ACS – Stomach Cancer", "url": "https://www.cancer.org/cancer/stomach-cancer.html"}],
    "confidence": "high"
  },
  "brain tumor": {
    "keywords": ["brain tumor", "brain cancer", "glioma", "meningioma", "glioblastoma"],
    "summary": "Growth of abnormal cells in the brain.",
    "symptoms": ["New or changed headache pattern", "Headaches more frequent and severe", "Nausea or vomiting", "Vision problems", "Gradual loss of sensation", "Difficulty with balance", "Speech difficulties", "Personality or behavior changes", "Seizures"],
    "precautions": ["Regular neurological monitoring", "Surgery, radiation, chemotherapy as planned", "Seizure precautions"],
    "when_to_seek_care": ["New onset seizures", "Rapidly progressive neurological symptoms", "Personality changes", "Vision loss", "Headaches with vomiting in morning"],
    "sources": [{"title": "ACS – Brain Tumors", "url": "https://www.cancer.org/cancer/brain-spinal-cord-tumors-adults.html"}],
    "confidence": "high"
  },
  "bone cancer": {
    "keywords": ["bone cancer", "osteosarcoma", "Ewing's sarcoma", "chondrosarcoma", "bone tumor"],
    "summary": "Cancer that begins in the bone or spreads to the bone.",
    "symptoms": ["Bone pain", "Swelling near bone", "Weakened bone leading to fractures", "Fatigue", "Weight loss"],
    "precautions": ["Seek medical evaluation for persistent bone pain", "Imaging and biopsy for diagnosis", "Multidisciplinary treatment"],
    "when_to_seek_care": ["Persistent unexplained bone pain in young person", "Bone pain waking from sleep", "Lump over bone"],
    "sources": [{"title": "ACS – Bone Cancer", "url": "https://www.cancer.org/cancer/bone-cancer.html"}],
    "confidence": "high"
  },
  "soft tissue sarcoma": {
    "keywords": ["sarcoma", "soft tissue sarcoma", "rhabdomyosarcoma", "liposarcoma"],
    "summary": "Cancer arising in soft tissues like muscle, fat, nerves, or blood vessels.",
    "symptoms": ["Painless lump or swelling", "Pain if tumor presses on nerves or muscles", "May grow very large before noticed"],
    "precautions": ["Seek evaluation for any growing lump", "Imaging and biopsy for diagnosis", "Specialized treatment center"],
    "when_to_seek_care": ["Any growing lump, especially >5cm", "Lump deep in muscle", "Painful lump"],
    "sources": [{"title": "ACS – Soft Tissue Sarcoma", "url": "https://www.cancer.org/cancer/soft-tissue-sarcoma.html"}],
    "confidence": "medium"
  },
  "testicular cancer": {
    "keywords": ["testicular cancer", "testicular tumor", "testicular lump"],
    "summary": "Cancer that develops in the testicles (testes).",
    "symptoms": ["Lump or enlargement in testicle", "Feeling of heaviness in scrotum", "Dull ache in abdomen or groin", "Sudden collection of fluid in scrotum", "Breast tenderness", "Back pain (metastatic)"],
    "precautions": ["Regular testicular self-exams", "Seek medical evaluation for any lump", "Treatment has high cure rates"],
    "when_to_seek_care": ["Any testicular lump", "Change in testicular size", "Testicular pain with lump"],
    "sources": [{"title": "ACS – Testicular Cancer", "url": "https://www.cancer.org/cancer/testicular-cancer.html"}],
    "confidence": "high"
  },
  "uterine cancer": {
    "keywords": ["uterine cancer", "endometrial cancer", "uterus cancer", "womb cancer"],
    "summary": "Cancer that begins in the uterus (endometrial cancer is most common type).",
    "symptoms": ["Abnormal vaginal bleeding", "Bleeding after menopause", "Pelvic pain", "Pain during sex", "Unusual discharge"],
    "precautions": ["Report any postmenopausal bleeding immediately", "Maintain healthy weight", "Manage estrogen levels", "Regular gynecological exams"],
    "when_to_seek_care": ["ANY postmenopausal vaginal bleeding", "Abnormal uterine bleeding at any age", "Pelvic pain with bleeding"],
    "sources": [{"title": "ACS – Uterine Cancer", "url": "https://www.cancer.org/cancer/uterine-cancer.html"}],
    "confidence": "high"
  },
  "Huntington's disease": {
    "keywords": ["Huntington's disease", "Huntington disease", "HD", "chorea", "huntingtin"],
    "summary": "A genetic disorder causing progressive breakdown of nerve cells in the brain.",
    "symptoms": ["Involuntary jerking movements (chorea)", "Balance and coordination problems", "Difficulty with speech and swallowing", "Cognitive decline", "Psychiatric symptoms", "Personality changes"],
    "precautions": ["Genetic counseling", "Medications for movement and psychiatric symptoms", "Physical and speech therapy", "Support groups"],
    "when_to_seek_care": ["Involuntary movements", "Cognitive or behavioral changes in at-risk individuals", "Swallowing difficulties"],
    "sources": [{"title": "HDSA – Huntington's", "url": "https://hdsa.org/"}],
    "confidence": "medium"
  },
  "amyotrophic lateral sclerosis": {
    "keywords": ["ALS", "amyotrophic lateral sclerosis", "Lou Gehrig's disease", "motor neuron disease"],
    "summary": "A progressive nervous system disease affecting nerve cells in the brain and spinal cord.",
    "symptoms": ["Muscle weakness and twitching", "Difficulty with speech", "Difficulty swallowing", "Difficulty breathing", "Muscle cramps", "Cognitive changes in some"],
    "precautions": ["Multidisciplinary care team", "Riluzole and other medications", "Respiratory support", "Nutritional support", "Physical and occupational therapy"],
    "when_to_seek_care": ["Unexplained muscle weakness", "Slurred speech with weakness", "Difficulty swallowing with weakness"],
    "sources": [{"title": "ALS Association", "url": "https://www.als.org/"}],
    "confidence": "high"
  },
  "Guillain-Barré syndrome": {
    "keywords": ["Guillain-Barré", "GBS", "ascending paralysis", "post-infectious paralysis", "peripheral neuropathy"],
    "summary": "A rare disorder where the immune system attacks the peripheral nervous system.",
    "symptoms": ["Tingling and weakness starting in feet", "Weakness spreading upward", "Severe pain", "Difficulty walking", "Eye and facial movement problems", "Rapid heart rate"],
    "precautions": ["Seek emergency care", "Hospitalization required", "IVIG or plasmapheresis treatment"],
    "when_to_seek_care": ["ANY ascending weakness starting after illness", "Emergency – rapid progression can cause breathing failure"],
    "sources": [{"title": "Mayo Clinic – GBS", "url": "https://www.mayoclinic.org/diseases-conditions/guillain-barre-syndrome/symptoms-causes/syc-20350382"}],
    "confidence": "high"
  },
  "spina bifida": {
    "keywords": ["spina bifida", "neural tube defect", "meningomyelocele", "spinal defect birth"],
    "summary": "A birth defect where the spine and spinal cord don't form properly.",
    "symptoms": ["Visible gap or opening in spine", "Paralysis or weakness in legs", "Bowel and bladder dysfunction", "Learning disabilities", "Hydrocephalus", "Tethered spinal cord"],
    "precautions": ["Folic acid before and during pregnancy", "Regular medical follow-up", "Surgical repair at birth", "Physical therapy", "Bladder and bowel management"],
    "when_to_seek_care": ["Urinary tract symptoms", "Changes in neurological function", "Signs of shunt malfunction", "Tethered cord symptoms"],
    "sources": [{"title": "CDC – Spina Bifida", "url": "https://www.cdc.gov/ncbddd/spinabifida/index.html"}],
    "confidence": "high"
  },
  "cerebral palsy": {
    "keywords": ["cerebral palsy", "CP", "brain damage movement disorder", "spastic cerebral palsy"],
    "summary": "A group of disorders affecting movement and muscle tone from brain damage.",
    "symptoms": ["Stiff muscles (spasticity)", "Exaggerated reflexes", "Lack of balance and coordination", "Involuntary movements", "Delayed motor milestones", "Difficulty walking or talking"],
    "precautions": ["Physical and occupational therapy", "Speech therapy", "Medications for spasticity", "Assistive devices", "Regular medical follow-up"],
    "when_to_seek_care": ["Motor developmental delay in infant", "Regression of motor skills", "New seizures"],
    "sources": [{"title": "CDC – Cerebral Palsy", "url": "https://www.cdc.gov/ncbddd/cp/index.html"}],
    "confidence": "high"
  },
  "Down syndrome": {
    "keywords": ["Down syndrome", "trisomy 21", "Down's syndrome", "chromosomal disorder trisomy"],
    "summary": "A genetic disorder caused by an extra chromosome 21.",
    "symptoms": ["Distinct facial features", "Intellectual disability", "Developmental delays", "Heart defects (common)", "Hearing and vision problems", "Thyroid issues"],
    "precautions": ["Early intervention programs", "Heart evaluation in newborns", "Regular hearing and vision checks", "Thyroid monitoring", "Speech and occupational therapy"],
    "when_to_seek_care": ["Cardiac symptoms", "Respiratory problems", "Developmental regression", "Thyroid symptoms"],
    "sources": [{"title": "CDC – Down Syndrome", "url": "https://www.cdc.gov/ncbddd/birthdefects/downsyndrome.html"}],
    "confidence": "high"
  },
  "fragile X syndrome": {
    "keywords": ["fragile X", "fragile X syndrome", "FXS", "intellectual disability genetic"],
    "summary": "A genetic condition causing intellectual disability and behavioral challenges.",
    "symptoms": ["Intellectual disability", "Learning disabilities", "Attention and behavior problems", "Social anxiety", "Delayed speech", "Physical features (long face, large ears)"],
    "precautions": ["Early intervention", "Speech and occupational therapy", "Behavioral therapy", "Medications for behavioral symptoms"],
    "when_to_seek_care": ["Developmental delays", "Behavioral concerns in young child", "Family history of intellectual disability"],
    "sources": [{"title": "CDC – Fragile X", "url": "https://www.cdc.gov/ncbddd/fxs/index.html"}],
    "confidence": "medium"
  },
  "phenylketonuria": {
    "keywords": ["phenylketonuria", "PKU", "phenylalanine metabolism", "inborn error metabolism"],
    "summary": "A metabolic disorder causing phenylalanine buildup in the body.",
    "symptoms": ["Without treatment: intellectual disability", "Behavioral problems", "Seizures", "Light skin and eyes (untreated)"],
    "precautions": ["Newborn screening", "Strict low-phenylalanine diet", "Medical formula", "Regular monitoring", "Medications (sapropterin for some)"],
    "when_to_seek_care": ["Positive newborn screening", "Developmental regression despite diet", "Seizures"],
    "sources": [{"title": "NORD – PKU", "url": "https://rarediseases.org/rare-diseases/phenylketonuria/"}],
    "confidence": "medium"
  },
  "Marfan syndrome": {
    "keywords": ["Marfan syndrome", "Marfan's", "connective tissue disorder hereditary", "aortic root dilatation genetic"],
    "summary": "A genetic connective tissue disorder affecting the heart, eyes, and skeleton.",
    "symptoms": ["Tall, slender build", "Long arms, legs, and fingers", "Flexible joints", "Curved spine", "Aortic aneurysm risk", "Lens dislocation in eye", "Chest deformity"],
    "precautions": ["Regular cardiac monitoring", "Beta-blockers or ARBs for aorta", "Avoid contact sports", "Regular eye exams", "Genetic counseling"],
    "when_to_seek_care": ["Sudden chest or back pain (aortic dissection)", "Vision changes", "Chest deformity", "Tall stature with eye or heart concerns"],
    "sources": [{"title": "Mayo Clinic – Marfan Syndrome", "url": "https://www.mayoclinic.org/diseases-conditions/marfan-syndrome/symptoms-causes/syc-20350782"}],
    "confidence": "medium"
  },
  "Ehlers-Danlos syndrome": {
    "keywords": ["Ehlers-Danlos", "EDS", "hypermobile joints", "connective tissue disorder skin", "skin hyperextensibility"],
    "summary": "A group of inherited connective tissue disorders affecting skin, joints, and vessels.",
    "symptoms": ["Overly flexible joints", "Stretchy or fragile skin", "Chronic joint pain", "Easy bruising", "Slow wound healing", "Scoliosis"],
    "precautions": ["Physical therapy for joint stability", "Protective padding", "Low-impact exercise", "Avoid joint locking", "Cardiovascular monitoring for vascular EDS"],
    "when_to_seek_care": ["Joint dislocations", "Vascular EDS: any sudden pain", "Skin tearing", "Cardiovascular complications"],
    "sources": [{"title": "EDS Society", "url": "https://www.ehlers-danlos.com/"}],
    "confidence": "medium"
  },
  "hemophilia": {
    "keywords": ["hemophilia", "haemophilia", "clotting disorder", "bleeding disorder", "factor deficiency"],
    "summary": "A rare disorder where blood doesn't clot normally due to lack of clotting factors.",
    "symptoms": ["Excessive bleeding from cuts", "Prolonged bleeding after surgery or dental procedures", "Spontaneous bleeding into joints or muscles", "Blood in urine or stool", "Frequent nosebleeds"],
    "precautions": ["Factor replacement therapy", "Avoid blood thinners", "Medical alert bracelet", "Protective equipment for activities", "Regular hematology follow-up"],
    "when_to_seek_care": ["Uncontrolled bleeding", "Bleeding into joints", "Head trauma", "Blood in urine or stool", "Before surgery or dental procedures"],
    "sources": [{"title": "CDC – Hemophilia", "url": "https://www.cdc.gov/ncbddd/hemophilia/index.html"}],
    "confidence": "high"
  },
  "von Willebrand disease": {
    "keywords": ["von Willebrand disease", "vWD", "bleeding disorder mild", "vWF deficiency"],
    "summary": "A bleeding disorder caused by deficient or defective von Willebrand factor.",
    "symptoms": ["Heavy or prolonged menstrual periods", "Frequent nosebleeds", "Bleeding gums", "Easy bruising", "Prolonged bleeding from cuts", "Heavy bleeding from surgery"],
    "precautions": ["Desmopressin for mild cases", "Factor replacement", "Avoid aspirin and NSAIDs", "Inform medical providers"],
    "when_to_seek_care": ["Excessive menstrual bleeding", "Uncontrolled nosebleeds", "Prolonged bleeding after surgery or dental procedures"],
    "sources": [{"title": "CDC – vWD", "url": "https://www.cdc.gov/ncbddd/vwd/index.html"}],
    "confidence": "medium"
  },
  "thalassemia": {
    "keywords": ["thalassemia", "thalassaemia", "beta thalassemia", "alpha thalassemia", "hemoglobin disorder genetic"],
    "summary": "An inherited blood disorder where the body makes less hemoglobin than normal.",
    "symptoms": ["Fatigue and weakness", "Pale skin", "Jaundice", "Facial bone deformities", "Slow growth", "Abdominal swelling (enlarged spleen)", "Dark urine"],
    "precautions": ["Regular blood transfusions if severe", "Iron chelation therapy", "Folic acid supplements", "Bone marrow transplant option", "Genetic counseling"],
    "when_to_seek_care": ["Severe fatigue with pale skin", "Signs of iron overload", "Abdominal swelling", "Infections in transfusion-dependent patients"],
    "sources": [{"title": "CDC – Thalassemia", "url": "https://www.cdc.gov/ncbddd/thalassemia/index.html"}],
    "confidence": "high"
  },
  "polycythemia vera": {
    "keywords": ["polycythemia vera", "PV", "too many red blood cells", "myeloproliferative"],
    "summary": "A blood cancer causing overproduction of red blood cells.",
    "symptoms": ["Itching after warm bath", "Headache", "Dizziness", "Redness of skin (face, hands)", "Fatigue", "Night sweats", "Vision problems", "Blood clot risk"],
    "precautions": ["Phlebotomy treatment", "Low-dose aspirin", "Regular hematology follow-up", "Stay hydrated", "Hydroxyurea if indicated"],
    "when_to_seek_care": ["Blood clot symptoms", "Stroke symptoms", "Severe headache", "Abdominal pain (enlarged spleen)"],
    "sources": [{"title": "Mayo Clinic – Polycythemia Vera", "url": "https://www.mayoclinic.org/diseases-conditions/polycythemia-vera/symptoms-causes/syc-20355850"}],
    "confidence": "medium"
  },
  "Raynaud's phenomenon": {
    "keywords": ["Raynaud's", "Raynaud's phenomenon", "Raynaud's disease", "cold hands color change", "white blue red fingers cold"],
    "summary": "A condition causing blood vessels in fingers and toes to narrow in response to cold or stress.",
    "symptoms": ["Fingers or toes turning white, blue, then red", "Tingling and numbness", "Cold extremities", "Pain and throbbing on rewarming"],
    "precautions": ["Keep warm in cold weather", "Layer clothing", "Hand warmers", "Avoid smoking", "Manage stress", "Medications if severe"],
    "when_to_seek_care": ["Sores or ulcers on fingers", "Symptoms getting worse", "Associated with autoimmune disease symptoms", "Secondary Raynaud's (new onset in older adult)"],
    "sources": [{"title": "Mayo Clinic – Raynaud's", "url": "https://www.mayoclinic.org/diseases-conditions/raynauds-disease/symptoms-causes/syc-20353519"}],
    "confidence": "high"
  },
  "Sjögren's syndrome": {
    "keywords": ["Sjögren's syndrome", "Sjogren's", "dry eyes dry mouth autoimmune", "sicca syndrome"],
    "summary": "An autoimmune disease that attacks moisture-producing glands causing dry eyes and mouth.",
    "symptoms": ["Dry eyes (gritty, burning)", "Dry mouth", "Difficulty swallowing", "Fatigue", "Joint pain", "Skin rashes", "Vaginal dryness"],
    "precautions": ["Artificial tears", "Saliva substitutes", "Stay hydrated", "Good dental hygiene", "Medications as prescribed"],
    "when_to_seek_care": ["Corneal problems from dry eyes", "Difficulty swallowing", "Systemic complications", "New neurological symptoms"],
    "sources": [{"title": "Sjögren's Foundation", "url": "https://www.sjogrens.org/"}],
    "confidence": "high"
  },
  "scleroderma": {
    "keywords": ["scleroderma", "systemic sclerosis", "skin hardening autoimmune", "CREST syndrome"],
    "summary": "A group of rare diseases involving hardening and tightening of skin and connective tissues.",
    "symptoms": ["Hardened, thickened skin patches", "Raynaud's phenomenon", "Acid reflux", "Difficulty swallowing", "Shortness of breath", "Joint pain and stiffness"],
    "precautions": ["Treat specific organ complications", "Physical therapy", "Protect from cold", "Regular organ monitoring", "Medications as prescribed"],
    "when_to_seek_care": ["Worsening breathing", "New cardiac symptoms", "Severe Raynaud's with sores", "Renal crisis (severe high BP)"],
    "sources": [{"title": "Mayo Clinic – Scleroderma", "url": "https://www.mayoclinic.org/diseases-conditions/scleroderma/symptoms-causes/syc-20351952"}],
    "confidence": "medium"
  },
  "polymyositis": {
    "keywords": ["polymyositis", "dermatomyositis", "inflammatory muscle disease", "myositis"],
    "summary": "An inflammatory disease causing muscle weakness and sometimes skin rashes.",
    "symptoms": ["Progressive muscle weakness (proximal)", "Difficulty rising from sitting", "Difficulty lifting arms overhead", "Skin rash (dermatomyositis)", "Difficulty swallowing", "Fatigue"],
    "precautions": ["Corticosteroids and immunosuppressants", "Physical therapy", "Nutrition management (if dysphagia)", "Cancer screening (associated)"],
    "when_to_seek_care": ["Rapidly progressive muscle weakness", "Difficulty swallowing", "Breathing difficulty", "New skin rash with weakness"],
    "sources": [{"title": "Mayo Clinic – Polymyositis", "url": "https://www.mayoclinic.org/diseases-conditions/polymyositis/symptoms-causes/syc-20353690"}],
    "confidence": "medium"
  },
  "vasculitis": {
    "keywords": ["vasculitis", "blood vessel inflammation", "polyarteritis", "Wegener's granulomatosis", "GPA"],
    "summary": "Inflammation of blood vessels that can affect blood flow to organs.",
    "symptoms": ["Fever", "Fatigue and weight loss", "Headache", "Rash", "Numbness or weakness", "Organ-specific symptoms (kidney, lung, etc.)", "Joint pain"],
    "precautions": ["Corticosteroids and immunosuppressants", "Regular organ monitoring", "Prevent infections", "Regular medical follow-up"],
    "when_to_seek_care": ["Any suspected vasculitis", "Organ-threatening symptoms", "Rapid progression"],
    "sources": [{"title": "Mayo Clinic – Vasculitis", "url": "https://www.mayoclinic.org/diseases-conditions/vasculitis/symptoms-causes/syc-20363435"}],
    "confidence": "medium"
  },
  "temporal arteritis": {
    "keywords": ["temporal arteritis", "giant cell arteritis", "GCA", "scalp tenderness headache elderly"],
    "summary": "Inflammation of the temporal arteries that supply blood to the head and brain.",
    "symptoms": ["Severe headache (usually one-sided)", "Scalp tenderness", "Jaw pain when chewing (claudication)", "Temporal artery tenderness", "Vision disturbances", "Fever", "Fatigue"],
    "precautions": ["Immediate high-dose steroids to prevent blindness", "Seek urgent care", "Regular ESR/CRP monitoring"],
    "when_to_seek_care": ["URGENT – vision loss or visual disturbance with headache in person over 50", "Any suspected GCA", "Sudden vision changes in elderly"],
    "sources": [{"title": "Mayo Clinic – Giant Cell Arteritis", "url": "https://www.mayoclinic.org/diseases-conditions/giant-cell-arteritis/symptoms-causes/syc-20372758"}],
    "confidence": "high"
  },
  "polymyalgia rheumatica": {
    "keywords": ["polymyalgia rheumatica", "PMR", "shoulder hip girdle pain elderly", "morning stiffness elderly"],
    "summary": "An inflammatory disorder causing muscle pain and stiffness in shoulders and hips.",
    "symptoms": ["Aching in shoulders, neck, upper arms, hips, and thighs", "Morning stiffness lasting more than 45 minutes", "Limited range of motion", "Fatigue", "Mild fever", "Loss of appetite"],
    "precautions": ["Corticosteroids as prescribed", "Regular ESR/CRP monitoring", "Watch for giant cell arteritis", "Exercise within tolerance"],
    "when_to_seek_care": ["Visual symptoms (GCA risk)", "Sudden severe headache", "Jaw pain when chewing"],
    "sources": [{"title": "Mayo Clinic – Polymyalgia Rheumatica", "url": "https://www.mayoclinic.org/diseases-conditions/polymyalgia-rheumatica/symptoms-causes/syc-20353411"}],
    "confidence": "medium"
  },
  "Paget's disease of bone": {
    "keywords": ["Paget's disease bone", "osteitis deformans", "bone Paget's"],
    "summary": "A chronic disorder disrupting normal bone remodeling causing enlarged and deformed bones.",
    "symptoms": ["Bone pain", "Enlarged or misshapen bones", "Bone fractures", "Hearing loss (skull involvement)", "Headache", "Bowing of legs"],
    "precautions": ["Bisphosphonate medications", "Adequate calcium and Vitamin D", "Regular bone monitoring", "Hearing aids if needed"],
    "when_to_seek_care": ["Bone pain in older adult", "Hearing loss with bone symptoms", "Fracture from minimal trauma"],
    "sources": [{"title": "Mayo Clinic – Paget's Disease", "url": "https://www.mayoclinic.org/diseases-conditions/pagets-disease-of-bone/symptoms-causes/syc-20350811"}],
    "confidence": "medium"
  },
  "septic arthritis": {
    "keywords": ["septic arthritis", "infectious arthritis", "joint infection", "pyarthrosis"],
    "summary": "A painful joint infection caused by bacteria, viruses, or fungi.",
    "symptoms": ["Severe joint pain", "Swelling", "Warmth and redness", "Fever and chills", "Inability to move joint", "Usually single joint affected"],
    "precautions": ["URGENT – requires immediate medical treatment", "IV antibiotics", "Joint drainage", "Hospitalization usually required"],
    "when_to_seek_care": ["ANY suspected septic arthritis – urgent care", "Sudden severe joint pain with fever"],
    "sources": [{"title": "Mayo Clinic – Septic Arthritis", "url": "https://www.mayoclinic.org/diseases-conditions/infectious-arthritis/symptoms-causes/syc-20352875"}],
    "confidence": "high"
  },
  "tendinitis": {
    "keywords": ["tendinitis", "tendinopathy", "tendon pain", "rotator cuff tendinitis", "patellar tendinitis"],
    "summary": "Inflammation or irritation of a tendon, usually from overuse.",
    "symptoms": ["Pain at the site of tendon (worsens with movement)", "Mild swelling", "Tenderness to touch", "Dull ache at rest"],
    "precautions": ["Rest from aggravating activities", "Ice therapy", "Physical therapy exercises", "Anti-inflammatory medications", "Modify technique"],
    "when_to_seek_care": ["Severe pain limiting activity", "Complete tendon rupture (sudden severe pain with weakness)", "Not improving with rest"],
    "sources": [{"title": "Mayo Clinic – Tendinitis", "url": "https://www.mayoclinic.org/diseases-conditions/tendinitis/symptoms-causes/syc-20378243"}],
    "confidence": "high"
  },
  "bursitis": {
    "keywords": ["bursitis", "bursa inflammation", "shoulder bursitis", "hip bursitis", "prepatellar bursitis"],
    "summary": "Inflammation of the bursae (fluid-filled sacs) near joints.",
    "symptoms": ["Joint pain and tenderness", "Swelling", "Warm to touch", "Restricted movement", "Dull ache or stiffness"],
    "precautions": ["Rest and avoid aggravating activities", "Ice therapy", "Anti-inflammatory medications", "Physical therapy", "Protective padding"],
    "when_to_seek_care": ["Fever with bursitis (infected bursa)", "Severe pain", "Skin redness over bursa", "Not improving in 1-2 weeks"],
    "sources": [{"title": "Mayo Clinic – Bursitis", "url": "https://www.mayoclinic.org/diseases-conditions/bursitis/symptoms-causes/syc-20353242"}],
    "confidence": "high"
  },
  "frozen shoulder": {
    "keywords": ["frozen shoulder", "adhesive capsulitis", "shoulder stiffness", "shoulder capsule"],
    "summary": "Stiffness and pain in the shoulder joint that progressively worsens.",
    "symptoms": ["Shoulder stiffness", "Dull, aching shoulder pain", "Pain worse at night", "Progressive loss of range of motion", "Difficult to perform daily activities"],
    "precautions": ["Physical therapy (key treatment)", "Pain management", "Anti-inflammatory medications", "Corticosteroid injections", "Surgical hydrodilatation if severe"],
    "when_to_seek_care": ["Progressively worsening shoulder stiffness", "Significant functional limitation", "Not improving with physical therapy"],
    "sources": [{"title": "Mayo Clinic – Frozen Shoulder", "url": "https://www.mayoclinic.org/diseases-conditions/frozen-shoulder/symptoms-causes/syc-20372684"}],
    "confidence": "high"
  },
  "trigger finger": {
    "keywords": ["trigger finger", "trigger thumb", "stenosing tenosynovitis", "finger locking"],
    "summary": "A condition where a finger gets stuck in a bent position.",
    "symptoms": ["Finger stiffness (especially in morning)", "Popping or clicking sensation", "Finger locking in bent position", "Tender lump at base of finger"],
    "precautions": ["Rest finger", "Anti-inflammatory medications", "Splinting", "Corticosteroid injection", "Surgery if persistent"],
    "when_to_seek_care": ["Finger locked in position", "Significant functional limitation", "Not responding to conservative treatment"],
    "sources": [{"title": "Mayo Clinic – Trigger Finger", "url": "https://www.mayoclinic.org/diseases-conditions/trigger-finger/symptoms-causes/syc-20365100"}],
    "confidence": "high"
  },
  "ganglion cyst": {
    "keywords": ["ganglion cyst", "wrist cyst", "ganglion", "fluid cyst joint"],
    "summary": "Noncancerous lumps that most commonly develop along tendons or joints of wrists and hands.",
    "symptoms": ["Lump (most on wrist, foot)", "May be soft or firm", "Pain if pressing on nerve", "Reduced range of motion", "Tingling if near nerve"],
    "precautions": ["Often resolves on own", "Aspiration or surgery if symptomatic", "Wrist splinting"],
    "when_to_seek_care": ["Pain from cyst", "Functional limitation", "Cyst growing rapidly"],
    "sources": [{"title": "Mayo Clinic – Ganglion Cyst", "url": "https://www.mayoclinic.org/diseases-conditions/ganglion-cyst/symptoms-causes/syc-20350157"}],
    "confidence": "high"
  },
  "De Quervain's tenosynovitis": {
    "keywords": ["De Quervain's", "de quervain", "thumb pain side", "radial side wrist pain"],
    "summary": "A painful condition affecting the tendons on the thumb side of the wrist.",
    "symptoms": ["Pain and swelling at base of thumb", "Difficulty grasping or pinching", "Pain when moving thumb", "Positive Finkelstein test"],
    "precautions": ["Rest and splinting (thumb and wrist)", "Ice therapy", "Anti-inflammatory medications", "Corticosteroid injection", "Activity modification"],
    "when_to_seek_care": ["Pain limiting function", "Not improving with rest", "Numbness or tingling"],
    "sources": [{"title": "Mayo Clinic – De Quervain's", "url": "https://www.mayoclinic.org/diseases-conditions/de-quervains-tenosynovitis/symptoms-causes/syc-20371316"}],
    "confidence": "high"
  },
  "Morton's neuroma": {
    "keywords": ["Morton's neuroma", "foot nerve pain", "interdigital neuroma", "ball of foot pain"],
    "summary": "Thickening of tissue around the nerves between the toes, causing ball-of-foot pain.",
    "symptoms": ["Burning pain in ball of foot", "Sensation of walking on a pebble", "Pain between third and fourth toes", "Numbness or tingling in toes", "Pain worse with tight shoes"],
    "precautions": ["Wear wide, low-heeled shoes", "Metatarsal pads", "Ice therapy", "Corticosteroid injection", "Surgery if severe"],
    "when_to_seek_care": ["Persistent foot pain", "Numbness", "Not responding to shoe changes"],
    "sources": [{"title": "Mayo Clinic – Morton's Neuroma", "url": "https://www.mayoclinic.org/diseases-conditions/mortons-neuroma/symptoms-causes/syc-20350368"}],
    "confidence": "high"
  }
}

print(f"Total diseases: {len(diseases)}")
output_path = "backend/symptoms.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(diseases, f, indent=2, ensure_ascii=False)
print(f"Saved to {output_path}")
print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")
# ================== ADD THIS AT END ==================

def generate_response(query):
    """
    Main function used by app.py
    Converts user input into structured medical-style response
    """

    query = query.lower()
    matched = []

    # Match diseases using keywords
    for disease, info in diseases.items():
        for keyword in info["keywords"]:
            if keyword in query:
                matched.append((disease, info))
                break

    # If no match found
    if not matched:
        return {
            "possible_conditions": ["General illness / unclear symptoms"],
            "reason": "Symptoms do not clearly match a specific condition. More details needed.",
            "precautions": ["Monitor symptoms", "Stay hydrated", "Consult doctor if worsens"],
            "when_to_see_doctor": ["If symptoms persist or worsen"]
        }

    # Take best match
    disease, info = matched[0]

    return {
        "possible_conditions": [disease.title()],
        "reason": f"The symptoms you provided match common indicators of {disease}.",
        "symptoms": info.get("symptoms", []),
        "precautions": info.get("precautions", []),
        "when_to_see_doctor": info.get("when_to_seek_care", [])
    }
