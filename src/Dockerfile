# app/Dockerfile
FROM python:3.9-slim-bullseye

EXPOSE 8080
WORKDIR /src
COPY . ./

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --root --upgrade pip
RUN pip config list -v
RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the web service on container startup
CMD ["streamlit", "run", "main.py", "--server.port=8080"]