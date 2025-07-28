FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
COPY analyze_persona_docs.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "analyze_persona_docs.py"] 