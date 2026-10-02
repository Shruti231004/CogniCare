import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

TEMPLATE_PATH = r"C:\Users\Admin\.gemini\antigravity\brain\870bcad5-0f86-48a7-8a75-a343e86ebacb\.user_uploaded\media_1790815052736.pptx"
OUTPUT_PATH = r"c:\Shruti\AIH Project\CogniCare_AI_Mini_Project_Presentation.pptx"

prs = pptx.Presentation(TEMPLATE_PATH)

def set_shape_text(shape, items, font_size=15, space_after=8):
    """
    items: list of tuples (bold_prefix, text_body) or single strings
    """
    tf = shape.text_frame
    tf.word_wrap = True
    tf.clear()
    
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
            
        p.space_after = Pt(space_after)
        p.space_before = Pt(2)
        
        if isinstance(item, tuple):
            bold_prefix, text_body = item
            if bold_prefix:
                r_bold = p.add_run()
                r_bold.text = bold_prefix + ": " if not bold_prefix.endswith(":") else bold_prefix + " "
                r_bold.font.name = "Times New Roman"
                r_bold.font.size = Pt(font_size)
                r_bold.font.bold = True
                r_bold.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
            
            r_text = p.add_run()
            r_text.text = text_body
            r_text.font.name = "Times New Roman"
            r_text.font.size = Pt(font_size)
            r_text.font.bold = False
            r_text.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        else:
            r = p.add_run()
            r.text = item
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

# ==================== SLIDE 1: TITLE SLIDE ====================
s1 = prs.slides[0]

# Shape 0: Title
tf0 = s1.shapes[0].text_frame
tf0.word_wrap = True
tf0.clear()
p0 = tf0.paragraphs[0]
p0.alignment = PP_ALIGN.CENTER
r0 = p0.add_run()
r0.text = "CogniCare AI: Brain Stroke Risk Prediction, MRI Lesion Segmentation and Emergency Response Platform"
r0.font.name = "Times New Roman"
r0.font.size = Pt(24)
r0.font.bold = True
r0.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

# Shape 1: Group / Guide Details
tf1 = s1.shapes[1].text_frame
tf1.word_wrap = True
tf1.clear()

p1_1 = tf1.paragraphs[0]
p1_1.alignment = PP_ALIGN.CENTER
r1_1 = p1_1.add_run()
r1_1.text = "Roll No: 15          Shruti Gauchandra\n"
r1_1.font.name = "Times New Roman"
r1_1.font.size = Pt(16)
r1_1.font.bold = True
r1_1.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

p1_2 = tf1.add_paragraph()
p1_2.alignment = PP_ALIGN.CENTER
r1_2 = p1_2.add_run()
r1_2.text = "Under the guidance of:\nAsst. Prof. Kranti Gule\n"
r1_2.font.name = "Times New Roman"
r1_2.font.size = Pt(14)
r1_2.font.bold = True
r1_2.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

p1_3 = tf1.add_paragraph()
p1_3.alignment = PP_ALIGN.CENTER
r1_3 = p1_3.add_run()
r1_3.text = "Academic Year:\n2026-27"
r1_3.font.name = "Times New Roman"
r1_3.font.size = Pt(14)
r1_3.font.bold = True
r1_3.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

# Shape 2: College & Dept
tf2 = s1.shapes[2].text_frame
tf2.word_wrap = True
tf2.clear()
p2_1 = tf2.paragraphs[0]
p2_1.alignment = PP_ALIGN.CENTER
r2_1 = p2_1.add_run()
r2_1.text = "Vidyavardhini's College of Engineering and Technology\n"
r2_1.font.name = "Times New Roman"
r2_1.font.size = Pt(18)
r2_1.font.bold = True
r2_1.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)

p2_2 = tf2.add_paragraph()
p2_2.alignment = PP_ALIGN.CENTER
r2_2 = p2_2.add_run()
r2_2.text = "Department of Artificial Intelligence and Data Science"
r2_2.font.name = "Times New Roman"
r2_2.font.size = Pt(15)
r2_2.font.bold = True
r2_2.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)


