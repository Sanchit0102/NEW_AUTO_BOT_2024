FROM python:3.10.8-slim-buster

# Update and install necessary packages
RUN apt update && \
    apt upgrade -y && \
    apt install -y git dos2unix

# Copy and install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip3 install -U pip && pip3 install -U -r /requirements.txt

# Create working directory and set it
RUN mkdir /NewAuto
WORKDIR /NewAuto

# Copy the start script and convert line endings
COPY start.sh /start.sh
RUN dos2unix /start.sh && chmod +x /start.sh

# Set the command to run the start script
CMD ["/bin/bash", "/start.sh"]
