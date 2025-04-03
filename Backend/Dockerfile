# Use official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy only the backend folder into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
