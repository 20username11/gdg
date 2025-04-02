from flask import Flask, request, jsonify
import requests
import google.generativeai as genai
import geopy.distance  # Library to calculate distances
from flask_cors import CORS
import json  # For debugging API responses

app = Flask(__name__)

CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
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

        places.extend([{"type": "police",
                "name": place["name"],
                "vicinity": place["vicinity"],
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"]
             } for place in police_response["results"][:3]])

        #places.extend([f"🚔 Police - {place['name']} - {place['vicinity']}" for place in police_response["results"][:3]])

    # 🔹 Search for Hospitals
    hospital_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=3000&type=hospital&key={GOOGLE_MAPS_API_KEY}"
    hospital_response = requests.get(hospital_url).json()
    if "results" in hospital_response:
        
        places.extend([{ "type": "hospital",
                "name": place["name"],
                "vicinity": place["vicinity"],
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"]} for place in hospital_response["results"][:3]])

        #places.extend([f"🏥 Hospital - {place['name']} - {place['vicinity']}" for place in hospital_response["results"][:3]])

    return places if places else [{"type": "none", "name": "No emergency locations found", "vicinity": ""}]
    #return places if places else ["No emergency locations found."]

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

def calculate_safety_score(lat, lng):
    """ Compute the refined safety score based on multiple factors """
    
    # Get safety-related data
    distance = get_distance_from_main_road(lat, lng) or 1000  # Default to high distance
    safety_info = get_safety_info(lat, lng)
    crime_level = get_crime_level(lat, lng)
    cctv_count = get_cctv_count(lat, lng)
    street_lighting = get_street_lighting_status(lat, lng)
    
    # Define scoring weights
    weights = {
        "distance": 20,  # Closer to main road = riskier
        "crime": 30,      # Higher crime reports = riskier
        "cctv": 25,       # More CCTV = safer
        "lighting": 25     # Well-lit streets = safer
    }
    
    # Distance score (inverse relation)
    distance_score = max(0, 20 - (distance / 50))  # Reducing score if too close
    
    # Crime level score
    crime_scores = {"low": 30, "moderate": 15, "high": 0}
    crime_score = crime_scores.get(crime_level, 15)  # Default to moderate
    
    # CCTV score (more cameras = safer)
    cctv_score = min(25, cctv_count * 5)  # 5 points per camera, max 25
    
    # Street lighting score
    lighting_score = 25 if street_lighting == "well-lit" else 10
    
    # Final score calculation
    total_score = distance_score + crime_score + cctv_score + lighting_score
    total_score = max(0, min(100, total_score))  # Clamp to 0-100
    
    return total_score


@app.route("/check_safety", methods=["POST"])
def check_safety():
    """ Return safety data with AI-generated safety score & locations. """
    data = request.json
    address = data.get("location", "").strip()
    if not address:
        return jsonify({"error": "Please provide a valid location"}), 400

    location = geocode_location(address)
    if not location:
        return jsonify({"error": "Could not find the location. Try again."}), 404

    user_lat, user_lng = location
    safety_info = get_safety_info(user_lat, user_lng)
    distance = get_distance_from_main_road(user_lat, user_lng)
    crime_level = get_crime_level(user_lat, user_lng)
    cctv_count = get_cctv_count(user_lat, user_lng)
    street_lighting = get_street_lighting_status(user_lat, user_lng)
    safety_score = calculate_safety_score(user_lat, user_lng)
    print("DEBUG: safety_info =", safety_info)  # Add this line
    
    if isinstance(safety_info, str):
        try:
            safety_info = json.loads(safety_info)  # Convert string to JSON
        except json.JSONDecodeError:
            return "Error: Invalid JSON format", 500  # Handle incorrect format

    safety_locations = ', '.join([place['name'] for place in safety_info])
 # 🔹 Generate AI response
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"""
    Ellaborate the safety of {address} based on these details:
    - Distance from main road: {distance} meters
    - Number of nearby emergency locations: {len(safety_info)} (police + hospitals)
    - Emergency locations list:
    {safety_locations}
    - Crime level: {crime_level}
    - Number of CCTVs: {cctv_count}
    - Street lighting: {street_lighting}
    - Computed safety score: {safety_score}

    🔹 **Return the result in strict JSON format:**
    {{
      "response": "A natural language summary of safety",
      "safety_score": {safety_score}
    }}
    """
    
    try:
        ai_response = model.generate_content(prompt).text
        ai_data = json.loads(ai_response)  # Convert Gemini's response to JSON
    except json.JSONDecodeError:
        print("⚠️ Gemini response is not valid JSON, using fallback...")
        ai_data = {"response": ai_response, "safety_score": safety_score}  
    
    return jsonify({
        "location": address,
        "lat": user_lat,
        "lng": user_lng,
        "distance_from_main_road": f"{distance} meters" if distance is not None else "N/A",
        "crime_level": crime_level,
        "cctv_count": cctv_count,
        "street_lighting": street_lighting,
        "ai_response": ai_data["response"],  # Natural language response
        "safety_score": ai_data["safety_score"],  # AI-generated safety score
        "safety_locations": safety_info  # Emergency locations with coordinates
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
