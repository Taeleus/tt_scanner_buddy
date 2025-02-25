FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy and install requirements first
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy everything into /defaults (to populate /app if empty)
COPY . /defaults/

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 5000 for Flask
EXPOSE 5000

# Use entrypoint to set up the container
ENTRYPOINT ["/entrypoint.sh"]
