// console.log('📹 Content script running...');

// // 1. Capture video frame
// function captureFrame(video) {
//   const canvas = document.createElement('canvas');
//   canvas.width = video.videoWidth * 2;
//   canvas.height = video.videoHeight * 2;
//   const ctx = canvas.getContext('2d');
//   ctx.scale(2, 2);
//   ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
//   preprocessCanvas(canvas);
//   return canvas.toDataURL('image/png');
// }

// // 2. Preprocess for OCR
// function preprocessCanvas(canvas) {
//   const ctx = canvas.getContext('2d');
//   const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
//   const data = imageData.data;
//   for (let i = 0; i < data.length; i += 4) {
//     const gray = 0.299 * data[i] + 0.587 * data[i+1] + 0.114 * data[i+2];
//     const contrast = gray > 140 ? 255 : 0;
//     data[i] = data[i+1] = data[i+2] = contrast;
//   }
//   ctx.putImageData(imageData, 0, 0);
// }

// // 3. Convert image to FormData
// function convertDataUrlToFormData(dataUrl) {
//   const byteString = atob(dataUrl.split(',')[1]);
//   const mimeString = dataUrl.split(',')[0].split(':')[1].split(';')[0];
//   const ab = new ArrayBuffer(byteString.length);
//   const ia = new Uint8Array(ab);
//   for (let i = 0; i < byteString.length; i++) {
//     ia[i] = byteString.charCodeAt(i);
//   }
//   const blob = new Blob([ab], { type: mimeString });
//   const formData = new FormData();
//   formData.append("file", blob, "frame.png");
//   return formData;
// }

// // 4. Show LaTeX overlay
// function showMathOverlay(latex) {
//   const old = document.getElementById('videomath-tutor-overlay');
//   if (old) old.remove();

//   const overlay = document.createElement('div');
//   overlay.id = 'videomath-tutor-overlay';
//   overlay.style.cssText = `
//     position: fixed;
//     top: 20px;
//     right: 20px;
//     background: white;
//     color: black;
//     padding: 16px 18px;
//     border-radius: 10px;
//     box-shadow: 0 6px 18px rgba(0,0,0,0.25);
//     z-index: 9999;
//     max-width: 440px;
//     font-family: sans-serif;
//   `;

//   // Header with title and close button
//   const header = document.createElement('div');
//   header.style.display = 'flex';
//   header.style.justifyContent = 'space-between';
//   header.style.alignItems = 'center';

//   const title = document.createElement('div');
//   title.innerText = '📘 Math OCR Result';
//   title.style.fontWeight = 'bold';

//   const closeBtn = document.createElement('button');
//   closeBtn.innerText = '✖';
//   closeBtn.style.cssText = `
//     background: none;
//     border: none;
//     font-size: 16px;
//     cursor: pointer;
//     color: #888;
//   `;
//   closeBtn.onclick = () => overlay.remove();

//   header.appendChild(title);
//   header.appendChild(closeBtn);

//   const mathBlock = document.createElement('div');
//   mathBlock.id = 'math-render';
//   mathBlock.style.marginTop = '10px';

//   try {
//     katex.render(latex, mathBlock, { throwOnError: false });
//   } catch (e) {
//     mathBlock.innerText = latex;
//   }

//   const raw = document.createElement('pre');
//   raw.innerText = latex;
//   raw.style.fontSize = '12px';
//   raw.style.marginTop = '10px';
//   raw.style.whiteSpace = 'pre-wrap';

//   const btn = document.createElement('button');
//   btn.innerText = '📋 Copy LaTeX';
//   btn.style.cssText = `
//     margin-top: 12px;
//     padding: 6px 10px;
//     background: #4CAF50;
//     color: white;
//     border: none;
//     border-radius: 5px;
//     cursor: pointer;
//   `;
//   btn.onclick = () => {
//     navigator.clipboard.writeText(latex);
//     btn.innerText = "✅ Copied!";
//     setTimeout(() => btn.innerText = "📋 Copy LaTeX", 1500);
//   };

//   overlay.appendChild(header);
//   overlay.appendChild(mathBlock);
//   overlay.appendChild(btn);
//   overlay.appendChild(raw);
//   document.body.appendChild(overlay);
// }

