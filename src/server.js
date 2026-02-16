// server.js - YouTube Shorts Editor Backend
const express = require('express');
const multer = require('multer');
const ffmpeg = require('fluent-ffmpeg');
const path = require('path');
const fs = require('fs');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// File upload configuration
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadDir = './uploads';
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir, { recursive: true });
        }
        cb(null, uploadDir);
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});

const upload = multer({ 
    storage: storage,
    limits: { fileSize: 500 * 1024 * 1024 } // 500MB limit
});

// Output directory
const outputDir = './output';
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// ============================================
// AI Script Generation Endpoint
// ============================================
app.post('/api/generate-script', async (req, res) => {
    try {
        const { apiKey, topic } = req.body;
        
        if (!apiKey || !topic) {
            return res.status(400).json({ error: 'API Key and topic are required' });
        }

        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({ model: 'gemini-pro' });

        const prompt = `Create a 30-45 second YouTube Shorts script about: ${topic}. 

The script should be:
- In Myanmar (Burmese) language
- Engaging and trendy
- Include a strong hook in the first 3 seconds
- Have clear, conversational narration
- End with a call-to-action
- Keep it simple and easy to follow

Format the script with timing markers like [0-3s], [4-10s], etc.`;

        const result = await model.generateContent(prompt);
        const response = await result.response;
        const text = response.text();

        res.json({ success: true, script: text });
    } catch (error) {
        console.error('Script generation error:', error);
        res.status(500).json({ error: error.message });
    }
});

// ============================================
// Video Upload Endpoint
// ============================================
app.post('/api/upload-video', upload.single('video'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No video file uploaded' });
    }
    
    res.json({
        success: true,
        filename: req.file.filename,
        path: req.file.path,
        size: req.file.size
    });
});

// ============================================
// Audio Upload Endpoint
// ============================================
app.post('/api/upload-audio', upload.single('audio'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No audio file uploaded' });
    }
    
    res.json({
        success: true,
        filename: req.file.filename,
        path: req.file.path
    });
});

// ============================================
// Video Processing Endpoint
// ============================================
app.post('/api/process-video', upload.single('video'), async (req, res) => {
    try {
        const {
            speed = 1,
            mirrorH = false,
            mirrorV = false,
            blur = 0,
            textOverlays = '[]',
            audioFile = null,
            format = 'shorts'
        } = req.body;

        if (!req.file) {
            return res.status(400).json({ error: 'No video file provided' });
        }

        const inputPath = req.file.path;
        const outputFilename = `processed_${Date.now()}.mp4`;
        const outputPath = path.join(outputDir, outputFilename);

        // Parse text overlays
        const overlays = JSON.parse(textOverlays);

        // Create FFmpeg command
        let command = ffmpeg(inputPath);

        // Video filters array
        let videoFilters = [];

        // Speed adjustment
        if (speed !== 1) {
            videoFilters.push(`setpts=${1/speed}*PTS`);
        }

        // Mirror/Flip effects
        if (mirrorH && mirrorV) {
            videoFilters.push('hflip,vflip');
        } else if (mirrorH) {
            videoFilters.push('hflip');
        } else if (mirrorV) {
            videoFilters.push('vflip');
        }

        // Blur effect
        if (blur > 0) {
            videoFilters.push(`boxblur=${blur}:${blur}`);
        }

        // Scale to YouTube Shorts/TikTok format (9:16 aspect ratio)
        if (format === 'shorts' || format === 'tiktok') {
            videoFilters.push('scale=1080:1920:force_original_aspect_ratio=decrease');
            videoFilters.push('pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black');
        }

        // Add text overlays using drawtext filter
        overlays.forEach((overlay, index) => {
            const startTime = overlay.time;
            const duration = 5; // Show text for 5 seconds
            
            videoFilters.push(
                `drawtext=text='${overlay.text.replace(/'/g, "\\'")}':` +
                `fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:` +
                `fontsize=48:fontcolor=white:` +
                `x=(w-text_w)/2:y=(h-text_h)/2:` +
                `borderw=3:bordercolor=black:` +
                `enable='between(t,${startTime},${startTime + duration})'`
            );
        });

        // Apply video filters
        if (videoFilters.length > 0) {
            command = command.videoFilters(videoFilters);
        }

        // Add background audio if provided
        if (audioFile && fs.existsSync(audioFile)) {
            command = command.input(audioFile);
            command = command.complexFilter([
                '[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2[a]'
            ]);
            command = command.outputOptions(['-map', '0:v', '-map', '[a]']);
        }

        // Output settings
        command
            .outputOptions([
                '-c:v libx264',
                '-preset fast',
                '-crf 23',
                '-c:a aac',
                '-b:a 128k',
                '-movflags +faststart'
            ])
            .output(outputPath)
            .on('start', (commandLine) => {
                console.log('FFmpeg command:', commandLine);
            })
            .on('progress', (progress) => {
                console.log('Processing: ' + progress.percent + '% done');
            })
            .on('end', () => {
                console.log('Video processing complete!');
                res.json({
                    success: true,
                    outputFile: outputFilename,
                    downloadUrl: `/download/${outputFilename}`
                });
            })
            .on('error', (err) => {
                console.error('FFmpeg error:', err);
                res.status(500).json({ error: err.message });
            })
            .run();

    } catch (error) {
        console.error('Processing error:', error);
        res.status(500).json({ error: error.message });
    }
});

