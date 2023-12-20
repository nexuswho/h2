# Use the official Python image as the base image
FROM python:3.8-slim

# install google chrome
RUN apt-get update -y \
    && apt-get install -y wget gnupg xvfb unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update -y \
    && apt-get install -y google-chrome-stable

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 2.19
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR \
    && wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" \
    && unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR \
    && export PATH=$CHROMEDRIVER_DIR:$PATH

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Create a non-root user
RUN groupadd -r user && useradd -r -g user user

# Change the ownership of the app directory to the non-root user
RUN chown -R user:user /app

# Switch to the non-root user
USER user

# Expose both port 5000 and 8000 to the outside world
EXPOSE 5000
EXPOSE 8000

# Define environment variables
ENV FLASK_APP=app.py
ENV FLASK_APP_SERVER=server.py

# Run both Flask applications
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=5000 --with-threads & flask run --host=0.0.0.0 --port=8000"]