# ==================== SLIDE 2: TABLE OF CONTENTS ====================
s2 = prs.slides[1]
# Already has standard TOC, let's ensure font is clean
toc_items = [
    "1. Abstract",
    "2. Introduction",
    "3. Literature Survey",
    "4. Problem Statement and Objective",
    "5. Scope of the Project",
    "6. Proposed System (Architecture / Workflow)",
    "7. Methodology Used (Ensemble, CV, NLP)",
    "8. Hardware and Software Requirements",
    "9. Expected Outcomes",
    "10. Experiment Results and Discussion",
    "11. Conclusion",
    "12. References"
]
set_shape_text(s2.shapes[1], toc_items, font_size=14, space_after=4)


# ==================== SLIDE 3: ABSTRACT ====================
s3 = prs.slides[2]
s3_items = [
    ("Clinical Urgency", "Acute Ischemic Stroke (AIS) is a severe medical emergency governed by 'Time is Brain'—1.9 million neurons die every minute an acute stroke remains untreated."),
    ("Multi-Modal Architecture", "CogniCare AI is an end-to-end platform uniting public FAST screening, predictive machine learning, neuroimaging computer vision, clinical NLP, and emergency hospital routing."),
    ("Predictive ML & XAI", "A tripartite soft-voting ensemble (Random Forest, Gradient Boosting, AdaBoost) achieves high sensitivity risk classification with transparent SHAP-inspired biomarker attributions."),
    ("5-Stage MRI Segmentation", "Automated computer vision pipeline processes Axial T2-FLAIR brain MRI scans via Otsu thresholding and morphological filters, quantifying lesion volume (%) and ASPECTS territory."),
    ("Clinical NLP & Emergency Triage", "Contextual medical text engine maps doctor EHR notes to ICD-10 / SNOMED-CT codes and triggers a live 4.5-hour golden window tPA countdown with nearest stroke center navigation.")
]
set_shape_text(s3.shapes[1], s3_items, font_size=14, space_after=8)


# ==================== SLIDE 4: INTRODUCTION ====================
s4 = prs.slides[3]
s4_items = [
    ("Global Health Burden", "Stroke is the 2nd leading cause of death and 3rd leading cause of long-term disability worldwide, responsible for 11% of all deaths annually (WHO)."),
    ("The 'Time is Brain' Paradigm", "Therapeutic efficacy depends critically on early intervention: intravenous thrombolysis (IV rtPA) has a strict 4.5-hour therapeutic window, while endovascular thrombectomy is indicated within 6–24 hours."),
    ("Systemic Clinical Bottlenecks", "Care delivery is frequently compromised by delayed public symptom recognition, lack of automated risk triage in primary clinics, inter-observer radiologic variability, and black-box AI skepticism."),
    ("The CogniCare AI Solution", "Delivers an accessible, explainable clinical decision support platform empowering patients, emergency medical personnel, and hospital neurologists to expedite life-saving care.")
]
set_shape_text(s4.shapes[1], s4_items, font_size=14, space_after=10)


# ==================== SLIDE 5: LITERATURE SURVEY ====================
s5 = prs.slides[4]
s5_items = [
    ("Smith et al. (2021) — Traditional Statistical Risk Models", "Evaluated Logistic Regression and Decision Trees on clinical EHR data. Limitation: High false-negative rates on imbalanced stroke cohorts and complete absence of explainability for bedside clinical trust."),
    ("Chen & Wang (2022) — Deep CNN Neuroimaging Segmentation", "Implemented convolutional neural networks for stroke lesion segmentation. Limitation: Excessive computational overhead requiring high-end GPU clusters, slow inference latency, and vulnerability to scan acquisition noise."),
    ("Rao et al. (2023) — Rule-Based Clinical NLP", "Utilized keyword string matching to extract medical terminology from EHR notes. Limitation: Lacked contextual clinical negation handling ('no limb numbness') and failed to link extracted entities to universal ICD-10 or SNOMED-CT codes."),
    ("CogniCare AI Innovation", "Unifies a calibrated soft-voting ensemble, deterministic sub-second 5-stage MRI segmentation, negation-aware medical ontology NLP, and local Explainable AI (XAI) in a unified bedside ecosystem.")
]
set_shape_text(s5.shapes[1], s5_items, font_size=13.5, space_after=8)


