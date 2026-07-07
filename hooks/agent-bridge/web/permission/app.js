(() => {
  const brandEl = document.getElementById('brand');
  const headlineEl = document.getElementById('headline');
  const subtitleEl = document.getElementById('subtitle');
  const toolLabelEl = document.getElementById('toolLabel');
  const toolNameEl = document.getElementById('toolName');
  const toggleEl = document.getElementById('toggle');
  const summaryEl = document.getElementById('summary');
  const detailWrapEl = document.getElementById('detailWrap');
  const detailEl = document.getElementById('detail');
  const denyBtn = document.getElementById('deny');
  const allowBtn = document.getElementById('allow');
  const allowRememberBtn = document.getElementById('allowRemember');

  let cfg = null;
  let expanded = false;
  let closing = false;

  function formatDetail(input) {
    const lines = [];
    for (const [key, value] of Object.entries(input || {})) {
      if (key === 'description') {
        continue;
      }
      if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
        lines.push(`${key}: ${value}`);
      } else {
        lines.push(`${key}: ${JSON.stringify(value)}`);
      }
    }
    return lines.join('\n');
  }

  function applyConfig(config, payload) {
    cfg = config;
    brandEl.textContent = config.brand ?? 'Agent Mecha';
    headlineEl.textContent = config.headline ?? '允许这次操作？';
    subtitleEl.textContent = config.subtitle ?? 'Agent 请求使用工具。拒绝会停止当前处理。';
    toolLabelEl.textContent = config.tool_label ?? 'TOOL';
    toolNameEl.textContent = payload.tool_name ?? 'Unknown';
    toggleEl.textContent = config.toggle_expand ?? '展开';
    summaryEl.textContent = formatDetail(payload.tool_input);
    detailEl.textContent = payload.detail ?? formatDetail(payload.tool_input);
    denyBtn.textContent = config.buttons?.deny ?? '拒绝';
    allowBtn.textContent = config.buttons?.allow ?? '同意';
    allowRememberBtn.textContent = config.buttons?.allow_and_remember ?? '同意并记住';
    document.documentElement.style.setProperty('--enter-ms', `${config.motion?.enter_ms ?? 180}ms`);
    document.documentElement.style.setProperty('--exit-ms', `${config.motion?.exit_ms ?? 160}ms`);
  }

  function syncDetail() {
    detailWrapEl.classList.toggle('hidden', !expanded);
    toggleEl.textContent = expanded
      ? (cfg.toggle_collapse ?? '折叠')
      : (cfg.toggle_expand ?? '展开');
  }

  async function submit(action) {
    if (closing || !cfg) {
      return;
    }
    closing = true;
    document.body.classList.add('closing');
    window.setTimeout(async () => {
      try {
        await window.pywebview.api.finish(action);
      } catch (error) {
        console.error(error);
      }
    }, cfg.motion?.exit_ms ?? 160);
  }

  window.pywebviewready = async () => {
    const [config, payload] = await Promise.all([
      window.pywebview.api.get_config(),
      window.pywebview.api.get_data(),
    ]);
    applyConfig(config, payload);
    syncDetail();
    requestAnimationFrame(() => document.body.classList.add('ready'));
  };

  toggleEl.addEventListener('click', () => {
    expanded = !expanded;
    syncDetail();
  });

  denyBtn.addEventListener('click', () => submit('deny'));
  allowBtn.addEventListener('click', () => submit('allow'));
  allowRememberBtn.addEventListener('click', () => submit('allow_and_remember'));

  window.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      submit('deny');
    } else if (event.key === 'Enter') {
      submit('allow');
    }
  });
})();
