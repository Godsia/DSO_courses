#!/bin/bash
set -e

echo "Testing container security and functionality..."

echo "1. Checking if container is running..."
docker compose ps | grep "Up" || exit 1

echo "2. Checking if running as non-root..."
USER_ID=$(docker compose exec -T app id -u)
if [ "$USER_ID" = "0" ]; then
    echo "ERROR: Container is running as root!"
    exit 1
fi
echo "✓ Running as user ID: $USER_ID"

echo "3. Checking health endpoint..."
curl -f http://localhost:8000/ || exit 1
echo "✓ Health endpoint OK"

echo "4. Checking info endpoint..."
curl -f http://localhost:8000/api/info || exit 1
echo "✓ Info endpoint OK"

echo "5. Checking container health status..."
HEALTH=$(docker compose ps --format json | jq -r '.[0].Health // "none"')
if [ "$HEALTH" != "healthy" ]; then
    echo "WARNING: Container health status: $HEALTH"
else
    echo "✓ Container is healthy"
fi

echo "All tests passed!"