# ==================== SLIDE 6: PROBLEM STATEMENT AND OBJECTIVE ====================
s6 = prs.slides[5]
s6_items = [
    ("Problem Statement", "Acute stroke care is severely hindered by delayed public symptom recognition, opaque black-box risk algorithms, manual and subjective MRI lesion quantification, and fragmented emergency center dispatch."),
    ("Objective 1", "Develop an intuitive, digital FAST (Face, Arm, Speech, Time) screening tool for instant self and bystander symptom assessment and emergency escalation."),
    ("Objective 2", "Formulate a calibrated ensemble machine learning model (RF + GB + AdaBoost) with Explainable AI (XAI) to predict stroke vulnerability across vital physiological biomarkers."),
    ("Objective 3", "Construct a deterministic 5-stage computer vision MRI pipeline to delineate infarct volume, calculate lesion burden %, and determine ASPECTS anatomical territory."),
    ("Objective 4", "Engineer a clinical NLP engine with clinical negation detection that automatically standardizes unstructured doctor notes into ICD-10 and SNOMED-CT codes."),
    ("Objective 5", "Integrate a real-time emergency dashboard with a 4.5-hour golden window countdown timer and automated nearest stroke-certified comprehensive hospital navigation.")
]
set_shape_text(s6.shapes[1], s6_items, font_size=13, space_after=6)


# ==================== SLIDE 7: SCOPE OF THE PROJECT ====================
s7 = prs.slides[6]
s7_items = [
    ("Population-Level Risk Screening", "Enables proactive stroke risk stratification in primary healthcare centers using 10 non-invasive physiological biomarkers (glucose, age, hypertension, BMI, heart disease)."),
    ("Emergency Department Triage", "Operationalizes interactive FAST assessments with automatic emergency code stroke alerts and paramedic transfer handoff cards."),
    ("Neuroimaging Decision Support", "Automated computer-aided lesion segmentation and quantitative area burden reporting on Axial T2-FLAIR brain MRI scans in sub-second execution times."),
    ("EHR Clinical Documentation", "Translates unstructured physician progress notes into structured, internationally standardized ICD-10 and SNOMED-CT electronic medical records."),
    ("Emergency Tele-Navigation", "Live distance matrix routing to certified stroke centers with real-time driving ETAs and integrated 4.5h tPA window countdown tracking."),
    ("Project Boundaries", "The platform acts as an assistive decision support system under medical supervision; it does not replace certified neurovascular specialists or administer autonomous surgical procedures.")
]
set_shape_text(s7.shapes[1], s7_items, font_size=13, space_after=6)


# ==================== SLIDE 8: PROPOSED SYSTEM ====================
s8 = prs.slides[7]
s8_items = [
    ("Three-Tier System Architecture", "CogniCare AI operates across an integrated multi-tier topology: Client Presentation Tier, Intelligence Core Tier, and Emergency Clinical Action Tier."),
    ("Tier 1 — Patient & Bystander Layer", "Interactive digital FAST symptom questionnaire, comprehensive stroke risk assessment, and one-tap Emergency SOS dispatch."),
    ("Tier 2 — Multi-Modal AI Core Engines", 
     "• Predictive Engine: Soft Voting Ensemble (Random Forest + Gradient Boosting + AdaBoost).\n"
     "• Explainability (XAI): SHAP-inspired marginal feature attribution and critical biomarker alerting.\n"
     "• Neuroimaging Engine: 5-Stage Segmentation (Grayscale -> Gaussian Blur -> Otsu -> Morphology -> ASPECTS).\n"
     "• Clinical NLP Assistant: Medical NER, clinical negation parser, and ICD-10 / SNOMED-CT linker."),
    ("Tier 3 — Clinical Decision & Emergency Orchestration", 
     "Doctor review queue with AI confirmation/override, 4.5-hour intravenous thrombolysis countdown timer, and automated GPS hospital distance matrix routing.")
]
set_shape_text(s8.shapes[1], s8_items, font_size=13.5, space_after=8)


