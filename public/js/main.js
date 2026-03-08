    // Dynamic API URL setup relative to the current host
    const API = window.location.origin;
    let selectedQuality = '1080p';
    let pollTimer = null;

    // Quality buttons
    document.querySelectorAll('.q-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.q-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedQuality = btn.dataset.q;
      });
    });

    // Enter key
    document.getElementById('urlInput').addEventListener('keydown', e => {
      if (e.key === 'Enter') fetchInfo();
    });

    function formatDuration(s) {
      const h = Math.floor(s / 3600);
      const m = Math.floor((s % 3600) / 60);
      const sec = s % 60;
      if (h > 0) return `${h}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
      return `${m}:${String(sec).padStart(2, '0')}`;
    }

    function formatViews(n) {
      if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
      if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
      return n;
    }

    function showError(msg) {
      const el = document.getElementById('errorBox');
      el.textContent = '⚠ ' + msg;
      el.classList.add('visible');
    }

    function clearError() {
      document.getElementById('errorBox').classList.remove('visible');
    }

    async function fetchInfo() {
      const url = document.getElementById('urlInput').value.trim();
      if (!url) return;

      clearError();
      document.getElementById('videoInfo').classList.remove('visible');
      document.getElementById('doneBox').classList.remove('visible');
      document.getElementById('progressArea').classList.remove('visible');

      const btn = document.getElementById('fetchBtn');
      btn.disabled = true;
      btn.innerHTML = '<span class="spin"></span>';

      try {
        const res = await fetch(`${API}/api/info`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url })
        });
        const data = await res.json();

        if (data.error) { showError(data.error); return; }

        document.getElementById('thumb').src = data.thumbnail;
        document.getElementById('vidTitle').textContent = data.title;
        document.getElementById('vidChannel').textContent = data.channel;
        document.getElementById('vidDuration').textContent = formatDuration(data.duration);
        document.getElementById('vidViews').textContent = formatViews(data.view_count) + ' görüntüleme';
        document.getElementById('videoInfo').classList.add('visible');
      } catch (e) {
        showError('Sunucuya bağlanılamadı. Python sunucusu çalışıyor mu?');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Getir';
      }
    }

    async function startDownload() {
      const url = document.getElementById('urlInput').value.trim();
      if (!url) { showError('Önce bir URL gir ve "Getir" butonuna bas.'); return; }

      clearError();
      document.getElementById('doneBox').classList.remove('visible');

      const dlBtn = document.getElementById('dlBtn');
      dlBtn.disabled = true;
      dlBtn.innerHTML = '<span class="spin"></span> Başlatılıyor...';

      const progressArea = document.getElementById('progressArea');
      const progressFill = document.getElementById('progressFill');
      const progressPct = document.getElementById('progressPct');
      const progressStatus = document.getElementById('progressStatus');
      const progressSpeed = document.getElementById('progressSpeed');
      const progressEta = document.getElementById('progressEta');

      progressFill.style.width = '0%';
      progressFill.classList.remove('done');
      progressArea.classList.add('visible');

      try {
        const res = await fetch(`${API}/api/download`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url, quality: selectedQuality })
        });
        const { task_id, error } = await res.json();
        if (error) { showError(error); return; }

        // Poll progress
        pollTimer = setInterval(async () => {
          const pRes = await fetch(`${API}/api/progress/${task_id}`);
          const p = await pRes.json();

          if (p.status === 'downloading') {
            progressFill.style.width = p.percent + '%';
            progressPct.textContent = p.percent + '%';
            progressSpeed.textContent = p.speed || '—';
            progressEta.textContent = 'ETA: ' + (p.eta || '—');
            progressStatus.textContent = 'İndiriliyor...';
            dlBtn.innerHTML = `<span class="spin"></span> ${p.percent}% İndiriliyor`;
          } else if (p.status === 'processing') {
            progressFill.style.width = '99%';
            progressPct.textContent = '99%';
            progressStatus.textContent = 'İşleniyor (birleştiriliyor)...';
            dlBtn.innerHTML = '<span class="spin"></span> İşleniyor...';
          } else if (p.status === 'done') {
            clearInterval(pollTimer);
            progressFill.style.width = '100%';
            progressFill.classList.add('done');
            progressPct.textContent = '100%';
            progressStatus.textContent = 'Tamamlandı!';
            progressSpeed.textContent = '';
            progressEta.textContent = '';

            document.getElementById('doneFilename').textContent = p.filename || '';
            document.getElementById('saveLink').href = `${API}/api/file/${task_id}`;
            document.getElementById('doneBox').classList.add('visible');

            dlBtn.disabled = false;
            dlBtn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg> Tekrar İndir`;
          } else if (p.status === 'error') {
            clearInterval(pollTimer);
            showError(p.error || 'Bilinmeyen hata');
            dlBtn.disabled = false;
            dlBtn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg> İndir`;
            progressArea.classList.remove('visible');
          }
        }, 800);

      } catch (e) {
        showError('Sunucuya bağlanılamadı. Python sunucusu çalışıyor mu?');
        dlBtn.disabled = false;
        dlBtn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg> İndir`;
      }
    }
