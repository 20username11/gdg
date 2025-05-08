# Find Her

## Project Summary: Empowering Women with Safety and Support

**Find Her** is a comprehensive solution designed to empower women by providing critical safety insights and mental support. This project leverages advanced technologies to ensure women feel safe and supported in their daily lives. Here's how it helps:

### 1. **Safest Routes**:
   - Women can find the safest routes to their destinations by analyzing real-time data on nearby police stations, hospitals, and road accessibility.
   - The system calculates a **safety score** for each route, helping users make informed decisions about their travel paths.
   - The app displays the **three best paths** based on the safety score, ensuring users can choose the safest option.

### 2. **Safest Locations to Live**:
   - By analyzing crime data, CCTV presence, and street lighting, the platform identifies the safest neighborhoods for women to live.
   - Users can explore detailed safety insights for specific locations, ensuring peace of mind when choosing a place to reside.

### 3. **Chatbot for Mental Support**:
   - The integrated **AI-powered chatbot** provides a safe space for women to share their concerns and receive empathetic, intelligent responses.
   - Whether it's addressing safety-related questions or offering mental support, the chatbot is always available to assist.

### Vision:
This project aims to create a safer and more supportive environment for women by combining technology, real-time data, and AI-driven insights. By empowering women with actionable safety information and emotional support, we strive to make the world a safer place for everyone.
## Features

- **Location-Based Safety Info**:  
  Users can enter a location to find nearby police stations and hospitals. This feature ensures that women have access to critical emergency services in their vicinity, providing a sense of security and preparedness.

- **Accessibility Check**:  
  The app calculates the distance from the main road for any given location. This helps users understand how accessible a location is, which is crucial for safety, especially in emergencies.

- **AI-Powered Q&A**:  
  The integrated AI chatbot allows users to ask safety-related questions and receive intelligent, empathetic responses. Whether it's about the safety of a route, a neighborhood, or general safety tips, the chatbot provides accurate and helpful information.

- **Safety Score for Routes**:  
  The app calculates a **safety score** for each route by analyzing factors such as nearby emergency services, crime data, and road accessibility. Based on this score, the app displays the **three safest routes**, enabling users to make informed travel decisions.

- **Neighborhood Safety Insights**:  
  By analyzing crime data, CCTV presence, and street lighting, the app identifies the safest neighborhoods for women to live. This feature helps users choose a safe and secure place to reside, ensuring peace of mind.

- **Real-Time Data Integration**:  
  The app leverages real-time data from Google Maps and other APIs to provide up-to-date safety information. This ensures that users always have the most accurate and relevant data at their fingertips.

- **Empathetic Mental Support**:  
  The AI-powered chatbot is not just for safety-related queries but also serves as a mental support system. Women can share their concerns and receive empathetic, intelligent responses, making it a safe space for emotional well-being.

## How It Works
1. **Input Location**: Users provide a location (e.g., "Koregaon Park, Pune").
2. **Data Retrieval**: The API fetches real-time data using:
    - **Google Maps API** for location-based safety data.
    - **Google Roads API** for road distance calculations.
3. **AI-Generated Insights**: **Google Gemini AI** processes the data and generates a natural-language response.
4. **Output**: Users receive detailed safety information and answers.

## Key Technologies

- **Flask**: Manages API requests and responses.
- **Google Maps API**: Provides location-based data, such as nearby police stations, hospitals, and other points of interest.
- **Google Roads API**: Determines the nearest main road to a given location and calculates the distance from the user's location to the nearest main road.
- **Google Places API**: Fetches detailed information about places, such as police stations and hospitals, including names, addresses, and coordinates.
- **Google Street View API**: Analyzes street lighting conditions by fetching metadata for a given location, helping determine whether a location is well-lit or poorly lit.
- **Google Dialogflow**: Powers the chatbot for natural language understanding and intent detection, enabling intelligent responses to user queries.
- **Google Gemini AI**: Delivers human-like, AI-powered responses for safety-related queries, enhancing the chatbot's ability to provide empathetic and intelligent answers.
- **Docker**: Ensures seamless deployment with containerization.

## Getting Started
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/safety-check-api.git
    ```
2. Build and run the Docker container:
    ```bash
    docker build -t safety-check-api .
    docker run -p 5000:5000 safety-check-api
    ```
3. Access the API at `http://localhost:5000`.



---
Empowering safety with technology!
