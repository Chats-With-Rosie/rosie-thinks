# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY server/service/requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set the environment variable for flask
ENV FLASK_APP=server.service.think

# Expose port 5069 for Flask app
EXPOSE 5069

# Run the command to start Flask app
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5069"]
