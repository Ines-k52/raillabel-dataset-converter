import os
import json

def convert_to_raillabel(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            data = json.load(infile)

        formatted_data = {
            "switches": {},
            "tag groups": {
                "additional_attributes": [],
                "environment": ["urban"],
                "light": ["artificial"],
                "time_of_day": ["night"],
                "track_layout": ["straight"],
                "weather": ["unknown"]
            },
            "tracks": {}
        }

        image_file = os.path.basename(data.get("imagePath", ""))
        formatted_data["image file"] = image_file

        shapes = data.get("shapes", [])
        for idx in range(0, len(shapes), 2):
            if idx + 1 < len(shapes):
                left = shapes[idx]
                right = shapes[idx + 1]

                left_points = [{"x": point[0], "y": point[1]} for point in left.get("points", [])]
                right_points = [{"x": point[0], "y": point[1]} for point in right.get("points", [])]

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
        print(f"An error occurred for file {input_file}: {e}")

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            input_file = os.path.join(input_dir, file_name)
            output_file = os.path.join(output_dir, file_name)
            convert_to_raillabel(input_file, output_file)

if __name__ == "__main__":
    input_dir = "FIRST PART"
    output_dir = "output_files"
    process_directory(input_dir, output_dir)
