FROM alpine:latest

WORKDIR /app
COPY webshell.py .

RUN apk update && apk add --no-cache \
    iputils \
    iproute2 \
    net-tools \
    bind-tools \
    curl \
    wget \
    traceroute \
    tcpdump \
    nmap \
    netcat-openbsd \
    iperf3 \
    python3

EXPOSE 8080
CMD ["python3", "webshell.py"]