// ============================================
// Text-to-Speech Endpoint (using Google TTS)
// ============================================
app.post('/api/text-to-speech', async (req, res) => {
    try {
        const { text, apiKey } = req.body;
        
        if (!text) {
            return res.status(400).json({ error: 'Text is required' });
        }

        // Using Google Cloud Text-to-Speech API
        const textToSpeech = require('@google-cloud/text-to-speech');
        const client = new textToSpeech.TextToSpeechClient({
            apiKey: apiKey
        });

        const request = {
            input: { text: text },
            voice: { 
                languageCode: 'my-MM',
                ssmlGender: 'NEUTRAL'
            },
            audioConfig: { 
                audioEncoding: 'MP3',
                speakingRate: 1.0,
                pitch: 0.0
            }
        };

        const [response] = await client.synthesizeSpeech(request);
        const audioFilename = `voice_${Date.now()}.mp3`;
        const audioPath = path.join(outputDir, audioFilename);
        
        fs.writeFileSync(audioPath, response.audioContent, 'binary');

        res.json({
            success: true,
            audioFile: audioFilename,
            downloadUrl: `/download/${audioFilename}`
        });
    } catch (error) {
        console.error('TTS error:', error);
        // Fallback: Return error but suggest browser-based TTS
        res.json({
            success: false,
            error: error.message,
            suggestion: 'Use browser Web Speech API for TTS'
        });
    }
});

// ============================================
// Download Endpoint
// ============================================
app.get('/download/:filename', (req, res) => {
    const filename = req.params.filename;
    const filePath = path.join(outputDir, filename);
    
    if (fs.existsSync(filePath)) {
        res.download(filePath);
    } else {
        res.status(404).json({ error: 'File not found' });
    }
});

// ============================================
// Clean up old files periodically
// ============================================
setInterval(() => {
    const maxAge = 24 * 60 * 60 * 1000; // 24 hours
    const now = Date.now();

    [outputDir, './uploads'].forEach(dir => {
        if (fs.existsSync(dir)) {
            fs.readdirSync(dir).forEach(file => {
                const filePath = path.join(dir, file);
                const stats = fs.statSync(filePath);
                
                if (now - stats.mtimeMs > maxAge) {
                    fs.unlinkSync(filePath);
                    console.log(`Deleted old file: ${file}`);
                }
            });
        }
    });
}, 60 * 60 * 1000); // Run every hour

// ============================================
// Start Server
// ============================================
app.listen(PORT, () => {
    console.log(`🚀 YouTube Shorts Editor Server running on port ${PORT}`);
    console.log(`📹 Upload endpoint: http://localhost:${PORT}/api/upload-video`);
    console.log(`🎬 Process endpoint: http://localhost:${PORT}/api/process-video`);
    console.log(`🤖 Script generation: http://localhost:${PORT}/api/generate-script`);
});

module.exports = app;