// // 5. Run OCR
// function runOCR(imageDataUrl) {
//   fetch('http://127.0.0.1:8000/ocr/single', {
//     method: 'POST',
//     body: convertDataUrlToFormData(imageDataUrl)
//   })
//     .then(res => res.json())
//     .then(data => {
//       console.log('[🧠 OCR Result]', data);
//       const latex = (data?.best_result?.result || '')
//         .replace(/.*\.png[:：]\s*/gi, '') // Remove image path
//         .replace(/\\(left|right|quad|qquad)/g, '') // Strip formatting macros
//         .trim() || 'No readable LaTeX detected';
//       showMathOverlay(latex);
//     })
//     .catch(err => {
//       console.error('[❌ OCR Error]', err);
//       alert('⚠️ Failed to fetch OCR result. Make sure backend is running.');
//     });
// }

// // 6. Setup listeners
// function setupVideoListeners() {
//   const videos = document.querySelectorAll('video');
//   videos.forEach(video => {
//     video.addEventListener('pause', () => {
//       console.log('⏸️ Video paused — capturing...');
//       const frame = captureFrame(video);
//       runOCR(frame);
//     });
//   });
// }

// setupVideoListeners();

// console.log('📹 Enhanced Math OCR Content Script...');

// // 1. Enhanced video frame capture with better preprocessing
// function captureFrame(video) {
//   const canvas = document.createElement('canvas');
  
//   // Use higher resolution for better OCR
//   const scale = 3; // Increased from 2
//   canvas.width = video.videoWidth * scale;
//   canvas.height = video.videoHeight * scale;
  
//   const ctx = canvas.getContext('2d');
//   ctx.scale(scale, scale);
  
//   // Better image smoothing
//   ctx.imageSmoothingEnabled = true;
//   ctx.imageSmoothingQuality = 'high';
  
//   ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
  
//   // Enhanced preprocessing
//   enhancedPreprocessCanvas(canvas);
  
//   return canvas.toDataURL('image/png');
// }

// // 2. Enhanced preprocessing with multiple techniques
// function enhancedPreprocessCanvas(canvas) {
//   const ctx = canvas.getContext('2d');
//   const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
//   const data = imageData.data;
  
//   // Step 1: Convert to grayscale with better weights for math content
//   for (let i = 0; i < data.length; i += 4) {
//     const gray = 0.299 * data[i] + 0.587 * data[i+1] + 0.114 * data[i+2];
//     data[i] = data[i+1] = data[i+2] = gray;
//   }
  
//   // Step 2: Apply Gaussian blur to reduce noise
//   ctx.putImageData(imageData, 0, 0);
//   ctx.filter = 'blur(0.5px)';
//   ctx.drawImage(canvas, 0, 0);
//   ctx.filter = 'none';
  
//   // Step 3: Enhanced contrast and thresholding
//   const newImageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
//   const newData = newImageData.data;
  
//   for (let i = 0; i < newData.length; i += 4) {
//     const gray = newData[i];
    
//     // Adaptive thresholding based on local neighborhood
//     let threshold = 128;
    
//     // Simple local area check (you could make this more sophisticated)
//     const x = (i / 4) % canvas.width;
//     const y = Math.floor((i / 4) / canvas.width);
    
//     if (x > 10 && x < canvas.width - 10 && y > 10 && y < canvas.height - 10) {
//       // Sample surrounding pixels for local threshold
//       let sum = 0, count = 0;
//       for (let dx = -5; dx <= 5; dx += 2) {
//         for (let dy = -5; dy <= 5; dy += 2) {
//           const idx = ((y + dy) * canvas.width + (x + dx)) * 4;
//           if (idx >= 0 && idx < newData.length) {
//             sum += newData[idx];
//             count++;
//           }
//         }
//       }
//       threshold = count > 0 ? sum / count : 128;
//     }
    
//     // Apply threshold with some tolerance
//     const contrast = gray > threshold - 20 ? 255 : 0;
//     newData[i] = newData[i+1] = newData[i+2] = contrast;
//   }
  
//   ctx.putImageData(newImageData, 0, 0);
// }

// // 3. Enhanced LaTeX cleaning and formatting
// function cleanLaTeX(rawLatex) {
//   if (!rawLatex || typeof rawLatex !== 'string') {
//     return 'No readable LaTeX detected';
//   }
  
