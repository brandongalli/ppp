# Use an official PHP runtime as a parent image
FROM php:8.1-cli

# Install system dependencies including git
RUN apt-get update && apt-get install -y \
    git \
    unzip

# Set the working directory
WORKDIR /var/www/slim_app

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN composer install --no-dev --no-scripts --no-progress

# Expose port 8000
EXPOSE 8000

# Run Slim app using PHP's built-in server
CMD ["php", "-S", "0.0.0.0:8000", "-t", "src"]
