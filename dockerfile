# Use the official Python image as the base image
FROM python:3.12-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget unzip curl gnupg && \
    apt-get install -y libnss3 libgconf-2-4 libxss1 libappindicator3-1 libasound2 && \
    rm -rf /var/lib/apt/lists/*

# Add Google Chrome’s official GPG key
RUN curl -sSL https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Set up the Google Chrome repository
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install the latest version of Chrome
RUN apt-get update && apt-get install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the project files
COPY . /app
WORKDIR /app

# Run pytest with allure reporting
CMD ["pytest"]
