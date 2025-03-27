🚀 Project Summary: Safety Check API with Gemini AI
🔹 What We Built:
We created a Safety Check API that allows users to:
✅ Enter a location and get nearby police stations & hospitals 🚔🏥
✅ Check the distance from the main road for accessibility 🚗
✅ Ask safety-related questions using Google Gemini AI 🤖

🔹 How It Works:
1️⃣ User enters a location (e.g., "Koregaon Park, Pune")
2️⃣ The API fetches real-time data from Google Maps & Roads API
3️⃣ It returns safety info (police stations, hospitals, road distance)
4️⃣ Gemini AI generates a natural-language answer combining real data

🔹 Key Technologies Used:
🟢 Flask → Handles API requests
🟢 Google Maps API → Fetches safety-related data
🟢 Google Gemini AI → Generates human-like responses
🟢 Docker → Containerized for easy deployment

🔹 How to Run It:
📌 Start the API:

bash
Copy
Edit
docker-compose up --build
📌 Test Safety Info:

bash
Copy
Edit
curl -X POST http://localhost:5000/check_safety -H "Content-Type: application/json" -d '{"location": "Koregaon Park, Pune"}'
📌 Test AI Chatbot:

bash
Copy
Edit
curl -X POST http://localhost:5000/chatbot -H "Content-Type: application/json" -d '{"query": "Is Koregaon Park safe at night?"}'
🔹 Why This is Useful:
🔹 Helps users choose a safe place to live 🏡
🔹 Provides real-time emergency info 🚨
🔹 Uses AI to simplify safety insights 💡
