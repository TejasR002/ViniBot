# Use official Python image

FROM python:3.11-slim

# Set environment variables

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# Set working directory

WORKDIR /app

# Copy requirement files

COPY requirements.txt .

# Install dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app

COPY . .

# Expose Streamlit default port

EXPOSE 8501

# Set entry point to run Streamlit app

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