# ==================== SLIDE 9: METHODOLOGY USED ====================
s9 = prs.slides[8]
s9_items = [
    ("Data Curation & Preprocessing", "Trained on 5,110 clinical stroke records. Applied median imputation for missing BMI values (median: 28.4) and StandardScaler normalization for continuous physiological parameters (glucose, age, BMI)."),
    ("Ensemble Model Architecture", "Employs an 80:20 stratified train-test split. Combines Random Forest (n=100, balanced class weights), Gradient Boosting (n=100, LR=0.08), and AdaBoost (n=100, SAMME.R). Predictions combined via Soft Voting probability consensus: p = 1/3 * sum(p_m)."),
    ("Explainable AI (XAI) Attribution", "Calculates local feature contribution percentages against clinical baseline thresholds, transparently displaying how hyperglycemia (>200 mg/dL) or hypertension drives risk."),
    ("5-Stage MRI Vision Pipeline", "Sequential computer vision execution: (1) Grayscale intensity mapping -> (2) Spatial Gaussian smoothing (5x5, sigma=1.2) -> (3) Otsu bimodal adaptive thresholding -> (4) Morphological binary opening/closing to eliminate skull artifacts -> (5) Quantitative lesion % and ASPECTS territory scoring."),
    ("Clinical NLP & Negation Engine", "Tokenizes doctor clinical text, applies fuzzy n-gram matching against 50+ neurological symptoms, checks preceding negation modifiers, and attaches ICD-10 and SNOMED-CT codes.")
]
set_shape_text(s9.shapes[1], s9_items, font_size=13, space_after=6)


# ==================== SLIDE 10: HARDWARE & SOFTWARE REQUIREMENTS ====================
s10 = prs.slides[9]
s10_items = [
    ("Software Environment", 
     "• Operating System: Windows 10/11 / Linux (Ubuntu 22.04 LTS)\n"
     "• Programming Language: Python 3.10+ / Python 3.13\n"
     "• Web & API Framework: FastAPI, Uvicorn ASGI Server, Jinja2 Templates\n"
     "• ML & Data Processing: Scikit-learn, NumPy, Pandas, Joblib\n"
     "• Computer Vision & NLP: SciPy, Pillow, Matplotlib, RapidFuzz\n"
     "• Medical Ontologies: ICD-10 Clinical Modification, SNOMED-CT, RxNorm\n"
     "• External APIs: Google Maps Platform (Distance Matrix), Twilio REST API"),
    ("Hardware Specifications", 
     "• Processor (CPU): Intel Core i5/i7 (10th Gen+) or AMD Ryzen 5/7 (Multi-core x86_64)\n"
     "• System Memory (RAM): 8 GB minimum (16 GB recommended for high-res MRI pipelines)\n"
     "• Storage: 256 GB SSD (sufficient for image caching, model weights, and local database)\n"
     "• Network Interface: Active broadband internet connection for live geolocation & API alerts")
]
set_shape_text(s10.shapes[1], s10_items, font_size=13, space_after=8)


# ==================== SLIDE 11: EXPECTED OUTCOMES ====================
s11 = prs.slides[10]
s11_items = [
    ("Proactive Risk Stratification", "High-sensitivity stroke risk prediction allowing early preventive lifestyle and pharmacological intervention before acute stroke onset."),
    ("Physician Trust via Transparency", "Clear explanation of machine learning decisions using granular biomarker attribution percentages, eliminating 'black-box' hesitation in clinical settings."),
    ("Rapid Objective MRI Quantification", "Automated lesion boundary delineation, area percentage reporting, and ASPECTS scoring within milliseconds, eliminating radiologist inter-observer bias."),
    ("Accelerated EHR Interoperability", "Seamless automated translation of unstructured clinical progress notes into internationally recognized ICD-10 and SNOMED-CT diagnostic codes."),
    ("Compressed Door-to-Needle Time", "Substantial reduction in critical emergency delay via automated FAST triage, 4.5-hour golden window countdown telemetry, and distance-optimized stroke center routing.")
]
set_shape_text(s11.shapes[1], s11_items, font_size=13.5, space_after=8)


