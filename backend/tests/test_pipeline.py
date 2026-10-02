"""
CogniCare AI - Automated Test Suite
Verifies data preprocessing shapes, ensemble training/inference, segmentation outputs, and NLP extraction.
"""

import unittest
import numpy as np
import pandas as pd

from backend.src.preprocessing import preprocess_stroke_data
from backend.src.model_ensemble import CogniCareEnsemble
from backend.src.image_segmentation import process_mri_scan, create_synthetic_mri_scan
from backend.src.nlp_extractor import CogniCareNLP
from backend.src.xai_explainer import compute_xai_explanations

class TestCogniCarePipeline(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.raw_df, cls.cleaned_df, _ = preprocess_stroke_data()
        cls.ensemble = CogniCareEnsemble()
        cls.ensemble.load()
        cls.nlp = CogniCareNLP()

    def test_01_preprocessing(self):
        """Verifies missing BMI imputation and dataset integrity."""
        self.assertFalse(self.cleaned_df["bmi"].isnull().any(), "No nulls allowed in BMI")
        self.assertIn("stroke", self.cleaned_df.columns)
        self.assertEqual(len(self.cleaned_df), 2500)

    def test_02_ensemble_inference(self):
        """Verifies RF + GB + AdaBoost soft voting prediction."""
        patient = {
            "gender": 1, "age": 67, "hypertension": 1, "heart_disease": 1,
            "ever_married": 1, "work_type": 2, "Residence_type": 1,
            "avg_glucose_level": 218.4, "bmi": 32.2, "smoking_status": 1
        }
        res = self.ensemble.predict_risk(patient)
        self.assertIn("risk_score_percent", res)
        self.assertIn("model_breakdown", res)
        self.assertIn("random_forest", res["model_breakdown"])
        self.assertIn("gradient_boosting", res["model_breakdown"])
        self.assertIn("adaboost", res["model_breakdown"])
        self.assertGreater(res["risk_score_percent"], 50.0)

    def test_03_mri_segmentation(self):
        """Verifies 5-stage OpenCV/SciPy segmentation pipeline."""
        mri_arr = create_synthetic_mri_scan(has_lesion=True, lesion_side="left")
        res = process_mri_scan(mri_arr)
        self.assertIn("metrics", res)
        self.assertIn("stages", res)
        self.assertIn("overlay", res["stages"])
        self.assertGreater(res["metrics"]["segmented_area_px"], 0)
        self.assertGreater(res["metrics"]["threshold_cutoff"], 0)

    def test_04_nlp_extraction(self):
        """Verifies medical NER and SNOMED-CT / ICD-10 linking."""
        note = "67yo male with acute facial drooping, slurred speech, and arm weakness. Prescribed Aspirin and Amlodipine."
        res = self.nlp.parse_clinical_text(note)
        self.assertGreaterEqual(res["entity_count"], 4)
        self.assertTrue(any(e["category"] == "symptom" for e in res["entities"]))
        self.assertTrue(any(e["category"] == "medication" for e in res["entities"]))

    def test_05_xai_explanations(self):
        """Verifies local feature impact and critical threshold flags."""
        patient = {"age": 67, "avg_glucose_level": 218.4, "bmi": 32.2, "hypertension": 1, "heart_disease": 1, "smoking_status": 1}
        xai = compute_xai_explanations(patient)
        self.assertGreaterEqual(len(xai["attributions"]), 5)
        self.assertTrue(any("Glucose" in f for f in xai["critical_flags"]))

if __name__ == "__main__":
    unittest.main()
