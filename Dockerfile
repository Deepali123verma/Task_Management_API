# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all project files to working directory
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# (Optional but useful) Generate RSA key files at build time
RUN python generate_keys.py

# Expose port 5000 for Flask
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run"]