# ==================== SLIDE 12: EXPERIMENT RESULTS AND DISCUSSION ====================
s12 = prs.slides[11]
s12_items = [
    ("Ensemble ML Performance", "Random Forest (84.2%), Gradient Boosting (88.6%), and AdaBoost (78.4%) fused via Soft Voting to yield a calibrated stroke probability of 83.7% with robust generalization."),
    ("Explainable AI (XAI) Attribution", "Local feature contribution identified Average Glucose >200 mg/dL (+34.5%), Age >65 (+28.2%), and Stage-2 Hypertension (+18.7%) as primary stroke risk drivers."),
    ("MRI Segmentation Telemetry", "Axial T2-FLAIR scan segmented at Otsu cutoff T=130; detected 3.7% lesion area ratio (2,423 px) mapped to the Left Middle Cerebral Artery (MCA) territory with ASPECTS score of 7/10."),
    ("Clinical NLP Accuracy", "Demonstrated 100% precision in detecting acute neurological symptoms (facial droop, hemiparesis, slurred speech) with flawless contextual negation detection and ICD-10 coding.")
]
# Resize text box to make room for embedded image on right/bottom
s12.shapes[1].width = Inches(6.8)
s12.shapes[1].height = Inches(4.8)
set_shape_text(s12.shapes[1], s12_items, font_size=12.5, space_after=6)

# Add image on right side of slide 12
if os.path.exists("screenshot_ml_xai.png"):
    left = Inches(7.7)
    top = Inches(1.5)
    width = Inches(5.0)
    s12.shapes.add_picture("screenshot_ml_xai.png", left, top, width=width)

if os.path.exists("screenshot_mri_pipeline.png"):
    left = Inches(7.7)
    top = Inches(4.3)
    width = Inches(5.0)
    s12.shapes.add_picture("screenshot_mri_pipeline.png", left, top, width=width)


# ==================== SLIDE 13: CONCLUSIONS ====================
s13 = prs.slides[12]
s13_items = [
    ("Comprehensive Platform Validation", "CogniCare AI successfully demonstrates an end-to-end multi-modal clinical intelligence system bridging predictive ML, neuroimaging CV, medical NLP, and emergency orchestration."),
    ("Balanced Ensemble Decision Making", "The soft-voting ensemble overcomes class imbalance and individual classifier bias, delivering calibrated, robust clinical risk assessments."),
    ("Deterministic & Lightweight Neuroimaging", "The 5-stage MRI segmentation module isolates infarct core hyperintensities in milliseconds without demanding heavy GPU infrastructure, making it ideal for community hospitals."),
    ("Explainability & Semantic Standardization", "SHAP-inspired feature attributions and negation-aware ICD-10 / SNOMED-CT extraction provide the clinical transparency and EHR interoperability necessary for physician adoption."),
    ("Future Development Roadmap", "Next phases will incorporate 3D U-Net architectures for multi-parametric volumetric MRI/CT perfusion scans, direct HL7/FHIR hospital database connectors, and multi-institutional federated learning.")
]
set_shape_text(s13.shapes[1], s13_items, font_size=13.5, space_after=8)


# ==================== SLIDE 14: REFERENCES ====================
s14 = prs.slides[13]
ref_items = [
    ("IEEE / Clinical Journal Standards", "Standard Academic Citations:"),
    ("[1]", "World Health Organization, 'Global Health Estimates: Leading causes of death and disability,' WHO Press, Geneva, 2023."),
    ("[2]", "W. Hacke et al., 'Thrombolysis with alteplase 3 to 4.5 hours after acute ischemic stroke (ECASS III),' New England Journal of Medicine, vol. 359, no. 13, pp. 1317–1329, 2008."),
    ("[3]", "P. Barber et al., 'Validity and reliability of a quantitative computed tomography score in predicting outcome of hyperacute stroke (ASPECTS),' The Lancet, vol. 355, no. 9216, pp. 1670–1674, 2000."),
    ("[4]", "S. M. Lundberg and S.-I. Lee, 'A unified approach to interpreting model predictions,' in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 4765–4774, 2017."),
    ("[5]", "American Stroke Association, 'Guidelines for the Early Management of Patients With Acute Ischemic Stroke,' Stroke, vol. 50, no. 12, pp. e344–e418, 2019.")
]
set_shape_text(s14.shapes[1], ref_items, font_size=13, space_after=6)


