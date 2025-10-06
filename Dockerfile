FROM python:3.10-slim

WORKDIR /app

# Install dependencies for building gssapi/kerberos
RUN apt-get update && apt-get install -y \
    build-essential \
    krb5-user \
    libkrb5-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Remove CMD from here
# CMD ["python", "sync_from_ipa.py"]
