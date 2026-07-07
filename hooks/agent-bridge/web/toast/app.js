(() => {
  const titleEl = document.getElementById('title');
  const subtitleEl = document.getElementById('subtitle');
  let cfg = null;
  let closing = false;

  function applyConfig(config) {
    cfg = config;
    titleEl.textContent = config.content?.title ?? 'Agent 已完成';
    subtitleEl.textContent = config.content?.subtitle ?? '等待下一步输入';
    const root = document.documentElement.style;
    root.setProperty('--enter-ms', `${config.timing?.enter_ms ?? 260}ms`);
    root.setProperty('--exit-ms', `${config.timing?.exit_ms ?? 220}ms`);
  }

  async function closeWindow() {
    if (closing || !cfg) {
      return;
    }
    closing = true;
    document.body.classList.add('closing');
    window.setTimeout(() => {
      window.pywebview.api.close();
    }, cfg.timing?.exit_ms ?? 220);
  }

  window.pywebviewready = async () => {
    const config = await window.pywebview.api.get_config();
    applyConfig(config);
    requestAnimationFrame(() => {
      document.body.classList.add('ready');
    });
    window.setTimeout(closeWindow, config.timing?.visible_ms ?? 3000);
  };

  window.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeWindow();
    }
  });
})();
