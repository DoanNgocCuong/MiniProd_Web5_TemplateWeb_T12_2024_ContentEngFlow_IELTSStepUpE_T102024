FROM python:3.9-slim

WORKDIR /app


# Install curl and other dependencies
# Ko có Curl thì SCRIPT generate_ipa.py sẽ gen ra mỗi file .exls nhưng ko có audio (còn khi run riêng python generate_ipa.py thì lại có audio)
# RUN apt-get update && \
#     apt-get install -y curl && \
#     rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"] 