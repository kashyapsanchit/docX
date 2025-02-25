FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENV=production

WORKDIR /src

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . /src

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000  
EXPOSE 8501  

CMD ["sh", "-c", "uvicorn src.app.main:app & streamlit run src/streamlit_app.py"]