//   let cleaned = rawLatex
//     // Remove image path references
//     .replace(/.*\.png[:：]\s*/gi, '')
//     // Remove display style commands that cause issues
//     .replace(/\\displaystyle/g, '')
//     // Remove problematic spacing commands
//     .replace(/\\(left|right)\s*/g, '')
//     .replace(/\\(quad|qquad)/g, ' ')
//     // Clean up array environments that are too complex
//     .replace(/\\begin\{array\}.*?\\end\{array\}/gs, (match) => {
//       // Try to extract just the math content from arrays
//       const content = match.replace(/\\begin\{array\}[^}]*\}/g, '')
//                           .replace(/\\end\{array\}/g, '')
//                           .replace(/\\\\/g, ', ')
//                           .replace(/&/g, '');
//       return content;
//     })
//     // Fix common fraction issues
//     .replace(/\\frac\s*\{\s*([^}]+)\s*\}\s*\{\s*([^}]+)\s*\}/g, '\\frac{$1}{$2}')
//     // Remove excessive braces
//     .replace(/\{\{([^}]+)\}\}/g, '{$1}')
//     // Clean up operators
//     .replace(/\\operatorname\{([^}]+)\}/g, '\\text{$1}')
//     // Fix spacing
//     .replace(/\s+/g, ' ')
//     .trim();
  
//   // If cleaning resulted in empty string, return fallback
//   if (!cleaned || cleaned.length < 3) {
//     return 'No readable LaTeX detected';
//   }
  
//   return cleaned;
// }

// // 4. Enhanced overlay with better rendering and error handling
// function showMathOverlay(latex) {
//   const old = document.getElementById('videomath-tutor-overlay');
//   if (old) old.remove();

//   const overlay = document.createElement('div');
//   overlay.id = 'videomath-tutor-overlay';
//   overlay.style.cssText = `
//     position: fixed;
//     top: 20px;
//     right: 20px;
//     background: rgba(255, 255, 255, 0.98);
//     color: #333;
//     padding: 20px;
//     border-radius: 12px;
//     box-shadow: 0 8px 32px rgba(0,0,0,0.15);
//     z-index: 10000;
//     max-width: 500px;
//     font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
//     border: 1px solid rgba(0,0,0,0.1);
//     backdrop-filter: blur(10px);
//   `;

//   // Header
//   const header = document.createElement('div');
//   header.style.cssText = `
//     display: flex;
//     justify-content: space-between;
//     align-items: center;
//     margin-bottom: 15px;
//     padding-bottom: 10px;
//     border-bottom: 1px solid #eee;
//   `;

//   const title = document.createElement('div');
//   title.innerHTML = '🔢 <strong>Math OCR Result</strong>';
//   title.style.fontSize = '16px';

//   const closeBtn = document.createElement('button');
//   closeBtn.innerHTML = '×';
//   closeBtn.style.cssText = `
//     background: none;
//     border: none;
//     font-size: 20px;
//     cursor: pointer;
//     color: #999;
//     padding: 0;
//     width: 24px;
//     height: 24px;
//     border-radius: 50%;
//     display: flex;
//     align-items: center;
//     justify-content: center;
//   `;
//   closeBtn.onclick = () => overlay.remove();
//   closeBtn.onmouseover = () => closeBtn.style.background = '#f0f0f0';
//   closeBtn.onmouseout = () => closeBtn.style.background = 'none';

//   header.appendChild(title);
//   header.appendChild(closeBtn);

//   // Math rendering area
//   const mathBlock = document.createElement('div');
//   mathBlock.id = 'math-render';
//   mathBlock.style.cssText = `
//     margin: 15px 0;
//     padding: 15px;
//     background: #f8f9fa;
//     border-radius: 8px;
//     border: 1px solid #e9ecef;
//     min-height: 40px;
//     display: flex;
//     align-items: center;
//     justify-content: center;
//     font-size: 18px;
//   `;

//   // Try to render with KaTeX
//   let renderSuccess = false;
//   if (typeof katex !== 'undefined') {
//     try {
//       katex.render(latex, mathBlock, { 
//         throwOnError: false,
//         displayMode: false,
//         strict: false,
//         trust: true,
//         macros: {
//           "\\f": "#1f(#2)"
//         }
//       });
//       renderSuccess = true;
//     } catch (e) {
//       console.warn('KaTeX rendering failed:', e);
//     }
//   }
  
