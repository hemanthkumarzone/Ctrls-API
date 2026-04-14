#!/bin/bash

# AI FinOps Platform - Start Script

set -e

echo "🚀 Starting AI FinOps Platform..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create one based on .env.example"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Wait for database
echo "⏳ Waiting for database..."
while ! pg_isready -h localhost -p 5432 -U finops > /dev/null 2>&1; do
    sleep 1
done

# Run migrations
echo "🗄️ Running database migrations..."
alembic upgrade head

# Start the application
echo "🌟 Starting FastAPI server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000