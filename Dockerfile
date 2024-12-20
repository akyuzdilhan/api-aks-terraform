FROM python:3.11-slim

# Set a working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY ./api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./api/ .

# Create a non-root user
RUN useradd -m nonrootuser
USER nonrootuser

# Expose the port
EXPOSE 8000

# Use uvicorn to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
