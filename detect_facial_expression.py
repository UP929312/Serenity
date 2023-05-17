import cv2  # type: ignore[import]
from hsemotion.facial_emotions import HSEmotionRecognizer

EMOTION_NAMES = ("Anger", "Contempt", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise")  # fmt: ignore

NO_FEATURES_DETECTED = {emotion: 0.0 for emotion in EMOTION_NAMES}

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


def get_facial_emotion(testing_mode: bool = False) -> tuple[str, dict[str, float]]:
    """
    Takes a picture of the user and returns the emotion and the scores for each emotion.
    If the camera is not accessible, it returns 0.0 for each emotion.
    WARNING: Takes 0.7 seconds to run from start to finish.
    """
    try:
        # print("Taking picture!")
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # print("Camera made")
        _, frame = camera.read()
        # print("Camera taken")
        camera.release()
        # print("Release")
    except:
        return "camera_being_used_already", NO_FEATURES_DETECTED

    if frame is None:
        return "no_camera_detected", NO_FEATURES_DETECTED
    # print("Taken!")
    if testing_mode:
        # cv2.imshow("test", frame)
        # cv2.waitKey(0)
        return "testing_mode", NO_FEATURES_DETECTED

    model_name = "enet_b0_8_best_afew"
    fer = HSEmotionRecognizer(model_name=model_name, device="cpu")  # device is cpu or gpu
    emotion, scores = fer.predict_emotions(frame, logits=True)
    scores = list(zip(EMOTION_NAMES, scores))
    sorted_scores = dict(sorted(scores, key=lambda x: x[1], reverse=True))
    return str(emotion), sorted_scores


if __name__ == "__main__":
    print(get_facial_emotion(testing_mode=True))
    """
    import time
    start_time = time.time()
    for i in range(10):
        print(test_camera_accessible())
        print(time.time() - start_time)
    """
