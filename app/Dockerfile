# Set the base image
FROM debian:13-slim

# Upgrade the system
RUN apt update && apt upgrade -y

# Install Python
RUN apt update && apt install -y python-is-python3

# Install SQLite
RUN apt update && apt install -y sqlite3

# Copy source code from the project to the container
COPY server /root/server

# Set the working directory
WORKDIR /root/server

# Run the server Python script
CMD ["python", "server.py"]
