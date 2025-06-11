// 📹 Content script for VideoMath Tutor
console.log('📹 Content script running...');

let ocrActive = true;

function captureFrame(video) {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth * 2;
  canvas.height = video.videoHeight * 2;
  const ctx = canvas.getContext('2d');
  ctx.scale(2, 2);
  ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
  preprocessCanvas(canvas);
  return canvas.toDataURL('image/png');
}

function preprocessCanvas(canvas) {
  const ctx = canvas.getContext('2d');
  const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const data = imgData.data;
  for (let i = 0; i < data.length; i += 4) {
    const gray = 0.3 * data[i] + 0.59 * data[i+1] + 0.11 * data[i+2];
    const value = gray > 140 ? 255 : 0;
    data[i] = data[i+1] = data[i+2] = value;
  }
  ctx.putImageData(imgData, 0, 0);
}

function convertDataUrlToFormData(dataUrl) {
  const byteString = atob(dataUrl.split(',')[1]);
  const mime = dataUrl.split(',')[0].split(':')[1].split(';')[0];
  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  for (let i = 0; i < byteString.length; i++) ia[i] = byteString.charCodeAt(i);
  const blob = new Blob([ab], { type: mime });
  const formData = new FormData();
  formData.append("file", blob, "frame.png");
  return formData;
}

function showOverlay(latex, hints = [], solution = null) {
  const old = document.getElementById('videomath-tutor-overlay');
  if (old) old.remove();

  const overlay = document.createElement('div');
  overlay.id = 'videomath-tutor-overlay';
  overlay.style.cssText = `
    position: fixed; top: 20px; right: 20px;
    background: #fff; border: 1px solid #ccc;
    padding: 16px; border-radius: 10px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.25);
    font-family: sans-serif; font-size: 14px;
    z-index: 9999; max-width: 400px;
  `;

  const title = document.createElement('div');
  title.innerText = '📘 Math OCR Result';
  title.style.fontWeight = 'bold';
  title.style.marginBottom = '12px';

  const closeBtn = document.createElement('span');
  closeBtn.innerText = '✖';
  closeBtn.style.cssText = 'position: absolute; top: 10px; right: 15px; cursor: pointer; font-size: 16px;';
  closeBtn.onclick = () => overlay.remove();

  const mathBlock = document.createElement('div');
  mathBlock.style.marginBottom = '10px';
  try {
    katex.render(latex, mathBlock, { throwOnError: false });
  } catch (e) {
    mathBlock.innerText = latex;
  }

  const buttons = document.createElement('div');
  buttons.style.marginTop = '10px';

  const copyBtn = document.createElement('button');
  copyBtn.textContent = '📋 Copy';
  copyBtn.onclick = () => navigator.clipboard.writeText(latex);

  const searchBtn = document.createElement('button');
  searchBtn.textContent = '🔍 Web Search';
  searchBtn.onclick = () => window.open(`https://www.google.com/search?q=${encodeURIComponent(latex)}`);

  const solveBtn = document.createElement('button');
  solveBtn.textContent = '✅ Solve';
  solveBtn.onclick = async () => {
    const res = await fetch('http://127.0.0.1:8000/solve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ expression: latex })
    });
    const data = await res.json();
    alert(`✅ Solution:\n${data.solution}\n\n🧠 Explanation:\n${data.steps}${data.gpt_fallback ? '\n\n🤖 GPT Help:\n' + data.gpt_fallback : ''}`);
  };

  const toggleBtn = document.createElement('button');
  toggleBtn.textContent = ocrActive ? '🛑 Deactivate' : '▶️ Activate';
  toggleBtn.onclick = () => {
    ocrActive = !ocrActive;
    toggleBtn.textContent = ocrActive ? '🛑 Deactivate' : '▶️ Activate';
  };

  [copyBtn, searchBtn, solveBtn, toggleBtn].forEach(btn => {
    btn.style.marginRight = '8px';
    btn.style.padding = '6px 10px';
    btn.style.borderRadius = '4px';
    btn.style.border = 'none';
    btn.style.cursor = 'pointer';
    btn.style.background = '#444';
    btn.style.color = 'white';
    btn.style.marginTop = '8px';
  });

  buttons.append(copyBtn, searchBtn, solveBtn, toggleBtn);

  const hintBlock = document.createElement('div');
  hintBlock.style.marginTop = '10px';
  if (hints.length > 0) {
    const hintTitle = document.createElement('strong');
    hintTitle.innerText = '💡 Hints:';
    hintBlock.appendChild(hintTitle);
    const list = document.createElement('ul');
    hints.forEach(h => {
      const li = document.createElement('li');
      li.innerText = h;
      list.appendChild(li);
    });
    hintBlock.appendChild(list);
  }

  overlay.append(closeBtn, title, mathBlock, buttons, hintBlock);
  document.body.appendChild(overlay);
}

function runOCR(imageDataUrl) {
  fetch('http://127.0.0.1:8000/ocr/single', {
    method: 'POST',
    body: convertDataUrlToFormData(imageDataUrl)
  })
    .then(res => res.json())
    .then(data => {
      console.log('[🧠 OCR Result]', data);
      const raw = (data?.best_result?.result || '').replace(/.*\.png[:\uff1a]\s*/gi, '').trim();
      const hints = generateHints(raw);
      showOverlay(raw, hints);
    })
    .catch(err => {
      console.error('[❌ OCR Error]', err);
      alert('⚠️ Failed to fetch OCR result. Ensure backend is running.');
    });
}

function generateHints(expr) {
  const hints = [];
  if (expr.includes('|')) hints.push("This looks like an absolute value equation. Consider splitting into cases.");
  if (expr.includes('lim')) hints.push("You might need L'Hôpital's Rule if you get 0/0.");
  if (expr.includes('tan') || expr.includes('sin') || expr.includes('cos')) hints.push("Use trigonometric identities.");
  if (expr.includes('x^2') || expr.includes('x**2')) hints.push("Looks quadratic — factor or use the quadratic formula.");
  if (expr.includes('=')) hints.push("Try isolating the variable.");
  return hints;
}

function setupVideoListeners() {
  const videos = document.querySelectorAll('video');
  videos.forEach(video => {
    if (!video.dataset.listenerAttached) {
      video.addEventListener('pause', () => {
        if (!ocrActive) return;
        console.log('⏸️ Video paused — capturing...');
        const frame = captureFrame(video);
        runOCR(frame);
      });
      video.dataset.listenerAttached = 'true';
    }
  });
}

setupVideoListeners();
