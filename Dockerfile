# Stage 1: Build dependencies
FROM python:3.14-slim AS builder

WORKDIR /usr/src

# Copy only necessary files
COPY app/ app/

# Final Stage: Minimal runtime image
FROM python:3.14-slim

WORKDIR /usr/src

# Copy only necessary files from builder
COPY --from=builder /usr/src/app /usr/src/app

# Run the main script
ENTRYPOINT ["python", "/usr/src/app/main.py"]
