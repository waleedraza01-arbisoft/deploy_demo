# Use a lightweight Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY app/requirements.txt .

# Install dependencies
# We install pytorch cpu version explicitly to keep the image small
RUN pip install --upgrade pip
# RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir "torch>=2.6.0" --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app/ ./app

# Expose the port
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]