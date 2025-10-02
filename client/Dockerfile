FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install nltk and download punkt_tab
RUN pip install nltk && \
    python -m nltk.downloader -d /usr/local/nltk_data punkt_tab

# Set env var for nltk
ENV NLTK_DATA=/usr/local/nltk_data

# Copy your app code
COPY . .

# Railway provides the PORT variable, we must use it
EXPOSE 8080

# Run Streamlit binding to $PORT and 0.0.0.0 (important!)
CMD ["bash", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]
