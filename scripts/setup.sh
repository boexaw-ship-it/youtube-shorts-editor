#!/bin/bash

# YouTube Shorts AI Editor - Setup Script
# အလိုအလျောက် setup လုပ်ပေးမည့် script

echo "🎬 YouTube Shorts AI Editor Setup"
echo "=================================="
echo ""

# Check if running on Linux/Mac
if [[ "$OSTYPE" != "linux-gnu"* ]] && [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  This script is for Linux/Mac. Windows users please follow manual instructions."
    exit 1
fi

# Check Node.js
echo "📦 Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js found: $NODE_VERSION"
else
    echo "❌ Node.js not found!"
    echo "Please install Node.js from: https://nodejs.org/"
    exit 1
fi

# Check npm
echo "📦 Checking npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✅ npm found: $NPM_VERSION"
else
    echo "❌ npm not found!"
    exit 1
fi

# Check FFmpeg
echo "📦 Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version | head -n1)
    echo "✅ FFmpeg found: $FFMPEG_VERSION"
else
    echo "❌ FFmpeg not found!"
    echo ""
    echo "Installing FFmpeg..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt &> /dev/null; then
            sudo apt update
            sudo apt install -y ffmpeg
        elif command -v yum &> /dev/null; then
            sudo yum install -y ffmpeg
        else
            echo "⚠️  Please install FFmpeg manually"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "⚠️  Please install Homebrew first: https://brew.sh/"
            exit 1
        fi
    fi
    
    echo "✅ FFmpeg installed!"
fi

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p output
touch uploads/.gitkeep
touch output/.gitkeep
echo "✅ Directories created!"

# Install Node.js dependencies
echo ""
echo "📦 Installing Node.js dependencies..."
npm install
echo "✅ Dependencies installed!"

# Create .env file if not exists
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cat > .env << EOF
PORT=3000
# Add your Gemini API Key here (optional)
# GEMINI_API_KEY=your_api_key_here
EOF
    echo "✅ .env file created!"
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "=================================="
echo "🚀 Quick Start Commands:"
echo "=================================="
echo ""
echo "Start the server:"
echo "  npm start"
echo ""
echo "Then open in browser:"
echo "  http://localhost:3000/youtube-shorts-editor.html"
echo ""
echo "Get Gemini API Key:"
echo "  https://aistudio.google.com/app/apikey"
echo ""
echo "=================================="
echo "Happy Video Editing! 🎬✨"
echo "=================================="
