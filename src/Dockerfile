# Python image to use.
FROM gcr.io/aashe-migration/bulletin-base-image:4663dc6b-38cc-49fb-b47e-eb53aaa03252

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