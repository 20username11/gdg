from flask import Flask, request, jsonify
import requests
import google.generativeai as genai
import geopy.distance  # Library to calculate distances
import json  # For debugging API responses

app = Flask(__name__)

# 🔹 Replace with your actual Google Maps API Key
GOOGLE_MAPS_API_KEY = "AIzaSyAohWXg1BFJZYRt2i1FNimNv881qoSx4dM"
GEMINI_API_KEY = "AIzaSyAohWXg1BFJZYRt2i1FNimNv881qoSx4dM"
genai.configure(api_key=GEMINI_API_KEY)


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Safety Check API! Use /check_safety to check location safety."})

def geocode_location(address):
    """ Convert user-entered address into latitude & longitude """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url).json()

    if response["status"] == "OK":
        location = response["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None

def get_nearest_main_road(lat, lng):
    """ Find the nearest main road to the given coordinates """
    url = f"https://roads.googleapis.com/v1/nearestRoads?points={lat},{lng}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url).json()

    if "snappedPoints" in response:
        snapped_location = response["snappedPoints"][0]["location"]
        return snapped_location["latitude"], snapped_location["longitude"]
    return None  # Return None if no roads are found

def get_distance_from_main_road(user_lat, user_lng):
    """ Calculate the distance between the user's location and the nearest main road """
    main_road_location = get_nearest_main_road(user_lat, user_lng)
    if main_road_location:
        return round(geopy.distance.geodesic((user_lat, user_lng), main_road_location).meters, 2)
    return None

def get_safety_info(lat, lng):
    """ Fetch nearby police stations and hospitals separately """
    places = []

    # 🔹 Search for Police Stations
    police_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=3000&type=police&key={GOOGLE_MAPS_API_KEY}"
    police_response = requests.get(police_url).json()
    if "results" in police_response:
        places.extend([f"🚔 Police - {place['name']} - {place['vicinity']}" for place in police_response["results"][:3]])

    # 🔹 Search for Hospitals
    hospital_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=3000&type=hospital&key={GOOGLE_MAPS_API_KEY}"
    hospital_response = requests.get(hospital_url).json()
    if "results" in hospital_response:
        places.extend([f"🏥 Hospital - {place['name']} - {place['vicinity']}" for place in hospital_response["results"][:3]])

    return places if places else ["No emergency locations found."]

def get_crime_level(lat, lng):
    """ Analyze Google Places reviews of nearby police stations for crime reports """
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=3000&type=police&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url).json()
    if "results" not in response:
        return "moderate"  # Default to moderate if no data

    crime_keywords = ["robbery", "theft", "murder", "assault", "unsafe", "scam"]
    crime_count = 0

    for place in response["results"]:
        place_id = place["place_id"]
        reviews_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=reviews&key={GOOGLE_MAPS_API_KEY}"
        reviews_response = requests.get(reviews_url).json()

        if "result" in reviews_response and "reviews" in reviews_response["result"]:
            for review in reviews_response["result"]["reviews"]:
                for word in crime_keywords:
                    if word in review["text"].lower():
                        crime_count += 1

    if crime_count >= 10:
        return "high"
    elif crime_count >= 3:
        return "moderate"
    return "low"

def get_cctv_count(lat, lng):
    """ Fetch the number of CCTV cameras from Google Places API """
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=1000&keyword=CCTV&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url).json()
    return len(response.get("results", []))  # Count the number of CCTV locations

def get_street_lighting_status(lat, lng):
    """ Analyze street lighting using Google Street View API """
    url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={lat},{lng}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url).json()
    return "well-lit" if response.get("status") == "OK" else "poorly-lit"

def calculate_safety_score(num_safety_places, distance_to_road, crime_level, num_cctv, lighting_status):
    """ Calculates a Safety Score (0-100) based on emergency places, distance from roads, crime data, CCTV, and lighting """
    score = 0

    if num_safety_places >= 3:
        score += 40
    elif num_safety_places >= 1:
        score += 20

    if distance_to_road is not None:
        if distance_to_road < 50:
            score += 40
        elif distance_to_road < 200:
            score += 20

    if crime_level == "high":
        score -= 40
    elif crime_level == "moderate":
        score -= 20

    if num_cctv >= 5:
        score += 20
    elif num_cctv >= 1:
        score += 10

    if lighting_status == "well-lit":
        score += 20

    return max(0, min(score, 100))

@app.route("/check_safety", methods=["POST"])
def check_safety():
    """ User enters a location, and we return real-time safety data. """
    data = request.json
    address = data.get("location", "").strip()

    if not address:
        return jsonify({"error": "Please provide a valid location"}), 400

    location = geocode_location(address)
    if not location:
        return jsonify({"error": "Could not find the location. Try again."}), 404

    user_lat, user_lng = location
    distance_to_road = get_distance_from_main_road(user_lat, user_lng)
    safety_info = get_safety_info(user_lat, user_lng)

    crime_level = get_crime_level(user_lat, user_lng)
    num_cctv = get_cctv_count(user_lat, user_lng)
    lighting_status = get_street_lighting_status(user_lat, user_lng)

    safety_score = calculate_safety_score(len(safety_info), distance_to_road, crime_level, num_cctv, lighting_status)

    return jsonify({
        "location": address,
        "distance_from_main_road": f"{distance_to_road} meters",
        "safety_info": safety_info,
        "crime_level": crime_level,
        "cctv_count": num_cctv,
        "street_lighting": lighting_status,
        "safety_score": f"{safety_score}/100"
    })
@app.route("/chatbot", methods=["POST"])
def chatbot():
    """ Process user safety queries, extract location details, fetch data, and respond naturally using Gemini AI. """
    data = request.json
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "Please provide a valid query"}), 400

    try:
        # Step 1: Use Gemini AI to infer the location from the query
        model = genai.GenerativeModel("gemini-1.5-pro")
        infer_response = model.generate_content(
            f"Extract only the location name (if present) from this question: {user_query}. If no location is mentioned, respond with 'None'."
        )
        location_name = infer_response.text.strip()

        if location_name.lower() == "none":
            return jsonify({"error": "Please specify a location in your query."}), 400

        # Step 2: Convert location name to coordinates
        location = geocode_location(location_name)
        if not location:
            return jsonify({"error": "Could not find the location. Try again."}), 404

        lat, lng = location

        # Step 3: Fetch safety-related data
        safety_info = get_safety_info(lat, lng)
        distance = get_distance_from_main_road(lat, lng)

        # Step 4: Generate a natural language response using Gemini AI
        safety_details = f"Location: {location_name}\n"
        safety_details += f"Distance from main road: {distance} meters\n"
        safety_details += "Nearby emergency locations:\n" + "\n".join(safety_info)

        final_response = model.generate_content(
            f"Based on this safety data, answer the user's question naturally:\n{user_query}\n\n{safety_details}"
        )

        return jsonify({"response": final_response.text})

    except Exception as e:
        return jsonify({"error": "Failed to process the query", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
