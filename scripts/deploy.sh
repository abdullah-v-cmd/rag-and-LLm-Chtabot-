#!/bin/bash

# Production deployment script using Docker

echo "🚀 Deploying LLM RAG Chatbot with Docker"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating from example..."
    cp .env.example .env
    echo "Please edit .env and add your OPENAI_API_KEY, then run this script again."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Build and start containers
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting containers..."
docker-compose up -d

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📌 Frontend: http://localhost:3000"
echo "📌 Backend API: http://localhost:8000"
echo "📌 API Docs: http://localhost:8000/api/docs"
echo ""
echo "📊 Check logs with: docker-compose logs -f"
echo "🛑 Stop services with: docker-compose down"
