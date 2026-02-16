# 🚀 Quick Start Guide (မြန်မာဘာသာ)

## 📋 အကျဉ်းချုပ်

YouTube Shorts Video Editor သည် AI-powered web application တစ်ခုဖြစ်ပြီး အောက်ပါတို့ကို လုပ်ဆောင်နိုင်သည်:

✅ Gemini AI သုံးပြီး script အလိုအလျောက်ရေးခြင်း
✅ Video upload နှင့် editing
✅ Speed, Mirror, Flip, Blur effects
✅ စာတန်းထိုး (Text overlays)
✅ Background music ထည့်ခြင်း
✅ Text-to-Speech (Script to voice)

## 🎯 Option 1: Node.js Backend (အကြံပြုချက်)

### Installation

```bash
# 1. FFmpeg install လုပ်ပါ (video processing အတွက်)
# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg

# macOS:
brew install ffmpeg

# 2. Dependencies install လုပ်ပါ
npm install

# 3. Server start လုပ်ပါ
npm start
```

### အသုံးပြုခြင်း

1. Browser ဖွင့်ပြီး `http://localhost:3000/youtube-shorts-editor.html` သွားပါ
2. Gemini API Key ထည့်ပါ (https://aistudio.google.com/app/apikey)
3. Video topic ရိုက်ပြီး script generate လုပ်ပါ
4. Video upload လုပ်ပါ
5. Effects များ apply လုပ်ပါ
6. Export လုပ်ပါ!

## 🎯 Option 2: Python Backend

### Installation

```bash
# 1. FFmpeg install လုပ်ပါ
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # macOS

# 2. Python dependencies install လုပ်ပါ
pip install -r requirements.txt

# 3. Server start လုပ်ပါ
python server_python.py
```

### အသုံးပြုခြင်း

1. Browser ဖွင့်ပြီး `http://localhost:5000/youtube-shorts-editor.html` သွားပါ
2. Frontend file ကို Python server path မှာ copy လုပ်ပါ
3. Node.js version နဲ့ အတူတူပဲ အသုံးပြုနိုင်ပါသည်

## 🔑 Gemini API Key ရယူခြင်း

1. **သွားရန်**: https://aistudio.google.com/app/apikey
2. **Google Account** နှင့် sign in လုပ်ပါ
3. **"Create API Key"** button ကို နှိပ်ပါ
4. API key ကို copy လုပ်ပြီး သိမ်းထားပါ (AIzaSy... နဲ့ စတာ)
5. Frontend မှာ paste လုပ်ပါ

## 📹 Video Upload နှင့် Editing

### Step-by-Step:

**1. Video Upload**
- Click "📁 Video ရွေးမယ်"
- MP4, MOV, သို့မဟုတ် AVI file ရွေးပါ
- Preview မှာ video ပေါ်လာပါမယ်

**2. Speed Control ⚡**
```
0.5x = Slow motion
1.0x = Normal speed
2.0x = Fast forward
```

**3. Mirror & Flip 🔄**
- "↔️ Mirror" = ဘယ်ညာပြောင်းပြန်
- "↕️ Flip" = အပေါ်အောက်ပြောင်းပြန်

**4. Blur Effect ✨**
- 0px = No blur
- 20px = Maximum blur

**5. Text Overlay 💬**
```
Step 1: စာရိုက်ပါ
Step 2: အချိန် (seconds) ထည့်ပါ
Step 3: "➕ Add" နှိပ်ပါ
```

**6. Background Music 🎵**
- "🎵 Audio ရွေးမယ်" နှိပ်ပါ
- MP3 သို့မဟုတ် WAV file ရွေးပါ

**7. Export 📤**
- Format ရွေးပါ (YouTube Shorts / TikTok)
- "🎥 Video Export လုပ်မယ်" နှိပ်ပါ
- Processing ပြီးရင် download လုပ်ပါ

## 💡 Tips & Tricks

### Script Generation Tips:
- တိကျသော topic ပေးပါ (ဥပမာ: "How to edit videos fast")
- Myanmar language မှာ ရေးချင်ရင် "in Myanmar language" ထည့်ပြောပါ
- 30-45 seconds အတွက် optimize ထားပါသည်

### Video Editing Tips:
- Short videos (< 1 minute) က processing မြန်ပါသည်
- Text overlay များကို အချိန်တိကျ ထည့်ပါ
- Speed effect များက content အပေါ် မူတည်ပြီး သုံးပါ
- Background music သည် video length နှင့် ကိုက်ညီရပါမည်

### Performance Tips:
- Video resolution ကြီးလွန်းရင် processing အချိန်ကြာပါသည်
- 1080p သို့မဟုတ် 720p သုံးပါ
- File size 100MB အောက်ဖြစ်ရင် မြန်ပါသည်

## ⚠️ Common Issues

### Issue 1: FFmpeg not found
```bash
# Solution:
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # macOS
```

### Issue 2: API Key Invalid
- API Key မှန်ကန်မှု စစ်ဆေးပါ
- Spaces များ မပါသင့်ပါ
- Quota limit ကျော်လွန်ခြင်း ရှိ/မရှိ စစ်ပါ

### Issue 3: Video Processing Slow
- Video size လျှော့ပါ
- Resolution လျှော့ပါ (720p)
- Server resources စစ်ဆေးပါ

### Issue 4: Text-to-Speech Not Working
- Browser မှာ Web Speech API support ရှိ/မရှိ စစ်ပါ
- Chrome သို့မဟုတ် Edge browser သုံးပါ
- Myanmar language voice install ထားရပါမယ်

## 📱 Mobile Usage

Mobile devices များတွင် အသုံးပြုနိုင်သော်လည်း:
- Large files များ upload လုပ်ရန် ခက်ခဲနိုင်သည်
- Processing time ပိုကြာနိုင်သည်
- Desktop browser အသုံးပြုရန် အကြံပြုအပ်ပါသည်

## 🔧 Advanced Usage

### Custom Text Styling
Frontend HTML မှာ text style များကို customize လုပ်နိုင်ပါသည်:

```javascript
// Example: Change text color
fontcolor='yellow'  // instead of 'white'
fontsize=60         // bigger text
```

### Multiple Audio Tracks
Backend မှာ multiple audio files mix လုပ်နိုင်ပါသည်

### Batch Processing
Multiple videos တစ်ခါတည်း process လုပ်ရန် script ရေးနိုင်ပါသည်

## 🎓 Learning Resources

### Video Editing:
- FFmpeg Documentation: https://ffmpeg.org/documentation.html
- MoviePy Guide: https://zulko.github.io/moviepy/

### AI Integration:
- Gemini AI Docs: https://ai.google.dev/docs
- Google Cloud TTS: https://cloud.google.com/text-to-speech

### Web Development:
- Express.js: https://expressjs.com/
- Flask: https://flask.palletsprojects.com/

## 📞 လိုအပ်ချက်များ

### Node.js Version:
- FFmpeg
- Express.js server
- Port 3000

### Python Version:
- FFmpeg
- Flask server
- Port 5000

## ✅ Checklist

တပ်ဆင်ပြီးပြီလား?
- [ ] FFmpeg installed?
- [ ] Dependencies installed? (`npm install` or `pip install`)
- [ ] Server running? (`npm start` or `python server_python.py`)
- [ ] Gemini API Key ready?
- [ ] Browser opened? (http://localhost:3000 or 5000)

Video ရိုက်ပြီးပြီလား?
- [ ] Video uploaded?
- [ ] Script generated?
- [ ] Effects applied?
- [ ] Text overlays added?
- [ ] Background music added?
- [ ] Ready to export?

## 🎉 Ready to Create!

အားလုံး setup ပြီးသွားပြီဆိုရင် YouTube Shorts videos များ ဖန်တီးနိုင်ပါပြီ! 🎬✨

သင့်ရဲ့ ပထမဆုံး AI-powered video ကို create လုပ်ကြည့်ပါ!

---

**Questions or Issues?**
- README.md ဖတ်ပါ (detailed documentation)
- GitHub Issues မှာ မေးပါ
- Console logs များကို စစ်ဆေးပါ

**Happy Video Editing! 🎥🚀**
