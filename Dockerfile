FROM nicolaka/netshoot:latest

WORKDIR /app
COPY webshell.py .

RUN apk update && apk add --no-cache python3
RUN pip install flask --break-system-packages

EXPOSE 8080
CMD ["python3", "webshell.py"]
