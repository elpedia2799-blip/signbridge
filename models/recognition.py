import os
import json
import numpy as np
from models.sign import Sign
from recognition.preprocessing import normalize_landmarks

class ASLModel:
    def __init__(self, model_path='trained_models/asl_model.keras', labels_path='trained_models/labels.json'):
        self.model = None
        self.labels = {}
        if os.path.exists(labels_path):
            with open(labels_path, 'r') as f:
                self.labels = json.load(f)
        if os.path.exists(model_path):
            try:
                import tensorflow as tf
                self.model = tf.keras.models.load_model(model_path)
            except ImportError:
                self.model = None

    def match_uploaded_signs(self, landmarks):
        if not landmarks:
            return None, 0.0
        
        input_norm = np.array(normalize_landmarks(landmarks), dtype=np.float32)
        if input_norm.size == 0:
            return None, 0.0

        best_word = None
        best_score = 0.0

        all_signs = Sign.query.filter(Sign.landmarks_json.isnot(None)).all()
        for sign in all_signs:
            try:
                saved_lms = json.loads(sign.landmarks_json)
                saved_norm = np.array(normalize_landmarks(saved_lms), dtype=np.float32)
                if saved_norm.shape == input_norm.shape:
                    dist = np.linalg.norm(input_norm - saved_norm)
                    similarity = max(0.0, 1.0 - (dist / 5.0))
                    if similarity > best_score:
                        best_score = similarity
                        best_word = sign.word
            except Exception:
                continue

        if best_score >= 0.70:
            return best_word, float(best_score)
        return None, 0.0

    def predict(self, landmarks):
        matched_word, matched_conf = self.match_uploaded_signs(landmarks)
        if matched_word:
            return matched_word, matched_conf

        if not self.model or not landmarks:
            return None, 0.0
        features = normalize_landmarks(landmarks)
        input_data = np.array([features], dtype=np.float32)
        predictions = self.model.predict(input_data, verbose=0)
        class_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][class_idx])
        label = self.labels.get(str(class_idx), "Unknown")
        return label, confidence