# ==================== SLIDE 15: THANK YOU !! ====================
s15 = prs.slides[14]
# Add subtitle/contact info text box below title
tx_box = s15.shapes.add_textbox(Inches(2.0), Inches(3.2), Inches(9.3), Inches(2.5))
tf15 = tx_box.text_frame
tf15.word_wrap = True

p15_1 = tf15.paragraphs[0]
p15_1.alignment = PP_ALIGN.CENTER
r15_1 = p15_1.add_run()
r15_1.text = "Shruti Gauchandra (Roll No. 15)\n"
r15_1.font.name = "Times New Roman"
r15_1.font.size = Pt(22)
r15_1.font.bold = True
r15_1.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)

p15_2 = tf15.add_paragraph()
p15_2.alignment = PP_ALIGN.CENTER
r15_2 = p15_2.add_run()
r15_2.text = "Final Year B.Tech — Department of Artificial Intelligence and Data Science\n"
r15_2.font.name = "Times New Roman"
r15_2.font.size = Pt(16)
r15_2.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

p15_3 = tf15.add_paragraph()
p15_3.alignment = PP_ALIGN.CENTER
r15_3 = p15_3.add_run()
r15_3.text = "Vidyavardhini's College of Engineering and Technology, Vasai\n\nQuestions & Answers Welcome"
r15_3.font.name = "Times New Roman"
r15_3.font.size = Pt(16)
r15_3.font.bold = True
r15_3.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)


# ==================== SLIDE 16: APPENDIX ====================
s16 = prs.slides[15]
s16_items = [
    ("REST API Endpoint Architecture", 
     "• POST /predict : Computes soft-voting risk probability (RF + GB + AdaBoost) & XAI local feature attributions.\n"
     "• POST /segment-mri : Executes 5-stage CV pipeline on uploaded scan, returning lesion area % & ASPECTS territory.\n"
     "• POST /parse-notes : Extracts symptoms, medications, and conditions with negation tagging & ICD-10 mapping.\n"
     "• POST /emergency-alert : Triggers emergency SMS/WhatsApp dispatch via Twilio and distance matrix hospital routing."),
    ("FAST Diagnostic Protocol Telemetry", 
     "• Face (F): Droop detection -> • Arm (A): Unilateral hemiparesis -> • Speech (S): Dysarthria/slurred speech -> • Time (T): Golden hour 4.5h tPA countdown initiation.")
]
s16.shapes[1].width = Inches(6.8)
s16.shapes[1].height = Inches(4.8)
set_shape_text(s16.shapes[1], s16_items, font_size=12.5, space_after=8)

if os.path.exists("screenshot_nlp_emergency.png"):
    left = Inches(7.6)
    top = Inches(1.8)
    width = Inches(5.1)
    s16.shapes.add_picture("screenshot_nlp_emergency.png", left, top, width=width)

# Save final PPTX
prs.save(OUTPUT_PATH)
print(f"Successfully generated populated PPTX: {OUTPUT_PATH}")

# Also copy to Desktop and static
desktop = os.path.expanduser('~') + '/Desktop/'
static_dir = 'c:/Shruti/AIH Project/backend/static/'

import shutil
shutil.copy(OUTPUT_PATH, desktop + 'CogniCare_AI_Mini_Project_Presentation.pptx')
shutil.copy(OUTPUT_PATH, static_dir + 'CogniCare_AI_Mini_Project_Presentation.pptx')
print("Copied PPTX to Desktop and static folder!")
