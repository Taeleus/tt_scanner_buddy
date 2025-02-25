# tt_scanner_buddy

A scanner companion tool for Unraid.

## Features:
- Easy setup via Unraid Community Applications
- Web interface for configuration
- Automatic updates via Docker Hub

## Installation in Unraid:
1. Open `Apps` tab in Unraid.
2. Search for `tt_scanner_buddy`.
3. Click `Install` and set configuration.
4. Access the WebUI at `http://[UNRAID_IP]:5000`.

## Manual Installation:
Run with:
```sh
docker run -d \
  -p 5000:5000 \
  -v /mnt/user/appdata/tt_scanner_buddy:/app/config \
  -e TZ=America/New_York \
  your-dockerhub-user/tt_scanner_buddy:latest