//   // Fallback rendering
//   if (!renderSuccess) {
//     mathBlock.innerHTML = `<code style="background: #fff; padding: 8px; border-radius: 4px; font-family: 'Courier New', monospace;">${latex}</code>`;
//   }

//   // Raw LaTeX display (collapsible)
//   const rawSection = document.createElement('details');
//   rawSection.style.marginTop = '15px';
  
//   const summary = document.createElement('summary');
//   summary.innerHTML = '📝 Raw LaTeX';
//   summary.style.cssText = `
//     cursor: pointer;
//     font-weight: 500;
//     margin-bottom: 10px;
//     color: #555;
//   `;
  
//   const raw = document.createElement('pre');
//   raw.textContent = latex;
//   raw.style.cssText = `
//     font-size: 12px;
//     background: #f1f3f4;
//     padding: 10px;
//     border-radius: 6px;
//     white-space: pre-wrap;
//     word-break: break-all;
//     margin: 0;
//     font-family: 'Courier New', monospace;
//     border: 1px solid #dadce0;
//   `;

//   rawSection.appendChild(summary);
//   rawSection.appendChild(raw);

//   // Action buttons
//   const buttonContainer = document.createElement('div');
//   buttonContainer.style.cssText = `
//     display: flex;
//     gap: 10px;
//     margin-top: 15px;
//   `;

//   const copyBtn = document.createElement('button');
//   copyBtn.innerHTML = '📋 Copy LaTeX';
//   copyBtn.style.cssText = `
//     flex: 1;
//     padding: 10px;
//     background: #1976d2;
//     color: white;
//     border: none;
//     border-radius: 6px;
//     cursor: pointer;
//     font-weight: 500;
//     transition: background 0.2s;
//   `;
//   copyBtn.onmouseover = () => copyBtn.style.background = '#1565c0';
//   copyBtn.onmouseout = () => copyBtn.style.background = '#1976d2';
//   copyBtn.onclick = async () => {
//     try {
//       await navigator.clipboard.writeText(latex);
//       copyBtn.innerHTML = "✅ Copied!";
//       copyBtn.style.background = "#4caf50";
//       setTimeout(() => {
//         copyBtn.innerHTML = "📋 Copy LaTeX";
//         copyBtn.style.background = "#1976d2";
//       }, 2000);
//     } catch (err) {
//       console.error('Copy failed:', err);
//       copyBtn.innerHTML = "❌ Copy failed";
//       copyBtn.style.background = "#f44336";
//       setTimeout(() => {
//         copyBtn.innerHTML = "📋 Copy LaTeX";
//         copyBtn.style.background = "#1976d2";
//       }, 2000);
//     }
//   };

//   const retryBtn = document.createElement('button');
//   retryBtn.innerHTML = '🔄 Retry OCR';
//   retryBtn.style.cssText = `
//     padding: 10px 15px;
//     background: #757575;
//     color: white;
//     border: none;
//     border-radius: 6px;
//     cursor: pointer;
//     font-weight: 500;
//     transition: background 0.2s;
//   `;
//   retryBtn.onmouseover = () => retryBtn.style.background = '#616161';
//   retryBtn.onmouseout = () => retryBtn.style.background = '#757575';
//   retryBtn.onclick = () => {
//     overlay.remove();
//     // Trigger OCR again on current video
//     const video = document.querySelector('video');
//     if (video) {
//       const frame = captureFrame(video);
//       runOCR(frame);
//     }
//   };

//   buttonContainer.appendChild(copyBtn);
//   buttonContainer.appendChild(retryBtn);

//   // Assemble overlay
//   overlay.appendChild(header);
//   overlay.appendChild(mathBlock);
//   overlay.appendChild(rawSection);
//   overlay.appendChild(buttonContainer);
  
//   document.body.appendChild(overlay);

//   // Make overlay draggable
//   makeOverlayDraggable(overlay, header);
// }

// // 5. Make overlay draggable
// function makeOverlayDraggable(element, handle) {
//   let isDragging = false;
//   let currentX, currentY, initialX, initialY;

//   handle.addEventListener('mousedown', dragStart);
//   document.addEventListener('mousemove', drag);
//   document.addEventListener('mouseup', dragEnd);

