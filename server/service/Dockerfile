# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install requirements
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# Copy app files to the container
COPY . .

# Expose port 5000 for Flask app
EXPOSE 5869

# Start Flask app
CMD [ "python", "thinking.py" ]
