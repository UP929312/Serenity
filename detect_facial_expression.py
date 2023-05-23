import cv2  # type: ignore[import]
from hsemotion.facial_emotions import HSEmotionRecognizer  # type: ignore[import]

# https://github.com/HSE-asavchenko/hsemotion

import numpy as np
from typing import TypedDict

EMOTION_NAMES = ("Anger", "Contempt", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise")  # fmt: ignore

NO_FEATURES_DETECTED = {emotion: 0.0 for emotion in EMOTION_NAMES}


class CameraNotAccessible(Exception):
    pass


class ImageData(TypedDict):
    data: np.ndarray[int, np.dtype[np.int32]]


def test_camera_accessible() -> bool:
    """Returns True if the camera is accessible, False otherwise."""
    try:
        return bool(take_picture())
    except CameraNotAccessible:
        return False


def take_picture() -> ImageData:
    """
    Takes a single frame picture of the user, or raises a CameraNotAccessible exception.\n
    `WARNING:` Takes 0.7 seconds to run from start to finish.\n
    Returns a 2d array of integers representing the image's data (each colour value as decimal).
    """
    # print("Taking picture!")
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # print("Camera made")
    frame: ImageData
    _, frame = camera.read()
    print(type(frame))
    # print("Picture taken")
    camera.release()
    if frame is None:
        raise CameraNotAccessible("The camera is not accessible")
    # print("Camera Released")
    return frame


def get_facial_emotion(testing_mode_image: str | None = None) -> tuple[str, dict[str, float]]:
    """
    Takes a picture of the user and returns the emotion and the scores for each emotion.
    If the camera is not accessible, it returns 0.0 for each emotion.
    WARNING: Takes 0.7 seconds to run from start to finish.
    """
    if testing_mode_image:
        frame = cv2.imread(f"assets/images/{testing_mode_image}.png", cv2.IMREAD_COLOR)
    else:
        try:
            frame = take_picture()
        except CameraNotAccessible:
            return "camera_not_accessible", NO_FEATURES_DETECTED  # Either it's being used by something else, or no camera is connected

    fer = HSEmotionRecognizer(model_name="enet_b2_8", device="cpu")  # device is cpu | gpu
    emotion, scores = fer.predict_emotions(frame, logits=True)
    scores_and_names: list[tuple[str, float]] = list(zip(EMOTION_NAMES, scores))
    sorted_scores = dict(sorted(scores_and_names, key=lambda x: x[1], reverse=True))
    return str(emotion), sorted_scores


if __name__ == "__main__":
    # take_picture()
    print(get_facial_emotion(testing_mode_image="smiling_man.png"))
