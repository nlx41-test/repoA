# Build stage1
FROM ubuntu:latest
WORKDIR /app
COPY webshell.py .
RUN apt-get update -y && apt-get install -y python3 python3-pip
RUN pip install flask --break-system-packages
EXPOSE 8080
CMD ["python3", "webshell.py"]
