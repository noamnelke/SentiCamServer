import base64

import requests
import settings


class ApiError(Exception):
    def __init__(self, response):
        self.response = response


class NoFaceRecognizedError(Exception):
    pass


class MultipleFacesRecognizedError(Exception):
    pass


def recognize(image_data):
    response = requests.post(url=settings.API_HOST + '/recognize',
                             data=image_data,
                             headers=_get_headers())
    if not response.ok:
        raise ApiError(response)

    face_data = _extract_face_data(response)
    top_emotion = _get_top_emotion(face_data['scores'])

    return {"feeling": top_emotion,
            "faceRectangle": face_data['faceRectangle'],
            "imageData": base64.encodebytes(image_data).decode('ascii')}
    # I base64-encoded the binary image data so that it can be serialized as part of the JSON response,
    # this can be decoded on the client if needed


def _get_headers():
    return {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': settings.API_KEY,
    }


def _get_top_emotion(scores):
    return max(scores.items(), key=lambda emotion: emotion[1])[0]


def _extract_face_data(response):
    faces = response.json()
    if len(faces) == 0:
        raise NoFaceRecognizedError()
    if len(faces) > 1:
        raise MultipleFacesRecognizedError()
    return faces[0]
