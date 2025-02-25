FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies first for caching
COPY docker/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make entrypoint executable
RUN chmod +x docker/entrypoint.sh

# Expose port 5000 instead of 8080
EXPOSE 5000

# Define entrypoint
ENTRYPOINT ["sh", "docker/entrypoint.sh"]
