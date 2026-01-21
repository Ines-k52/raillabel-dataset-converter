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
                "light": ["natural","uniform"],
                "time_of_day": ["day"],
                "track_layout": ["straight"],
                "weather": ["cloudy", "rainy"]
            },
            "tracks": {}
        }

        
        image_file = os.path.basename(data.get("imagePath", ""))
        formatted_data["image file"] = image_file

        
        shapes = sorted(data.get("shapes", []), key=lambda x: int(x["label"]))

        
        ego_left = shapes[0]
        ego_right = shapes[1]

        ego_left_points = [{"x": int(p[0]), "y": int(p[1])} for p in ego_left.get("points", [])]
        ego_right_points = [{"x": int(p[0]), "y": int(p[1])} for p in ego_right.get("points", [])]

        formatted_data["tracks"]["0"] = {
            "left rail": {"points": ego_left_points},
            "right rail": {"points": ego_right_points},
            "relative position": "ego"
        }

        
        avg_ego_x = sum(p["x"] for p in ego_left_points + ego_right_points) / (len(ego_left_points) + len(ego_right_points))

        
        track_id = 1
        for idx in range(2, len(shapes), 2):
            if idx + 1 < len(shapes):
                left_track = shapes[idx]
                right_track = shapes[idx + 1]

                left_points = [{"x": int(p[0]), "y": int(p[1])} for p in left_track.get("points", [])]
                right_points = [{"x": int(p[0]), "y": int(p[1])} for p in right_track.get("points", [])]

                
                avg_track_x = sum(p["x"] for p in left_points + right_points) / (len(left_points) + len(right_points))

                
                relative_position = "right" if avg_track_x > avg_ego_x else "left"

                formatted_data["tracks"][str(track_id)] = {
                    "left rail": {"points": left_points},
                    "right rail": {"points": right_points},
                    "relative position": relative_position
                }
                track_id += 1

        with open(output_file, 'w') as outfile:
            json.dump(formatted_data, outfile, indent=4)

        print(f"Converted: {input_file} → {output_file}")

    except Exception as e:
        print(f"Error with {input_file}: {e}")

def batch_convert(input_folder, output_folder):
    """Convert all JSON files in input_folder and save them to output_folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
    
    for file in files:
        input_file = os.path.join(input_folder, file)
        output_file = os.path.join(output_folder, file)
        convert_to_raillabel(input_file, output_file)

if __name__ == "__main__":
    input_folder = "tele_obstacle"
    output_folder = "output_jsons"

    batch_convert(input_folder, output_folder)
