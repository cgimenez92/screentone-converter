# color_inspector_cv.py
import cv2
import numpy as np
import webcolors
from image_loader import load_image

def get_closest_color_name(rgb):
    try:
        return webcolors.rgb_to_name(rgb).capitalize()
    except ValueError:
        css3_rgb = {
            name: webcolors.name_to_rgb(name)
            for name in webcolors.names()
        }
        r1, g1, b1 = rgb
        closest_name = min(
            css3_rgb,
            key=lambda name: (
                (r1 - css3_rgb[name][0]) ** 2 +
                (g1 - css3_rgb[name][1]) ** 2 +
                (b1 - css3_rgb[name][2]) ** 2
            )
        )
        return f"Closest: {closest_name.capitalize()}"

def run_color_inspector():
    image_rgb, *_ = load_image()
    image_np = np.array(image_rgb)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    display_img = image_bgr.copy()

    def show_color_info(event, x, y, flags, param):
        nonlocal display_img
        if event == cv2.EVENT_MOUSEMOVE:
            if 0 <= x < image_np.shape[1] and 0 <= y < image_np.shape[0]:
                rgb = tuple(int(c) for c in image_np[y, x])
                name = get_closest_color_name(rgb)
                display_img = image_bgr.copy()
                cv2.circle(display_img, (x, y), 5, (0, 0, 0), 2)
                text = f"RGB({x}, {y}) = {rgb} → {name}"
                cv2.putText(display_img, text, (x + 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.namedWindow("Color Inspector")
    cv2.setMouseCallback("Color Inspector", show_color_info)

    while True:
        cv2.imshow("Color Inspector", display_img)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break
    cv2.destroyAllWindows()
