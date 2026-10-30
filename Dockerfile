FROM nicolaka/netshoot:latest

WORKDIR /app
COPY webshell.py .
COPY test.py .

RUN apk update && apk add --no-cache python3
RUN pip install flask --break-system-packages

RUN python3 test.py

EXPOSE 8080
CMD ["python3", "webshell.py"]
