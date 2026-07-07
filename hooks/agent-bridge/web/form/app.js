(() => {
  const CUSTOM_VALUE = '__custom_input__';

  const titleEl = document.getElementById('title');
  const messageEl = document.getElementById('message');
  const contentEl = document.getElementById('content');
  const errorEl = document.getElementById('error');
  const cancelBtn = document.getElementById('cancel');
  const declineBtn = document.getElementById('decline');
  const acceptBtn = document.getElementById('accept');

  let cfg = null;
  let spec = null;
  let closing = false;
  const state = new Map();
  const customState = new Map();

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) {
      node.className = className;
    }
    if (text !== undefined && text !== null) {
      node.textContent = String(text);
    }
    return node;
  }

  function setError(message) {
    errorEl.textContent = message || '';
    errorEl.title = message || '';
  }

  function optionInitialValue(field) {
    const values = new Set((field.options || []).map((option) => String(option.value)));
    if (field.default === null || field.default === undefined) {
      return field.options?.[0]?.value ?? '';
    }
    if (values.has(String(field.default))) {
      return field.default;
    }
    if (field.allow_custom) {
      customState.set(field.name, String(field.default));
      return CUSTOM_VALUE;
    }
    return field.options?.[0]?.value ?? '';
  }

  function syncOptionCards(field, wrapper) {
    wrapper.querySelectorAll('.option').forEach((card) => {
      card.classList.toggle('selected', String(card.dataset.value) === String(state.get(field.name)));
      const input = card.querySelector('input[type="radio"]');
      if (input) {
        input.checked = String(input.value) === String(state.get(field.name));
      }
    });
  }

  function buildOption(field, option, wrapper) {
    const card = el('label', 'option');
    card.dataset.value = String(option.value);

    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = field.name;
    radio.value = String(option.value);

    const copy = el('div');
    copy.appendChild(el('div', 'option-label', option.label));
    if (option.description) {
      copy.appendChild(el('div', 'option-description', option.description));
    }

    card.appendChild(radio);
    card.appendChild(copy);

    card.addEventListener('click', () => {
      state.set(field.name, option.value);
      setError('');
      syncOptionCards(field, wrapper);
    });

    return card;
  }

  function buildCustomOption(field, wrapper) {
    const card = el('label', 'option');
    card.dataset.value = CUSTOM_VALUE;

    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = field.name;
    radio.value = CUSTOM_VALUE;

    const copy = el('div');
    copy.appendChild(el('div', 'option-label', cfg.custom_label ?? '自定义输入'));
    copy.appendChild(el('div', 'option-description', '输入一个不在列表中的值。'));

    card.appendChild(radio);
    card.appendChild(copy);

    const input = document.createElement('input');
    input.className = 'input';
    input.type = 'text';
    input.value = customState.get(field.name) ?? '';
    input.placeholder = cfg.custom_placeholder ?? '请输入自定义内容';

    const selectCustom = () => {
      state.set(field.name, CUSTOM_VALUE);
      setError('');
      syncOptionCards(field, wrapper);
    };

    card.addEventListener('click', selectCustom);
    input.addEventListener('focus', selectCustom);
    input.addEventListener('input', () => {
      customState.set(field.name, input.value);
      selectCustom();
    });

    const block = el('div');
    block.appendChild(card);
    block.appendChild(input);
    return block;
  }

  function buildOptionsField(field, fieldEl) {
    const wrapper = el('div', 'options');
    state.set(field.name, optionInitialValue(field));

    (field.options || []).forEach((option) => {
      wrapper.appendChild(buildOption(field, option, wrapper));
    });

    if (field.allow_custom) {
      wrapper.appendChild(buildCustomOption(field, wrapper));
    }

    fieldEl.appendChild(wrapper);
    syncOptionCards(field, wrapper);
  }

  function buildBooleanField(field, fieldEl) {
    const row = el('label', 'checkbox-row');
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.checked = Boolean(field.default);
    state.set(field.name, input.checked);
    input.addEventListener('change', () => {
      state.set(field.name, input.checked);
      setError('');
    });
    row.appendChild(input);
    row.appendChild(el('span', null, cfg.boolean_label ?? '启用'));
    fieldEl.appendChild(row);
  }

  function buildTextField(field, fieldEl) {
    const input = document.createElement('input');
    input.className = 'input';
    input.type = field.type === 'number' || field.type === 'integer' ? 'number' : 'text';
    input.value = field.default === null || field.default === undefined ? '' : String(field.default);
    input.placeholder = field.placeholder ?? '';
    state.set(field.name, input.value);
    input.addEventListener('input', () => {
      state.set(field.name, input.value);
      setError('');
    });
    fieldEl.appendChild(input);
    window.setTimeout(() => input.focus(), 50);
  }

  function buildField(field) {
    const fieldEl = el('section', 'field');
    fieldEl.appendChild(el('div', 'field-title', field.title));
    if (field.description) {
      fieldEl.appendChild(el('div', 'field-description', field.description));
    }

    if (field.options && field.options.length) {
      buildOptionsField(field, fieldEl);
    } else if (field.type === 'boolean') {
      buildBooleanField(field, fieldEl);
    } else {
      buildTextField(field, fieldEl);
    }

    return fieldEl;
  }

  function render() {
    titleEl.textContent = spec.title || '需要选择';
    messageEl.textContent = spec.message || '';
    contentEl.replaceChildren();

    if (!spec.fields || !spec.fields.length) {
      contentEl.appendChild(el('div', 'empty', cfg.messages?.missing_fields ?? '没有检测到表单字段。'));
      return;
    }

    spec.fields.forEach((field) => {
      contentEl.appendChild(buildField(field));
    });
  }

  function content() {
    const result = {};
    (spec.fields || []).forEach((field) => {
      let value = state.get(field.name);
      if (field.allow_custom && value === CUSTOM_VALUE) {
        value = (customState.get(field.name) ?? '').trim();
      }
      result[field.name] = value;
    });
    return result;
  }

  function closeWithAnimation() {
    closing = true;
    document.body.classList.add('closing');
  }

  async function submit(action) {
    if (closing || !cfg) {
      return;
    }
    setError('');

    try {
      const response = await window.pywebview.api.finish(action, action === 'accept' ? content() : {});
      if (response && response.ok === false) {
        setError(response.error || cfg.messages?.invalid_input || '输入无效');
        return;
      }
      closeWithAnimation();
    } catch (error) {
      setError(String(error));
    }
  }

  window.pywebviewready = async () => {
    const data = await window.pywebview.api.get_data();
    cfg = data.config || {};
    spec = data.spec || { title: '', message: '', fields: [] };
    cancelBtn.textContent = cfg.buttons?.cancel ?? '取消';
    declineBtn.textContent = cfg.buttons?.decline ?? '拒绝';
    acceptBtn.textContent = cfg.buttons?.accept ?? '确定';
    document.documentElement.style.setProperty('--enter-ms', `${cfg.motion?.enter_ms ?? 180}ms`);
    document.documentElement.style.setProperty('--exit-ms', `${cfg.motion?.exit_ms ?? 160}ms`);
    render();
    requestAnimationFrame(() => document.body.classList.add('ready'));
  };

  cancelBtn.addEventListener('click', () => submit('cancel'));
  declineBtn.addEventListener('click', () => submit('decline'));
  acceptBtn.addEventListener('click', () => submit('accept'));

  window.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      submit('cancel');
    } else if (event.key === 'Enter' && (event.metaKey || event.ctrlKey)) {
      submit('accept');
    }
  });
})();
