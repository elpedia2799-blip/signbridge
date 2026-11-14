from recognition.hand_tracking import HandTracker
from models.recognition import ASLModel

class GestureRecognizer:
    def __init__(self):
        self.tracker = HandTracker()
        self.classifier = ASLModel()

    def process_frame(self, frame):
        annotated_frame = self.tracker.find_hands(frame)
        landmarks = self.tracker.get_landmark_list(frame)
        if not landmarks:
            return annotated_frame, None, 0.0
        label, confidence = self.classifier.predict(landmarks)
        return annotated_frame, label, confidence
