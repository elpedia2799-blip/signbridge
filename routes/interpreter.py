from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from recognition.speech import SpeechEngine
from models.recognition import ASLModel
from models.settings import SiteSettings

interpreter = Blueprint('interpreter', __name__)
speech_engine = SpeechEngine()
asl_model = ASLModel()

@interpreter.route('/live')
@login_required
def live():
    settings = SiteSettings.get_settings()
    return render_template('interpreter/live_interpreter.html', settings=settings)

@interpreter.route('/predict_gesture', methods=['POST'])
@login_required
def predict_gesture():
    data = request.get_json()
    landmarks = data.get('landmarks', [])
    
    if not landmarks:
        return jsonify({'status': 'success', 'prediction': 'No Hand Detected', 'confidence': 0.0})

    label, confidence = asl_model.predict(landmarks)
    if not label:
        label = "Unrecognized Gesture"
        confidence = 0.0

    return jsonify({
        'status': 'success',
        'prediction': label,
        'confidence': confidence
    })

@interpreter.route('/speak', methods=['POST'])
@login_required
def speak_text():
    data = request.get_json()
    text = data.get('text', '')
    speech_engine.speak(text)
    return jsonify({'status': 'success', 'spoken': text})
