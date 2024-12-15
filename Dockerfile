# Use a lightweight Python 3.11 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only the requirements file to avoid unnecessary files during image build
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Flask project into the container
COPY . .

# Expose the Flask default port (usually 5000)
EXPOSE 5000

# Set the environment variable to avoid some warnings related to Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Start the Flask application
CMD ["flask", "run"]
