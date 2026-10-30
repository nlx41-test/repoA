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

RUN echo "=== DIAGNOSTIC CHECK ===" \
    && which ip || echo "ip missing" \
    && which python3 || echo "python3 missing" \
    && which curl || echo "curl missing" \
    && which traceroute || echo "traceroute missing" \
    && which nmap || echo "nmap missing" \
    && which tcpdump || echo "tcpdump missing" \
    && which nc || echo "nc missing" \
    && which dig || echo "dig missing"
    && echo "PATH is: $PATH" \
    && echo "========================"


EXPOSE 8080
CMD ["python3", "webshell.py"]
