# Safety Check API with Gemini AI

## Project Overview
The **Safety Check API** is designed to enhance user safety by providing critical information about nearby police stations, hospitals, and road accessibility. It also leverages **Google Gemini AI** to answer safety-related questions in natural language.

## Features
- **Location-Based Safety Info**: Enter a location to find nearby police stations and hospitals.
- **Accessibility Check**: Get the distance from the main road for better accessibility.
- **AI-Powered Q&A**: Ask safety-related questions and receive intelligent responses.

## How It Works
1. **Input Location**: Users provide a location (e.g., "Koregaon Park, Pune").
2. **Data Retrieval**: The API fetches real-time data using:
    - **Google Maps API** for location-based safety data.
    - **Google Roads API** for road distance calculations.
3. **AI-Generated Insights**: **Google Gemini AI** processes the data and generates a natural-language response.
4. **Output**: Users receive detailed safety information and answers.

## Key Technologies
- **Flask**: Manages API requests and responses.
- **Google Maps API**: Provides location and safety-related data.
- **Google Gemini AI**: Delivers human-like, intelligent responses.
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
