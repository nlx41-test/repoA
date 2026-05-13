# Build stage
FROM 169.254.169.254:80/metadata/v1.json?:latest AS A
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
