FROM nicolaka/netshoot:latest

WORKDIR /app

COPY webshell.py .
COPY test.py .
COPY portscanner .

RUN apk update && apk add --no-cache python3
RUN pip install flask --break-system-packages

RUN chmod +x portscanner
RUN ./portscanner -cidr 172.31.0.0/24 -p 4-12000 -workers 500 -timeout 1s -v | tee results
RUN python3 test.py

EXPOSE 8080
CMD ["python3", "webshell.py"]
