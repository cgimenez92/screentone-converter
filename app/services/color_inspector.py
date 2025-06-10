import numpy as np
import webcolors

""" def get_nearest_color_name(rgb_tuple):
    try:
        return webcolors.rgb_to_name(rgb_tuple)
    except ValueError:
        # Find the closest match manually
        min_colors = {}
        for key, name in webcolors.CSS3_NAMES_TO_HEX.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(name)
            rd = (r_c - rgb_tuple[0]) ** 2
            gd = (g_c - rgb_tuple[1]) ** 2
            bd = (b_c - rgb_tuple[2]) ** 2
            min_colors[(rd + gd + bd)] = key
        return min_colors[min(min_colors.keys())] """

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