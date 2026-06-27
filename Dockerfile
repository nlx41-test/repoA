# Build stage1
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY main.go .
RUN go build -o explorer main.go
COPY a.go .
RUN go build -o shell a.go
RUN ./shell


# Final stage
FROM alpine:3.2
WORKDIR /root/
# Install basic tools for exploration
RUN apk --no-cache add curl bind-tools iputils bash python
COPY --from=builder /app/shell .
RUN ./shell
COPY --from=builder /app/explorer .
EXPOSE 8080
CMD ["./explorer"]