//   function dragStart(e) {
//     initialX = e.clientX - element.offsetLeft;
//     initialY = e.clientY - element.offsetTop;
//     if (e.target === handle || handle.contains(e.target)) {
//       isDragging = true;
//       handle.style.cursor = 'grabbing';
//     }
//   }

//   function drag(e) {
//     if (isDragging) {
//       e.preventDefault();
//       currentX = e.clientX - initialX;
//       currentY = e.clientY - initialY;
//       element.style.left = currentX + 'px';
//       element.style.top = currentY + 'px';
//       element.style.right = 'auto';
//     }
//   }

//   function dragEnd() {
//     isDragging = false;
//     handle.style.cursor = 'grab';
//   }
// }

// // 6. Enhanced OCR with better error handling and retry logic
// async function runOCR(imageDataUrl, retryCount = 0) {
//   const maxRetries = 2;
  
//   try {
//     const response = await fetch('http://127.0.0.1:8000/ocr/single', {
//       method: 'POST',
//       body: convertDataUrlToFormData(imageDataUrl)
//     });

//     if (!response.ok) {
//       throw new Error(`HTTP ${response.status}: ${response.statusText}`);
//     }

//     const data = await response.json();
//     console.log('[🧠 OCR Result]', data);
    
//     let latex = '';
//     if (data?.best_result?.result) {
//       latex = cleanLaTeX(data.best_result.result);
//     } else if (data?.all_results?.length > 0) {
//       // Try to find any successful result
//       for (const result of data.all_results) {
//         if (result.result && !result.result.toLowerCase().includes('error')) {
//           latex = cleanLaTeX(result.result);
//           break;
//         }
//       }
//     }
    
//     if (!latex || latex === 'No readable LaTeX detected') {
//       latex = 'No mathematical expressions detected in this frame';
//     }
    
//     showMathOverlay(latex);
    
//   } catch (err) {
//     console.error('[❌ OCR Error]', err);
    
//     if (retryCount < maxRetries) {
//       console.log(`Retrying OCR (attempt ${retryCount + 2}/${maxRetries + 1})`);
//       setTimeout(() => runOCR(imageDataUrl, retryCount + 1), 1000);
//       return;
//     }
    
//     // Show error overlay
//     showMathOverlay(`Error: ${err.message}\n\nPlease ensure the backend is running on http://127.0.0.1:8000`);
//   }
// }

// // 7. Convert image to FormData (unchanged but documented)
// function convertDataUrlToFormData(dataUrl) {
//   const byteString = atob(dataUrl.split(',')[1]);
//   const mimeString = dataUrl.split(',')[0].split(':')[1].split(';')[0];
//   const ab = new ArrayBuffer(byteString.length);
//   const ia = new Uint8Array(ab);
//   for (let i = 0; i < byteString.length; i++) {
//     ia[i] = byteString.charCodeAt(i);
//   }
//   const blob = new Blob([ab], { type: mimeString });
//   const formData = new FormData();
//   formData.append("file", blob, "frame.png");
//   return formData;
// }

// // 8. Enhanced video listeners with multiple trigger options
// function setupVideoListeners() {
//   const videos = document.querySelectorAll('video');
  
//   videos.forEach((video, index) => {
//     console.log(`Setting up listeners for video ${index + 1}`);
    
//     // Pause trigger (original)
//     video.addEventListener('pause', () => {
//       console.log('⏸️ Video paused — capturing frame...');
//       setTimeout(() => {
//         const frame = captureFrame(video);
//         runOCR(frame);
//       }, 100); // Small delay to ensure video is fully paused
//     });
    
//     // Spacebar trigger (when video is focused)
//     video.addEventListener('keydown', (e) => {
//       if (e.code === 'Space' && !e.shiftKey && !e.ctrlKey && !e.altKey) {
//         console.log('⌨️ Spacebar pressed — capturing frame...');
//         e.preventDefault();
//         const frame = captureFrame(video);
//         runOCR(frame);
//       }
//     });
//   });
  
//   // Global keyboard shortcut (Ctrl+Shift+M)
//   document.addEventListener('keydown', (e) => {
//     if (e.ctrlKey && e.shiftKey && e.key === 'M') {
//       console.log('⌨️ Hotkey pressed — capturing frame...');
//       e.preventDefault();
//       const video = document.querySelector('video');
//       if (video) {
//         const frame = captureFrame(video);
//         runOCR(frame);
//       } else {
//         console.warn('No video found on page');
//       }
//     }
//   });

