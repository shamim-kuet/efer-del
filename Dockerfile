# Use the official Python 3.8 image as the base image
FROM python:3.8

# Set an environment variable to prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /django

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    apt-utils \
    curl \
    lsof \
    nginx \
    supervisor

# Copy the requirements.txt file to the working directory
COPY requirements.txt requirements.txt

# Install Python dependencies from the requirements.txt file
RUN pip install --upgrade pip && pip3 install -r requirements.txt 

# Copy the entire project to the working directory in the container
COPY . /django

# Collect static files
RUN mkdir -p /django/static
RUN python manage.py collectstatic --noinput

# Copy the Nginx configuration files to the container
COPY nginx.conf.normal /etc/nginx/sites-available/default
# COPY proxy_params /etc/nginx/proxy_params
# COPY nginx.conf.normal /etc/nginx/http.d/default.conf

# Copy the Supervisor configuration file
COPY supervisord.conf.normal /etc/supervisor/conf.d/supervisord.conf

# Set up permissions
RUN chown -R www-data:www-data /django    

# Expose port 8000 for the Django application
EXPOSE 8000

# Command to run Supervisor
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]