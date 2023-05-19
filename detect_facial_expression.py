import cv2  # type: ignore[import]
from hsemotion.facial_emotions import HSEmotionRecognizer
from PIL import Image  # type: ignore[import]

EMOTION_NAMES = ("Anger", "Contempt", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise")  # fmt: ignore

NO_FEATURES_DETECTED = {emotion: 0.0 for emotion in EMOTION_NAMES}


class CameraNotAccessible(Exception):
    pass


def test_camera_accessible() -> bool:
    try:
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        _, image = camera.read()
        camera.release()
        if image is None:  # If it can't detect a camera, it will return None
            return False
        # print("All worked fine")
        return True
    except:
        return False


def take_picture() -> list[int]:
    # print("Taking picture!")
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # print("Camera made")
    _, frame = camera.read()
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
    scores: list[tuple[str, float]] = list(zip(EMOTION_NAMES, scores))
    sorted_scores = dict(sorted(scores, key=lambda x: x[1], reverse=True))
    return str(emotion), sorted_scores


if __name__ == "__main__":
    # take_picture()
    print(get_facial_emotion(testing_mode_image="smiling_man.png"))
