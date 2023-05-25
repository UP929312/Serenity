from typing import TypedDict

import cv2  # type: ignore[import]
import numpy as np

WINDOW_NAME = "Serenity"

presets = {
    "active": cv2.imread("assets/images/being_pressed.png"),
    "inactive": cv2.imread("assets/images/not_being_pressed.png"),
}

cv2.namedWindow(WINDOW_NAME)


def load_image_or_string(image: str | cv2.Mat) -> np.ndarray[int, np.dtype[np.generic]]:
    if isinstance(image, str):
        if image in presets:
            return presets[image]
        else:
            return cv2.imread(image)
    else:
        return image


def show_image(image: str | cv2.Mat, wait_for_key_press: bool = False) -> None:
    cv2.imshow(WINDOW_NAME, load_image_or_string(image))
    if wait_for_key_press:
        cv2.waitKey(0)


def show_text(
    img: str | cv2.Mat,
    text: str,
    position: tuple[int, int],
    font_size: float = 1,
    color: tuple[int, int, int] = (255, 255, 255),
    thickness: int = 2,
) -> None:
    cv2.putText(
        img=load_image_or_string(img),
        text=text,
        org=position,
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=font_size,
        color=color,
        thickness=thickness,
        lineType=cv2.LINE_AA,
        bottomLeftOrigin=True,
    )

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
    # print("Picture taken")
    camera.release()
    if frame is None:
        raise CameraNotAccessible("The camera is not accessible")
    # print("Camera Released")
    return frame