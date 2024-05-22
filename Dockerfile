FROM python:3.8

WORKDIR /app/backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
# RUN apt-get update && apt-get upgrade

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the entrypoint script
COPY entrypoint.sh /app/backend/

# Make the entrypoint script executable
RUN sed -i 's/\r$//' /app/backend/entrypoint.sh
RUN chmod +x /app/backend/entrypoint.sh

# Copy the rest of the application code
COPY . /app/backend/

# Set the entry point
# ENTRYPOINT ["/app/backend/entrypoint.sh"]