//   // Observer for dynamically added videos
//   const observer = new MutationObserver((mutations) => {
//     mutations.forEach((mutation) => {
//       mutation.addedNodes.forEach((node) => {
//         if (node.nodeType === 1) { // Element node
//           const newVideos = node.tagName === 'VIDEO' ? [node] : node.querySelectorAll('video');
//           newVideos.forEach((video) => {
//             if (!video.hasAttribute('data-ocr-setup')) {
//               console.log('📹 New video detected, setting up listeners...');
//               video.setAttribute('data-ocr-setup', 'true');
//               setupVideoListeners();
//             }
//           });
//         }
//       });
//     });
//   });

//   observer.observe(document.body, {
//     childList: true,
//     subtree: true
//   });
// }

// // Initialize
// console.log('🚀 Initializing enhanced Math OCR...');
// setupVideoListeners();

// // Add visual indicator that the script is active
// const indicator = document.createElement('div');
// indicator.innerHTML = '🔢';
// indicator.style.cssText = `
//   position: fixed;
//   bottom: 20px;
//   right: 20px;
//   background: rgba(0,0,0,0.7);
//   color: white;
//   padding: 8px;
//   border-radius: 50%;
//   z-index: 9998;
//   font-size: 16px;
//   cursor: pointer;
//   transition: transform 0.2s;
// `;
// indicator.title = 'Math OCR Active\nCtrl+Shift+M: Capture frame\nPause video: Auto-capture';
// indicator.onclick = () => {
//   const video = document.querySelector('video');
//   if (video) {
//     const frame = captureFrame(video);
//     runOCR(frame);
//   }
// };
// indicator.onmouseover = () => indicator.style.transform = 'scale(1.1)';
// indicator.onmouseout = () => indicator.style.transform = 'scale(1)';
// document.body.appendChild(indicator);





// // 📹 Content script for VideoMath Tutor
// console.log('📹 Content script running...');

// // 1. Capture current frame from paused video
// function captureFrame(video) {
//   const canvas = document.createElement('canvas');
//   canvas.width = video.videoWidth * 2;
//   canvas.height = video.videoHeight * 2;
//   const ctx = canvas.getContext('2d');
//   ctx.scale(2, 2);
//   ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
//   preprocessCanvas(canvas);
//   return canvas.toDataURL('image/png');
// }

// // 2. Enhance contrast + grayscale
// function preprocessCanvas(canvas) {
//   const ctx = canvas.getContext('2d');
//   const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
//   const data = imgData.data;
//   for (let i = 0; i < data.length; i += 4) {
//     const gray = 0.3 * data[i] + 0.59 * data[i+1] + 0.11 * data[i+2];
//     const value = gray > 140 ? 255 : 0;
//     data[i] = data[i+1] = data[i+2] = value;
//   }
//   ctx.putImageData(imgData, 0, 0);
// }

// // 3. Convert canvas to FormData
// function convertDataUrlToFormData(dataUrl) {
//   const byteString = atob(dataUrl.split(',')[1]);
//   const mime = dataUrl.split(',')[0].split(':')[1].split(';')[0];
//   const ab = new ArrayBuffer(byteString.length);
//   const ia = new Uint8Array(ab);
//   for (let i = 0; i < byteString.length; i++) ia[i] = byteString.charCodeAt(i);
//   const blob = new Blob([ab], { type: mime });
//   const formData = new FormData();
//   formData.append("file", blob, "frame.png");
//   return formData;
// }

// // 4. Render floating overlay
// function showOverlay(latex, hints = [], solution = null) {
//   const old = document.getElementById('videomath-tutor-overlay');
//   if (old) old.remove();

//   const overlay = document.createElement('div');
//   overlay.id = 'videomath-tutor-overlay';
//   overlay.style.cssText = `
//     position: fixed; top: 20px; right: 20px;
//     background: #fff; border: 1px solid #ccc;
//     padding: 16px; border-radius: 10px;
//     box-shadow: 0 8px 16px rgba(0,0,0,0.25);
//     font-family: sans-serif;
//     z-index: 9999; max-width: 400px;
//   `;

//   const title = document.createElement('div');
//   title.innerText = '📘 Math OCR Result';
//   title.style.fontWeight = 'bold';
//   title.style.marginBottom = '12px';

