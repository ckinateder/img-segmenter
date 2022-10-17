import cv2
import requests 
import numpy as np
from time import sleep
from typing import Union

def grab_image(url:str) -> np.ndarray:
    """
    Download am image to an opencv image
    """
    response = requests.get(url).content
    nparr = np.frombuffer(response, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    return img

def split_into_quarters(img: np.ndarray)->dict:
    """Divide an image into 4 quarters, and 4 more to ensure no overlap"""
    # constants
    h, w, channels = img.shape
    half_w = w//2
    half_h = h//2
    quarter_w = w//4
    quarter_h = h//4

    # split quarters (by quadrant)
    q1 = img[:half_h, :half_w] 
    q2 = img[:half_h, half_w:]
    q3 = img[half_h:, :half_w]
    q4 = img[half_h:, half_w:]

    # split middles
    top_middle = img[:half_h, quarter_w:(quarter_w*3)]
    bottom_middle = img[half_h:, quarter_w:(quarter_w*3)]
    center_left = img[quarter_h:(quarter_h*3), :half_w]
    center_right = img[quarter_h:(quarter_h*3), half_w:]

    imgs = {
        "top_left": {"img": q1, "x1": 0, "y1": 0, "x2": half_w, "y2": half_h},
        "top_middle": {"img": top_middle, "x1": quarter_w, "y1": 0, "x2": quarter_w*3, "y2": half_h},
        "top_right": {"img": q2, "x1": half_w, "y1": 0, "x2": w, "y2": half_h},
        "bottom_right": {"img": q4, "x1": half_w, "y1": half_h, "x2": w, "y2": h},
        "bottom_middle": {"img": bottom_middle, "x1": quarter_w, "y1": half_h, "x2": quarter_w*3, "y2": h},
        "bottom_left": {"img": q3, "x1": 0, "y1": half_h, "x2": half_w, "y2": h},
        "center_left": {"img": center_left, "x1": 0, "y1":  quarter_h, "x2": half_w, "y2": quarter_h*3},
        "center_right": {"img": center_right, "x1": half_w, "y1":  quarter_h, "x2": w, "y2": quarter_h*3},
    }
    return imgs

if __name__ == "__main__":
    img = grab_image("https://instrumentationtools.com/wp-content/uploads/2018/10/Circuit-Diagram-Schematic.png")
    cv2.imwrite("original.png", img)
    q = split_into_quarters(img)
    for i in q:
        cv2.imwrite(f"{i}.png",q[i]["img"])