import os
import json

from colormath.color_objects import LabColor, BaseRGBColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import XYZColor, sRGBColor
from colormath.color_conversions import convert_color

dir_path = os.path.dirname(os.path.realpath(__file__))


def color_distance(rgb1, rgb2):

    rgb1 = sRGBColor(rgb1[0], rgb1[1], rgb1[2])
    rgb2 = sRGBColor(rgb2[0], rgb2[1], rgb2[2])

    color1 = convert_color(rgb1, LabColor, target_illuminant='d50')
    color2 = convert_color(rgb2, LabColor, target_illuminant='d50')

    delta_e = delta_e_cie2000(color1, color2)

    return delta_e



class FoundationMatch:
    foundation_data = {}

    def __init__(self):
        foundations_path = os.path.join(dir_path, 'foundations')
        for filename in os.listdir(foundations_path):
            the_path = os.path.join(foundations_path, filename)
            if os.path.isdir(the_path):
                data_path = os.path.join(the_path, "meta.json")
                with open(data_path, "r") as input:
                    data = json.load(input)
                    self.foundation_data[filename] = data

    def found_cat_of_color(self, color):

        distant = None
        result = None

        record = {}

        for key in self.foundation_data:
            data = self.foundation_data[key]
            data_color = data["colors"]
            d = color_distance(color, data_color)
            record[key] = d
            if distant is None:
                distant = d
                result = data
            elif distant > d:
                distant = d
                result = data
        print(record)
        return result

    def sorted_cat_of_color(self, color):
        result = []
        for key in self.foundation_data:
            data = self.foundation_data[key]
            data_color = data["colors"]
            d = color_distance(color, data_color)
            data["distance"] = d
            result.append(data)

        def _sort(elem):
            return elem["distance"]

        result.sort(key=_sort)

        return result


if __name__ == '__main__':

    from face_color import get_main_colors, rgb_to_hex

    foundations_path = os.path.join(dir_path, 'foundations')
    for filename in os.listdir(foundations_path):
        the_path = os.path.join(foundations_path, filename)
        if os.path.isdir(the_path):
            json_object = {}
            for image_file in os.listdir(the_path):
                if image_file.endswith("json"):
                    continue
                image_path = os.path.join(the_path, image_file)
                result = get_main_colors(image_path)
                largest = None
                largest_c = None
                for (percent, colors) in result:
                    if largest is None:
                        largest = percent
                        largest_c = colors
                    elif largest < percent:
                        largest = percent
                        largest_c = colors

                if largest_c is not None:
                    hex_color = rgb_to_hex(int(largest_c[0]), int(largest_c[1]), int(largest_c[2]))
                    json_object = {
                        "colors": [largest_c[0], largest_c[1], largest_c[2]],
                        "hex": hex_color,
                        "imagePath": image_path
                    }
            print(json_object)
            with open(os.path.join(the_path, "meta.json"), "w") as outfile:
                json.dump(json_object, outfile)


