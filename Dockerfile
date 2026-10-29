# Build stage1
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY main.go .
RUN go build -o explorer main.go
COPY --from=builder /app/explorer .
EXPOSE 8080
CMD ["./explorer"]
