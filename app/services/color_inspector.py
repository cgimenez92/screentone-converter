import numpy as np
import webcolors


def build_color_name_map(image_np):
    """Build color name mapping for the image - moved from services"""
    height, width = image_np.shape[:2]
    color_name_map = np.empty((height, width), dtype=object)

    css3_names = list(webcolors._definitions._CSS3_NAMES_TO_HEX.keys())
    css3_rgb = np.array([webcolors.hex_to_rgb(webcolors._definitions._CSS3_NAMES_TO_HEX[name]) for name in css3_names])

    for y in range(height):
        for x in range(width):
            r1, g1, b1 = image_np[y, x]
            deltas = ((css3_rgb - [r1, g1, b1]) ** 2).sum(axis=1)
            closest_index = np.argmin(deltas)
            color_name_map[y, x] = css3_names[closest_index].capitalize()

    return color_name_map