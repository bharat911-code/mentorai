#!/bin/bash
echo "🚀 Starting Yapper RAG Server..."
echo "📊 Environment variables:"
echo "  - PORT: $PORT"
echo "  - HF_TOKEN: ${HF_TOKEN:0:10}..." # Show first 10 chars for security
echo ""

# Start the application
python yapper_server.py 