from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from drowsiness_detection import DrowsinessDetector

app = Flask(__name__)
CORS(app)  # Allow React frontend requests

# Initialize the detector
detector = DrowsinessDetector()

@app.route('/video_feed')
def video_feed():
    """Video stream endpoint for React frontend."""
    return Response(detector.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['POST'])
def control():
    """Handle control actions from React (pause, resume, stop)."""
    data = request.get_json()
    action = data.get("action", "")

    if action == "pause":
        detector.pause()
    elif action == "resume":
        detector.resume()
    elif action == "stop":
        detector.stop()
    else:
        return jsonify({"status": "error", "message": "Invalid action"}), 400

    return jsonify({"status": "ok", "action": action})

@app.route('/alert', methods=['GET'])
def alert_status():
    """
    Endpoint for React UI to check if the driver is drowsy.
    Returns a JSON with the current drowsiness state.
    """
    return jsonify({"alert": detector.is_drowsy})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
