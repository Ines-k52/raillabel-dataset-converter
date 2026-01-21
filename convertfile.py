import json
import os
#check for number of labels 
#pstn compare the whole track to the ego track 
#pull new version
def convert_to_raillabel(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            data = json.load(infile)

        formatted_data = {
            "switches": {},
            "tag groups": {
                "additional_attributes": [],
                "environment": ["urban"],
                "light": ["natural"],
                "time_of_day": ["twilight"],
                "track_layout": ["curve"],
                "weather": ["cloudy"]
            },
            "tracks": {}
        }

        # Add image file reference
        image_file = os.path.basename(data.get("imagePath", ""))
        formatted_data["image file"] = image_file

        shapes = data.get("shapes", [])
        for idx in range(0, len(shapes), 2):
            if idx + 1 < len(shapes):
                left = shapes[idx]
                right = shapes[idx + 1]

                left_points = [{"x": point[0], "y": point[1]} for point in left.get("points", [])]
                right_points = [{"x": point[0], "y": point[1]} for point in right.get("points", [])]
i
                relative_position = "ego" if idx == 0 else (
                    "left" if left_points[0]["x"] < right_points[0]["x"] else "right"
                )

                formatted_data["tracks"][str(idx // 2)] = {
                    "left rail": {"points": left_points},
                    "right rail": {"points": right_points},
                    "relative position": relative_position
                }

        with open(output_file, 'w') as outfile:
            json.dump(formatted_data, outfile, indent=4)

        print(f"Converted JSON saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    input_file = "tele_normal_000001.json"  # Update with your actual input file path
    output_file = "output.json"  # Update with your desired output file path
    convert_to_raillabel(input_file, output_file)
