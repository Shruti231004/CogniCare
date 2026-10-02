"""
CogniCare AI - Clinical NLP Extraction Engine
Robust medical entity recognition, synonym resolution, negation detection,
and ontology linking (SNOMED-CT / ICD-10 / RxNorm).
"""

import re
import string

# Canonical medical ontology database
ONTOLOGY_CONCEPTS = {
    # Symptoms
    "facial drooping": {
        "concept": "Facial Palsy / Drooping",
        "category": "symptom",
        "icd10": "R29.810",
        "snomed": "281555004",
        "synonyms": [
            "facial drooping", "facial droop", "face drooping", "face droop", "drooping face",
            "facial palsy", "face is drooping", "drooping on one side", "face sag", "sagging face",
            "droopy face", "crooked smile", "one sided facial droop"
        ]
    },
    "slurred speech": {
        "concept": "Dysarthria / Speech Difficulty",
        "category": "symptom",
        "icd10": "R47.81",
        "snomed": "289190003",
        "synonyms": [
            "slurred speech", "speech slurred", "slurring words", "slurring speech", "slurring",
            "dysarthria", "speech difficulty", "difficulty speaking", "trouble speaking",
            "can't speak properly", "cant speak properly", "unable to speak", "cannot speak",
            "trouble talking", "difficulty talking", "speech problems", "speech impairment",
            "incoherent speech", "garbled speech", "mumbled speech"
        ]
    },
    "arm weakness": {
        "concept": "Arm Weakness / Hemiparesis",
        "category": "symptom",
        "icd10": "G81.9",
        "snomed": "26544005",
        "synonyms": [
            "sudden right arm weakness", "sudden left arm weakness",
            "right arm weakness", "left arm weakness", "arm weakness", "weakness in arm",
            "weakness in right arm", "weakness in left arm", "right arm feels weak",
            "left arm feels weak", "arm feels weak", "weak arm", "arm drift", "loss of arm strength",
            "cannot lift arm", "can't lift arm", "trouble moving arm", "limb weakness",
            "hemiparesis", "unilateral weakness", "one sided weakness"
        ]
    },
    "leg weakness": {
        "concept": "Leg Weakness / Hemiparesis",
        "category": "symptom",
        "icd10": "G81.9",
        "snomed": "26544005",
        "synonyms": [
            "right leg weakness", "left leg weakness", "leg weakness", "weakness in leg",
            "weakness in right leg", "weakness in left leg", "weak leg", "trouble walking",
            "cannot walk", "can't walk", "unable to walk", "difficulty walking", "dragging leg",
            "foot drop", "limping", "stumbling"
        ]
    },
    "muscle weakness": {
        "concept": "Generalized Muscle Weakness",
        "category": "symptom",
        "icd10": "M62.81",
        "snomed": "13791008",
        "synonyms": [
            "muscle weakness", "feeling weak", "body weakness", "loss of strength",
            "profound weakness", "sudden weakness", "weakness"
        ]
    },
    "headache": {
        "concept": "Acute Cephalea / Severe Headache",
        "category": "symptom",
        "icd10": "R51",
        "snomed": "25064002",
        "synonyms": [
            "severe headache", "bad headache", "thunderclap headache", "sudden headache",
            "intense headache", "worst headache of my life", "headache", "head pain", "migraine",
            "throbbing headache", "splitting headache"
        ]
    },
    "dizziness": {
        "concept": "Dizziness / Vertigo",
        "category": "symptom",
        "icd10": "R42",
        "snomed": "404640003",
        "synonyms": [
            "dizziness", "dizzy", "lightheadedness", "lightheaded", "light-headed", "vertigo",
            "room spinning", "spinning sensation", "feeling faint", "loss of balance",
            "unsteadiness", "unsteady on feet", "off balance"
        ]
    },
    "numbness": {
        "concept": "Hypesthesia / Sensory Numbness",
        "category": "symptom",
        "icd10": "R20.0",
        "snomed": "44077006",
        "synonyms": [
            "numbness in arm", "numbness in face", "numbness in leg", "facial numbness",
            "numbness", "numb", "numbing sensation", "tingling", "pins and needles",
            "paresthesia", "loss of sensation", "loss of feeling", "can't feel my arm",
            "can't feel my face"
        ]
    },
    "vision loss": {
        "concept": "Visual Deficit / Amaurosis",
        "category": "symptom",
        "icd10": "H53.8",
        "snomed": "7973008",
        "synonyms": [
            "blurred vision", "double vision", "diplopia", "vision loss", "loss of vision",
            "sudden vision loss", "blind spot", "darkness in one eye", "partial blindness",
            "can't see clearly", "fuzzy vision", "blurry vision"
        ]
    },
    "confusion": {
        "concept": "Acute Cognitive Confusion / Alteration",
        "category": "symptom",
        "icd10": "R41.0",
        "snomed": "40917007",
        "synonyms": [
            "confusion", "confused", "disoriented", "memory loss", "cannot remember",
            "trouble understanding", "difficulty comprehending", "altered mental status"
        ]
    },
    "chest pain": {
        "concept": "Angina / Acute Chest Pain",
        "category": "symptom",
        "icd10": "R07.9",
        "snomed": "29857009",
        "synonyms": [
            "chest pain", "chest pressure", "chest tightness", "heart pain", "crushing chest pain",
            "substernal chest pain", "pain in chest"
        ]
    },
    "shortness of breath": {
        "concept": "Dyspnea / Shortness of Breath",
        "category": "symptom",
        "icd10": "R06.02",
        "snomed": "267036007",
        "synonyms": [
            "shortness of breath", "difficulty breathing", "trouble breathing", "can't breathe",
            "breathlessness", "dyspnea", "gasping for air"
        ]
    },
    "nausea": {
        "concept": "Nausea",
        "category": "symptom",
        "icd10": "R11.0",
        "snomed": "422587007",
        "synonyms": ["nausea", "feeling nauseous", "queasy", "sick to stomach"]
    },
    "vomiting": {
        "concept": "Emesis / Vomiting",
        "category": "symptom",
        "icd10": "R11.1",
        "snomed": "422400008",
        "synonyms": ["vomiting", "threw up", "throwing up", "puking", "emesis"]
    },
    "fever": {
        "concept": "Pyrexia / Fever",
        "category": "symptom",
        "icd10": "R50.9",
        "snomed": "386661006",
        "synonyms": ["fever", "high temperature", "feverish", "chills"]
    },
    "fatigue": {
        "concept": "Fatigue / Malaise",
        "category": "symptom",
        "icd10": "R53.83",
        "snomed": "84229001",
        "synonyms": ["fatigue", "exhaustion", "extremely tired", "lethargy"]
    },
    "palpitations": {
        "concept": "Tachycardia / Palpitations",
        "category": "symptom",
        "icd10": "R00.2",
        "snomed": "80313002",
        "synonyms": ["palpitations", "racing heart", "rapid heartbeat", "heart fluttering"]
    },
    "seizure": {
        "concept": "Convulsion / Seizure Event",
        "category": "symptom",
        "icd10": "R56.9",
        "snomed": "91175000",
        "synonyms": ["seizure", "convulsions", "epileptic fit", "shaking uncontrollably"]
    },
    "fainting": {
        "concept": "Syncope / Fainting",
        "category": "symptom",
        "icd10": "R55",
        "snomed": "271594007",
        "synonyms": ["fainting", "fainted", "syncope", "passed out", "blacked out", "loss of consciousness"]
    },

    # Diagnoses & Conditions
    "stroke": {
        "concept": "Cerebrovascular Accident (CVA)",
        "category": "diagnosis",
        "icd10": "I64",
        "snomed": "230690007",
        "synonyms": ["stroke", "brain stroke", "cva", "cerebrovascular accident"]
    },
    "ischemic stroke": {
        "concept": "Cerebral Ischemic Infarction",
        "category": "diagnosis",
        "icd10": "I63.9",
        "snomed": "422504002",
        "synonyms": ["ischemic stroke", "cerebral infarction", "brain infarct", "ischemic cva"]
    },
    "transient ischemic attack": {
        "concept": "Transient Ischemic Attack (TIA)",
        "category": "diagnosis",
        "icd10": "G45.9",
        "snomed": "266257000",
        "synonyms": ["tia", "transient ischemic attack", "mini stroke", "mini-stroke"]
    },
    "hypertension": {
        "concept": "Essential Hypertension",
        "category": "diagnosis",
        "icd10": "I10",
        "snomed": "38341003",
        "synonyms": ["hypertension", "high blood pressure", "elevated blood pressure", "bp high", "high bp"]
    },
    "heart disease": {
        "concept": "Coronary Artery Disease (CAD)",
        "category": "diagnosis",
        "icd10": "I25.1",
        "snomed": "53741008",
        "synonyms": ["heart disease", "coronary artery disease", "cad", "coronary heart disease"]
    },
    "atrial fibrillation": {
        "concept": "Atrial Fibrillation (AFib)",
        "category": "diagnosis",
        "icd10": "I48.91",
        "snomed": "49436004",
        "synonyms": ["atrial fibrillation", "afib", "a-fib", "irregular heartbeat"]
    },
    "diabetes": {
        "concept": "Diabetes Mellitus",
        "category": "diagnosis",
        "icd10": "E11",
        "snomed": "73211009",
        "synonyms": ["diabetes", "type 2 diabetes", "t2d", "high blood sugar", "diabetic"]
    },
    "high cholesterol": {
        "concept": "Hyperlipidemia / Dyslipidemia",
        "category": "diagnosis",
        "icd10": "E78.5",
        "snomed": "55822004",
        "synonyms": ["high cholesterol", "hyperlipidemia", "dyslipidemia", "elevated cholesterol"]
    },

    # Medications
    "aspirin": {
        "concept": "Aspirin (Antiplatelet)",
        "category": "medication",
        "icd10": "RxNorm:1191",
        "snomed": "387458008",
        "synonyms": ["aspirin", "acetylsalicylic acid", "ecosprin", "bayer aspirin"]
    },
    "clopidogrel": {
        "concept": "Clopidogrel (Plavix)",
        "category": "medication",
        "icd10": "RxNorm:73032",
        "snomed": "386864001",
        "synonyms": ["clopidogrel", "plavix"]
    },
    "atorvastatin": {
        "concept": "Atorvastatin (Lipitor)",
        "category": "medication",
        "icd10": "RxNorm:83367",
        "snomed": "386877005",
        "synonyms": ["atorvastatin", "lipitor", "statin"]
    },
    "amlodipine": {
        "concept": "Amlodipine (Norvasc)",
        "category": "medication",
        "icd10": "RxNorm:17767",
        "snomed": "386864001",
        "synonyms": ["amlodipine", "norvasc"]
    },
    "metformin": {
        "concept": "Metformin",
        "category": "medication",
        "icd10": "RxNorm:6809",
        "snomed": "372567009",
        "synonyms": ["metformin", "glucophage"]
    },
    "iv r-tpa": {
        "concept": "Intravenous Alteplase (r-tPA Thrombolytic)",
        "category": "medication",
        "icd10": "RxNorm:8410",
        "snomed": "387229007",
        "synonyms": ["iv r-tpa", "iv-tpa", "rtpa", "tpa", "alteplase", "thrombolytic", "thrombolysis"]
    },

    # Procedures
    "brain mri": {
        "concept": "Brain Magnetic Resonance Imaging",
        "category": "procedure",
        "icd10": "B030ZZZ",
        "snomed": "241601008",
        "synonyms": ["brain mri", "mri scan", "mri brain", "mri of brain", "mri examination", "diffusion mri"]
    },
    "head ct": {
        "concept": "Computed Tomography of Head",
        "category": "procedure",
        "icd10": "BW20ZZZ",
        "snomed": "303975005",
        "synonyms": ["head ct", "ct scan", "ct head", "stat head ct", "brain ct"]
    },
    "neurological exam": {
        "concept": "Neurological Physical Examination",
        "category": "procedure",
        "icd10": "Z01.89",
        "snomed": "89202008",
        "synonyms": ["neurological examination", "neuro exam", "neurological exam", "fast test"]
    }
}

