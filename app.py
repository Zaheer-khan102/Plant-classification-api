from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow CORS for all domains

# Replace with your actual Pl@ntNet API Key
PLANTNET_API_KEY = "2b10JDPN25AlR1rzALtFgdWb5e"

@app.route('/identify', methods=['POST'])
def identify_plant():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']
    files = {'images': (image.filename, image.stream, image.mimetype)}

    # PlantNet API endpoint
    url = f"https://my-api.plantnet.org/v2/identify/all?api-key={PLANTNET_API_KEY}"
    
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            best_match = data["results"][0]  # Taking the most confident result

            plant_info = best_match.get("species", {})
            scientific_name = plant_info.get("scientificNameWithoutAuthor", "Unknown")
            family = plant_info.get("family", {}).get("scientificName", "Unknown")
            genus = plant_info.get("genus", {}).get("scientificName", "Unknown")
            common_names = plant_info.get("commonNames", ["Not available"])
            confidence_score = best_match.get("score", 0) * 100  # Convert to percentage
            
            # Check if medicinal properties are available in the API
            uses = plant_info.get("medicinal", {}).get("description", "Not available")

            result = {
                "scientific_name": scientific_name,
                "family": family,
                "genus": genus,
                "confidence": round(confidence_score, 2),
                "common_names": common_names,
                "uses": uses
            }
            return jsonify(result)
        else:
            return jsonify({"error": "No plant found"}), 404
    else:
        return jsonify({"error": "API request failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
