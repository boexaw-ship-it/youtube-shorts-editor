#!/bin/bash

# YouTube Shorts AI Editor - Python Setup Script

echo "🎬 YouTube Shorts AI Editor Setup (Python)"
echo "==========================================="
echo ""

# Check Python
echo "📦 Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python found: $PYTHON_VERSION"
else
    echo "❌ Python3 not found!"
    echo "Please install Python3 from: https://www.python.org/"
    exit 1
fi

# Check pip
echo "📦 Checking pip..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    echo "✅ pip found: $PIP_VERSION"
else
    echo "❌ pip not found!"
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
        if command -v apt &> /dev/null; then
            sudo apt update
            sudo apt install -y ffmpeg
        elif command -v yum &> /dev/null; then
            sudo yum install -y ffmpeg
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install ffmpeg
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

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✅ Dependencies installed!"

# Create .env file if not exists
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cat > .env << EOF
PORT=5000
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
echo "  python3 server_python.py"
echo ""
echo "Then open in browser:"
echo "  http://localhost:5000/youtube-shorts-editor.html"
echo ""
echo "Get Gemini API Key:"
echo "  https://aistudio.google.com/app/apikey"
echo ""
echo "=================================="
echo "Happy Video Editing! 🎬✨"
echo "=================================="