# Negation trigger keywords
NEGATION_PRE = [
    r"\bno\b", r"\bnot\b", r"\bwithout\b", r"\bdenies\b", r"\bdenied\b",
    r"\bnegative for\b", r"\bno signs of\b", r"\bno evidence of\b",
    r"\bnever had\b", r"\bdoes not have\b", r"\bdoesn't have\b",
    r"\bfree of\b", r"\brules out\b", r"\bruled out\b"
]
NEGATION_POST = [
    r"\bresolved\b", r"\bhas resolved\b", r"\bwas ruled out\b",
    r"\bnot present\b", r"\bwas negative\b", r"\babsent\b"
]


class CogniCareNLP:
    """
    Precision Clinical NLP engine.
    Extracts high-confidence medical terms, maps to canonical ontology concepts,
    detects negation, and prevents spurious overlapping fragments.
    """

    def __init__(self):
        # Build flattened dictionary of (synonym_phrase, concept_key, concept_dict)
        self.phrase_registry = []
        for key, data in ONTOLOGY_CONCEPTS.items():
            for syn in data["synonyms"]:
                self.phrase_registry.append({
                    "phrase": syn.lower().strip(),
                    "key": key,
                    "concept": data["concept"],
                    "category": data["category"],
                    "icd10": data.get("icd10", ""),
                    "snomed": data.get("snomed", "")
                })

        # Sort by phrase length descending (longest phrase match takes precedence)
        self.phrase_registry.sort(key=lambda x: len(x["phrase"]), reverse=True)

        self.neg_pre_patterns = [re.compile(p, re.IGNORECASE) for p in NEGATION_PRE]
        self.neg_post_patterns = [re.compile(p, re.IGNORECASE) for p in NEGATION_POST]

    def is_negated(self, text: str, start: int, end: int) -> bool:
        """Checks if a matched entity is negated within a narrow surrounding window."""
        # 35 characters preceding
        pre_window = text[max(0, start - 35):start]
        for pat in self.neg_pre_patterns:
            if pat.search(pre_window):
                return True

        # 25 characters succeeding
        post_window = text[end:min(len(text), end + 25)]
        for pat in self.neg_post_patterns:
            if pat.search(post_window):
                return True

        return False

    def tokenize_and_tag(self, text: str):
        """POS tagger fallback for backward compatibility."""
        clean = text.replace("-", " - ")
        tokens = re.findall(r"\w+|[^\w\s]", clean)
        tags = []
        verbs = {"was", "is", "diagnosed", "reported", "confirmed", "prescribed", "advised", "has", "underwent", "arrived", "ordered", "experiencing"}
        nouns = {"patient", "stroke", "weakness", "side", "body", "drooping", "difficulty", "dizziness", "arm", "mri", "aspirin", "hypertension", "disease", "diabetes", "head", "ct"}
        adjectives = {"ischemic", "sudden", "right", "facial", "severe", "left", "cerebral", "regular", "important", "coronary", "acute", "slurred"}
        
        for tok in tokens:
            low = tok.lower()
            if tok in string.punctuation:
                t, d = "PUNCT", "Punctuation"
            elif re.match(r"^\d+", tok):
                t, d = "NUM", "Number"
            elif low in verbs:
                t, d = "VERB", "Verb"
            elif low in adjectives:
                t, d = "ADJ", "Adjective"
            elif low in nouns:
                t, d = "NOUN", "Noun"
            else:
                t, d = "NOUN", "Noun / Term"
            tags.append({"token": tok, "pos": t, "description": d})
        return tags

    def parse_clinical_text(self, text: str) -> dict:
        """
        Parses clinical free text to identify medical entities.
        Prevents overlapping duplicate fragments and detects negation.
        """
        if not text or not text.strip():
            return {
                "entity_count": 0,
                "token_count": 0,
                "entities": [],
                "ontology_links": [],
                "highlighted_html": ""
            }

        text_lower = text.lower()
        extracted = []
        ontology_links = []
        occupied_spans = []  # List of (start, end) tuples

        def spans_overlap(s1, e1, s2, e2):
            return not (e1 <= s2 or s1 >= e2)

        # 1. Match canonical concepts & synonyms (longest match first)
        for item in self.phrase_registry:
            phrase = item["phrase"]
            # Enforce whole word boundaries
            pattern = r"\b" + re.escape(phrase) + r"\b"
            for m in re.finditer(pattern, text_lower):
                s, e = m.span()
                # If this span overlaps with any already accepted span, discard it
                if any(spans_overlap(s, e, os, oe) for os, oe in occupied_spans):
                    continue

                occupied_spans.append((s, e))
                matched_text = text[s:e]
                negated = self.is_negated(text, s, e)

                extracted.append({
                    "entity": matched_text,
                    "concept": item["concept"],
                    "category": item["category"],
                    "confidence": 98 if not negated else 85,
                    "negated": negated,
                    "icd10": item["icd10"],
                    "snomed": item["snomed"],
                    "start": s,
                    "end": e
                })

                ontology_links.append({
                    "extracted_entity": matched_text,
                    "concept": item["concept"],
                    "category": item["category"],
                    "snomed": item["snomed"],
                    "icd10": item["icd10"],
                    "negated": negated,
                    "confidence": 98
                })

        # 2. Extract Patient Demographics (e.g., "67yo male", "54-year-old female")
        demo_match = re.search(r"\b(\d{1,2}(?:yo|-year-old))\s+(male|female|man|woman)?\b", text, re.IGNORECASE)
        if demo_match:
            s, e = demo_match.span()
            if not any(spans_overlap(s, e, os, oe) for os, oe in occupied_spans):
                occupied_spans.append((s, e))
                demo_text = text[s:e]
                extracted.append({
                    "entity": demo_text,
                    "concept": f"Patient Age/Sex ({demo_text})",
                    "category": "demographics",
                    "confidence": 99,
                    "negated": False,
                    "icd10": "Z00.00",
                    "snomed": "424144002",
                    "start": s,
                    "end": e
                })
                ontology_links.append({
                    "extracted_entity": demo_text,
                    "concept": f"Patient Age/Sex ({demo_text})",
                    "category": "demographics",
                    "snomed": "424144002",
                    "icd10": "Z00.00",
                    "negated": False,
                    "confidence": 99
                })

        # Sort all extractions in chronological order of appearance
        extracted.sort(key=lambda x: x["start"])

        # 3. Generate Clean HTML Highlight
        color_map = {
            "symptom": ("#ef4444", "rgba(239, 68, 68, 0.12)"),
            "diagnosis": ("#3b82f6", "rgba(59, 130, 246, 0.12)"),
            "medication": ("#10b981", "rgba(16, 185, 129, 0.12)"),
            "procedure": ("#06b6d4", "rgba(6, 182, 212, 0.12)"),
            "demographics": ("#8b5cf6", "rgba(139, 92, 246, 0.12)")
        }

        html_out = ""
        last_idx = 0
        for ent in extracted:
            s, e = ent["start"], ent["end"]
            cat = ent["category"]
            neg = ent["negated"]
            bc, bg = color_map.get(cat, ("#94a3b8", "rgba(148, 163, 184, 0.12)"))

            html_out += text[last_idx:s]
            strike = "text-decoration: line-through; opacity: 0.6;" if neg else ""
            status_text = " (Ruled Out)" if neg else ""

            html_out += (
                f'<span style="background:{bg}; border-bottom:2px solid {bc}; padding:2px 6px; '
                f'border-radius:4px; font-weight:600; {strike}" title="{ent["concept"]}{status_text}">'
                f'{text[s:e]}'
                f'<sup style="font-size:0.65rem; color:{bc}; margin-left:3px; font-weight:700;">'
                f'{"NOT-" if neg else ""}{cat[:3].upper()}</sup></span>'
            )
            last_idx = e

        html_out += text[last_idx:]

        return {
            "entity_count": len(extracted),
            "token_count": len(text.split()),
            "entities": extracted,
            "ontology_links": ontology_links,
            "highlighted_html": html_out,
            "pos_preview": self.tokenize_and_tag(text)[:15]
        }


# Backwards compatibility alias
NLPExtractor = CogniCareNLP


if __name__ == "__main__":
    nlp = CogniCareNLP()
    sample = "I have sudden right arm weakness, my face is drooping on one side, and I can't speak properly. It started about 2 hours ago. I also have a bad headache. No chest pain."
    res = nlp.parse_clinical_text(sample)
    print(f"Extracted {res['entity_count']} entities:")
    for ent in res["entities"]:
        print(f" - {ent['entity']} -> {ent['concept']} [{ent['category'].upper()}], negated={ent['negated']}")
