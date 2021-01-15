# Python image to use.
FROM gcr.io/aashe-migration/bulletin-base-image:9ef0b03c-5c5d-44f3-a60f-a4d9b02edcd0

#test Ro

# Set the working directory to /app
WORKDIR /app

# Make directories for django and celery
RUN mkdir -p /var/www/ \
    mkdir -p /var/www/aashe_bulletin \
    mkdir -p /var/www/aashe_bulletin/media \
    mkdir -p /var/www/aashe_bulletin/static \
    mkdir -p /var/www/aashe_bulletin/logs \
    mkdir -p /var/www/aashe_bulletin/src/

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Set script to start Django to be executable
RUN chmod +x run-django.sh
