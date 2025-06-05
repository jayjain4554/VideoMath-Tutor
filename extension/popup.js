let isActive = true;

const btn = document.getElementById('toggle-btn');
btn.addEventListener('click', async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (isActive) {
    btn.textContent = '🔴 Inactive';
    btn.classList.remove('on');
    btn.classList.add('off');

    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => window.VideoMathEnabled = false
    });
  } else {
    btn.textContent = '🟢 Active';
    btn.classList.remove('off');
    btn.classList.add('on');

    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['content.js']
    });
  }

  isActive = !isActive;
});
