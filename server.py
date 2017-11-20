import json

from flask import Flask, request
import emotion_api

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/recognize', methods=['POST'])
def recognize():
    image_data = request.get_data()
    try:
        return json.dumps(emotion_api.recognize(image_data))
    except emotion_api.ApiError as err:
        return json.dumps({'error': 'The emotion api call failed',
                           'emotionApiResponse': {'status_code': err.response.status_code,
                                                  'data': err.response.json()}}), 400
    except emotion_api.NoFaceRecognizedError:
        return json.dumps({'error': 'No face recognized'}), 400
    except emotion_api.MultipleFacesRecognizedError:
        return json.dumps({'error': 'Multiple faces recognized (only one is supported)'}), 400


if __name__ == '__main__':
    app.run()
