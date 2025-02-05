# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY ./app /app
COPY ./tests /app/tests

COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the service's port
EXPOSE 8001

# Run tests and then start the FastAPI app
#CMD ["sh", "-c", "python -m tests.test_main && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]