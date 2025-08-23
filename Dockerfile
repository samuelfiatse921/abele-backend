FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Optional tools
ARG BUILD_TOOLS=false
RUN apt-get update && \
    if [ "$BUILD_TOOLS" = "true" ]; then \
        apt-get install -y --no-install-recommends \
            curl \
            iputils-ping; \
    fi && \
    rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock ./

# Install the dependencies
RUN pipenv install

# Copy the application code into the container
COPY app app

# Set the environment variable
ENV PYTHONPATH=/app

# Expose the port that the app runs on
EXPOSE 9000

# Command to run the application
CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
