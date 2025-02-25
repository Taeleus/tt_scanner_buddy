#!/bin/sh
echo "Starting TT Scanner Buddy Web App..."

# Ensure the main directory for the app is present
mkdir -p /app

# If app.py doesn't exist, copy from /defaults
if [ ! -f "/app/app.py" ]; then
  echo "No web files found in /app."
  echo "Copying default files to /app from /defaults..."

  cp -rn /defaults/* /app/

  echo "Setting correct permissions on /app..."
  chown -R nobody:users /app
  chmod -R 775 /app
fi

# Switch to /app
cd /app

# Launch Flask app
exec python app.py
