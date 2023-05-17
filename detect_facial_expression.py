import cv2
from hsemotion.facial_emotions import HSEmotionRecognizer

EMOTION_NAMES = ("Anger", "Contempt", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise")

def test_camera_accessible() -> bool:
    try:
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        _, image = camera.read()
        camera.release()
        cv2.imshow("Camera accessible", image)
        #cv2.waitKey(0)
        cv2.destroyAllWindows()
        #print("All worked fine")
        return True
    except:
        return False

def get_facial_emotion() -> tuple[str, dict[str, float]]:
    try:
        #print("Taking picture!")
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        #print("Camera made")
        _, frame = camera.read()
        #print("Camera taken")
        camera.release()
        #print("Release")
    except:
        return "Unknown", {emotion: 0.0 for emotion in EMOTION_NAMES}
    #print("Taken!")

    #cv2.imshow("test", frame)
    #cv2.waitKey(0)

    model_name = 'enet_b0_8_best_afew'
    fer = HSEmotionRecognizer(model_name=model_name,device='cpu') # device is cpu or gpu
    emotion, scores = fer.predict_emotions(frame, logits=True)
    scores = dict(list(zip(EMOTION_NAMES, scores)))
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return emotion, sorted_scores

if __name__ == "__main__":
    print(get_facial_emotion())