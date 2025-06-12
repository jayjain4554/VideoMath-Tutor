
# 🎥 VideoMath Tutor

**Solve math problems from educational videos using OCR + AI!**

VideoMath Tutor is a smart Chrome Extension + Python backend that captures paused video frames, extracts math expressions using OCR (Pix2Tex or Tesseract), and solves them using Together AI for detailed step-by-step solutions.

---

## 🚀 Features

- ⏸ **Pause any video** to auto-capture math problems
- 🔍 OCR via **Pix2Tex CLI** (preferred) or **Tesseract** fallback
- 🧠 **AI-powered solving** using Together AI (Mixtral / LLaMA)
- 🧾 Render LaTeX in an elegant **KaTeX popup**
- ✂ Copy, 🌐 Search, and ✅ Solve directly from overlay
- 💡 Built-in hint engine for learning context
- 🧲 Toggle extension on/off anytime

---

## ⚙ How It Works

1. User **pauses a video**
2. Content script captures the **video frame**
3. Frame sent to **FastAPI backend** at `/ocr/single`
4. OCR returns LaTeX (Pix2Tex or Tesseract)
5. User sees formatted math + options (solve, copy, hints)
6. On clicking **Solve**, `/solve` sends it to Together AI
7. Solution is cleaned and shown inline 🎯

---


## 🛠 Installation

#### Backend (FastAPI + Together AI)

```bash
# Clone the repo
git clone https://github.com/jayjain4554/VideoMath-Tutor.git
cd VideoMath-Tutor/backend
````

**Create virtual environment**
````markdown
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
````

**Install dependencies**
````markdown
pip install -r requirements.txt
````

**Run server**
````markdown
uvicorn main:app --reload
````

🧠 **Note**:

* Ensure you have `Tesseract` installed and in PATH
* Install [Pix2Tex](https://github.com/lukas-blecher/LaTeX-OCR) CLI for better OCR accuracy
* Add your **Together AI API key** to the environment (`TOGETHER_API_KEY`)

> Server runs at `http://127.0.0.1:8000`

---

### 2️⃣ Chrome Extension

1. Go to `chrome://extensions`
2. Enable **Developer Mode**
3. Click **Load Unpacked**
4. Select the `extension/` folder from this repo

📌 Then click the extension icon and **Activate Extension** from popup

---

## 📂 Project Structure

```
VideoMath-Tutor/
├── backend/
│   ├── main.py              # FastAPI app with OCR + Together AI solve
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # TOGETHER_API_KEY (secure)
│   └── ocr_engine/          # Optional: Pix2Tex local installation
│
├── extension/
│   ├── content.js           # Core script to capture & display results
│   ├── manifest.json        # Chrome extension setup
│   ├── popup.html/.js/.css  # UI to toggle extension
│   └── katex.min.js/.css    # For math rendering
```

---

## 📸 Screenshots

![Screenshot 2025-06-12 133644](https://github.com/user-attachments/assets/af2914fd-442f-4390-a626-d1ef9831fbc3)
![Screenshot 2025-06-12 133657](https://github.com/user-attachments/assets/e88061cf-1090-442d-9b1f-05841203577e)
![Screenshot 2025-06-12 133714](https://github.com/user-attachments/assets/923f3d79-6af2-490b-b551-dda30c5de2b6)
![Screenshot 2025-06-12 133736](https://github.com/user-attachments/assets/4533cd5a-93aa-4ba0-9db3-63fa41a9ff84)
![Screenshot 2025-06-12 133826](https://github.com/user-attachments/assets/8e1a6fdc-1d7c-4c62-9b95-87e2b60f126b)

---

## 🧠 AI Solving Engine

The backend uses the [Together AI Inference API](https://api.together.ai/models) to solve LaTeX equations via models like:

* 🔸 `mistralai/Mixtral-8x7B-Instruct-v0.1` (default)
* ✳️ Easy to upgrade to LLaMA 3 or GPT-NeoX

It returns clean, step-by-step solutions that are parsed into human-readable output using a custom LaTeX cleaner.

---

## 💡 Future Roadmap

* 📢 Add LaTeX-to-speech for accessibility
* 🤖 Plug into Wolfram Alpha API for verified math
* 📈 Build a learning dashboard and insights tracker
* 🔍 Interactive step-by-step explanation viewer

---

## 👨‍💻 Author

Made with ❤️ by **Jay Jain**
Feel free to [contribute, suggest](https://github.com/jayjain4554/VideoMath-Tutor), or reach out for improvements.

> Learn math from videos — smarter than ever. 🧠🎬➕