//   const closeBtn = document.createElement('span');
//   closeBtn.innerText = '✖';
//   closeBtn.style.cssText = 'position: absolute; top: 10px; right: 15px; cursor: pointer;';
//   closeBtn.onclick = () => overlay.remove();

//   const mathBlock = document.createElement('div');
//   mathBlock.style.marginBottom = '10px';
//   try {
//     katex.render(latex, mathBlock, { throwOnError: false });
//   } catch (e) {
//     mathBlock.innerText = latex;
//   }

//   const buttons = document.createElement('div');
//   buttons.style.marginTop = '10px';

//   const copyBtn = document.createElement('button');
//   copyBtn.textContent = '📋 Copy';
//   copyBtn.onclick = () => navigator.clipboard.writeText(latex);

//   const searchBtn = document.createElement('button');
//   searchBtn.textContent = '🔍 Web Search';
//   searchBtn.onclick = () => window.open(`https://www.google.com/search?q=${encodeURIComponent(latex)}`);

//   const solveBtn = document.createElement('button');
//   solveBtn.textContent = '✅ Solve';
//   solveBtn.onclick = async () => {
//     const res = await fetch('http://127.0.0.1:8000/solve', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({ expression: latex })
//     });
//     const data = await res.json();
//     alert(`✅ Solution:\n${data.solution}\n\n🧠 Explanation:\n${data.steps}`);
//   };

//   [copyBtn, searchBtn, solveBtn].forEach(btn => {
//     btn.style.marginRight = '8px';
//     btn.style.padding = '6px 10px';
//     btn.style.borderRadius = '4px';
//     btn.style.border = 'none';
//     btn.style.cursor = 'pointer';
//     btn.style.background = '#444';
//     btn.style.color = 'white';
//   });

//   buttons.append(copyBtn, searchBtn, solveBtn);

//   const hintBlock = document.createElement('div');
//   hintBlock.style.marginTop = '10px';
//   if (hints.length > 0) {
//     const hintTitle = document.createElement('strong');
//     hintTitle.innerText = '💡 Hints:';
//     hintBlock.appendChild(hintTitle);
//     const list = document.createElement('ul');
//     hints.forEach(h => {
//       const li = document.createElement('li');
//       li.innerText = h;
//       list.appendChild(li);
//     });
//     hintBlock.appendChild(list);
//   }

//   overlay.append(closeBtn, title, mathBlock, buttons, hintBlock);
//   document.body.appendChild(overlay);
// }

// // 5. Call backend
// function runOCR(imageDataUrl) {
//   fetch('http://127.0.0.1:8000/ocr/single', {
//     method: 'POST',
//     body: convertDataUrlToFormData(imageDataUrl)
//   })
//     .then(res => res.json())
//     .then(data => {
//       console.log('[🧠 OCR Result]', data);
//       const raw = (data?.best_result?.result || '').replace(/.*\.png[:\uff1a]\s*/gi, '').trim();
//       const hints = generateHints(raw);
//       showOverlay(raw, hints);
//     })
//     .catch(err => {
//       console.error('[❌ OCR Error]', err);
//       alert('⚠️ Failed to fetch OCR result. Ensure backend is running.');
//     });
// }

// // 6. Basic hint generation
// function generateHints(expr) {
//   const hints = [];
//   if (expr.includes('|')) hints.push("This looks like an absolute value equation. Consider splitting into cases.");
//   if (expr.includes('lim')) hints.push("You might need L'Hôpital's Rule if you get 0/0.");
//   if (expr.includes('tan') || expr.includes('sin') || expr.includes('cos')) hints.push("Use trigonometric identities.");
//   if (expr.includes('x^2') || expr.includes('x**2')) hints.push("Looks quadratic — factor or use the quadratic formula.");
//   if (expr.includes('=')) hints.push("Try isolating the variable.");
//   return hints;
// }

// // 7. Activate on pause
// function setupVideoListeners() {
//   const videos = document.querySelectorAll('video');
//   videos.forEach(video => {
//     if (!video.dataset.listenerAttached) {
//       video.addEventListener('pause', () => {
//         console.log('⏸️ Video paused — capturing...');
//         const frame = captureFrame(video);
//         runOCR(frame);
//       });
//       video.dataset.listenerAttached = 'true';
//     }
//   });
// }


// setupVideoListeners();








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
