# VideoMath Tutor

**Solve math problems from educational videos using OCR + AI!**

VideoMath Tutor is a smart Chrome Extension + Python backend tool that captures paused video frames, extracts math expressions using OCR (Tesseract + Pix2Tex), and solves them using symbolic math or GPT assistance.

---

## Features

* ✅ **Pause any video** to extract visible math problems
* 🔍 **OCR extraction** with Pix2Tex & Tesseract
* 📐 **Solve equations** using SymPy, with GPT fallback
* 📋 **Copy LaTeX**, 🧠 AI-generated hints
* 🧾 **Render equations** in KaTeX overlay
* 🧠 Built-in hint engine for basic strategies
* 🌐 **Search on Web** button for quick lookups
* 🧲 Deactivate/Reactivate toggle built-in

---

## How It Works

1. **User pauses** a video on any page
2. **Content script** captures the frame
3. Image is sent to **FastAPI OCR backend**
4. OCR runs via Pix2Tex/Tesseract → returns LaTeX
5. Result is shown in a popup + option to solve, search, hint

---

## Installation

### Backend (FastAPI server)

```bash
# Clone the repo
git clone https://github.com/jayjain4554/VideoMath-Tutor.git
cd VideoMath-Tutor/backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload
```

> Backend runs at `http://127.0.0.1:8000`

Make sure Tesseract is installed and accessible in PATH. For best results, also install and set up [Pix2Tex](https://github.com/lukas-blecher/LaTeX-OCR).

### Chrome Extension

1. Go to `chrome://extensions`
2. Enable **Developer Mode**
3. Click **Load Unpacked**
4. Select the `/extension` folder from this repo

Click the extension icon → **Activate Extension**

---

## Project Structure

```
VideoMath-Tutor/
├── backend/
│   ├── main.py              # FastAPI OCR and solver logic
│   ├── requirements.txt     # Python dependencies
│   └── ocr_engine/          # Pix2Tex repo if installed locally
│
├── extension/
│   ├── content.js           # OCR & solver logic in browser
│   ├── popup.html/.js/.css  # UI to trigger script injection
│   ├── manifest.json        # Chrome extension config
│   └── katex.min.js/css     # Math rendering
```

---

## Screenshots

![Screenshot 2025-06-11 143540](https://github.com/user-attachments/assets/3453737e-c0ed-40a3-a422-4d48dc010834)
![Screenshot 2025-06-11 143609](https://github.com/user-attachments/assets/b215ad5c-5a42-4d7f-9ad2-ca0366066f66)
![Screenshot 2025-06-11 143635](https://github.com/user-attachments/assets/b38afba9-b671-479b-bd76-b0ad785998dd)
![Screenshot 2025-06-11 144139](https://github.com/user-attachments/assets/5b2a3562-d141-4e01-87e1-e898376ade67)


---

## Future Ideas

* ✅ LaTeX-to-speech for accessibility
* 🤝 Integration with Wolfram Alpha API
* 📊 Usage analytics and improvement tracking
* 🎯 Interactive steps view for solution breakdown


---

## Author

Made by **Jay Jain** — feel free to reach out via GitHub for contributions, ideas, or feedback!

> Enjoy learning math from video like never before. 🎥➕🧠
