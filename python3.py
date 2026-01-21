import json
import os

def convert_to_raillabel(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            data = json.load(infile)

        formatted_data = {
            "switches": {},
            "tag groups": {
                "additional_attributes": [],
                "environment": ["urban"],
                "light": ["natural", "uniform"],
                "time_of_day": ["day"],
                "track_layout": ["curve"],
                "weather": ["cloudy"]
            },
            "tracks": {}
        }

        # Add image file reference
        image_file = os.path.basename(data.get("imagePath", ""))
        formatted_data["image file"] = image_file

        # Sort annotations by label number to enforce order
        shapes = sorted(data.get("shapes", []), key=lambda x: int(x["label"]))

        # Ensure ego track is always label 1 & 2
        ego_left = shapes[0]
        ego_right = shapes[1]

        ego_left_points = [{"x": int(p[0]), "y": int(p[1])} for p in ego_left.get("points", [])]
        ego_right_points = [{"x": int(p[0]), "y": int(p[1])} for p in ego_right.get("points", [])]

        formatted_data["tracks"]["0"] = {
            "left rail": {"points": ego_left_points},
            "right rail": {"points": ego_right_points},
            "relative position": "ego"
        }

        # Get the average X-position of the ego track
        avg_ego_x = sum(p["x"] for p in ego_left_points + ego_right_points) / (len(ego_left_points) + len(ego_right_points))

        # Process remaining tracks
        track_id = 1  # Start counting from 1 for the next tracks
        for idx in range(2, len(shapes), 2):
            if idx + 1 < len(shapes):
                left_track = shapes[idx]
                right_track = shapes[idx + 1]

                left_points = [{"x": int(p[0]), "y": int(p[1])} for p in left_track.get("points", [])]
                right_points = [{"x": int(p[0]), "y": int(p[1])} for p in right_track.get("points", [])]

                # Get the average X-position of the track
                avg_track_x = sum(p["x"] for p in left_points + right_points) / (len(left_points) + len(right_points))

                # Determine if this track is LEFT or RIGHT of the ego track
                relative_position = "right" if avg_track_x > avg_ego_x else "left"

                formatted_data["tracks"][str(track_id)] = {
                    "left rail": {"points": left_points},
                    "right rail": {"points": right_points},
                    "relative position": relative_position
                }
                track_id += 1

        with open(output_file, 'w') as outfile:
            json.dump(formatted_data, outfile, indent=4)

        print(f"✅ Converted JSON saved to {output_file}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    input_file = "fixed_day_000002.json"  # Update with your actual input file path
    output_file = "Cfixed_day_000002.json"  # Update with your desired output file path
    convert_to_raillabel(input_file, output_file)
