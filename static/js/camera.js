document.addEventListener("DOMContentLoaded", () => {
    const videoElement = document.getElementById('webcam');
    const canvasElement = document.getElementById('output_canvas');
    const canvasCtx = canvasElement ? canvasElement.getContext('2d') : null;
    const speakBtn = document.getElementById('speak-btn');
    const translatedText = document.getElementById('translated-text');
    const confidenceText = document.getElementById('confidence-text');

    let lastDetectedWord = "";
    let lastFetchTime = 0;

    if (videoElement && window.Hands) {
        const hands = new Hands({
            locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
        });

        hands.setOptions({
            maxNumHands: 2,
            modelComplexity: 1,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        hands.onResults(results => {
            if (!canvasCtx || !canvasElement) return;
            canvasCtx.save();
            canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
            canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

            if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
                let allLandmarks = [];
                for (const landmarks of results.multiHandLandmarks) {
                    drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 2});
                    drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 1});
                    
                    landmarks.forEach(lm => {
                        allLandmarks.push(lm.x, lm.y, lm.z);
                    });
                }

                const now = Date.now();
                if (now - lastFetchTime > 300) {
                    lastFetchTime = now;
                    fetch('/interpreter/predict_gesture', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ landmarks: allLandmarks })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (translatedText && data.prediction) {
                            translatedText.innerText = data.prediction;
                            if (confidenceText) {
                                confidenceText.innerText = data.confidence > 0 
                                    ? `Confidence: ${(data.confidence * 100).toFixed(1)}%` 
                                    : "";
                            }

                            if (data.prediction && data.prediction !== "No Hand Detected" && data.prediction !== "Unrecognized Gesture" && data.prediction !== lastDetectedWord) {
                                lastDetectedWord = data.prediction;
                                speakText(data.prediction);
                            }
                        }
                    })
                    .catch(err => console.error('Gesture prediction error:', err));
                }
            } else {
                if (translatedText) {
                    translatedText.innerText = "No hand detected";
                    if (confidenceText) confidenceText.innerText = "";
                }
            }
            canvasCtx.restore();
        });

        if (window.Camera) {
            const camera = new Camera(videoElement, {
                onFrame: async () => {
                    canvasElement.width = videoElement.videoWidth;
                    canvasElement.height = videoElement.videoHeight;
                    await hands.send({ image: videoElement });
                },
                width: 640,
                height: 480
            });
            camera.start();
        }
    }

    function speakText(text) {
        fetch('/interpreter/speak', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => console.log('Spoken:', data))
        .catch(err => console.error('Error:', err));
    }

    if (speakBtn) {
        speakBtn.addEventListener('click', () => {
            const textToSpeak = translatedText.innerText;
            speakText(textToSpeak);
        });
    }
});
