#!/bin/bash

echo "🦁 Starting CodeLion..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from example..."
    cp env.example .env
    echo "📝 Please update .env with your actual API keys and configuration"
fi

# Start with Docker Compose
echo "🐳 Starting services with Docker Compose..."
docker-compose up -d

echo "✅ CodeLion is starting up!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"

echo ""
echo "📋 Next steps:"
echo "1. Update .env file with your API keys"
echo "2. Visit http://localhost:3000 to access the dashboard"
echo "3. Connect your GitHub repository"
echo "4. Create a pull request to test the agents!"

echo ""
echo "🛑 To stop: docker-compose down"
