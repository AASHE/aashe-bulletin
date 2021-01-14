# Python image to use.
FROM gcr.io/aashe-migration/bulletin-base-image:405c6e9b-6622-40e1-a202-22bf67525874

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
