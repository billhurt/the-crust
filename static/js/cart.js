function getCsrf() {
  const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
  if (cookie) return cookie.split('=')[1];
  const input = document.querySelector('[name=csrfmiddlewaretoken]');
  if (input) return input.value;
  return '';
}

function showToast(msg) {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = msg;
  container.appendChild(toast);
  requestAnimationFrame(() => {
    requestAnimationFrame(() => toast.classList.add('show'));
  });
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

function updateNavCount(count) {
  const badge = document.querySelector('.cart-badge');
  const link = document.querySelector('.cart-link');
  if (count > 0) {
    if (badge) {
      badge.textContent = count;
    } else if (link) {
      const b = document.createElement('span');
      b.className = 'cart-badge';
      b.textContent = count;
      link.appendChild(b);
    }
  } else if (badge) {
    badge.remove();
  }
}

function cartAdd(itemId, btn) {
  fetch(`/orders/cart/add/${itemId}/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body: JSON.stringify({ quantity: 1 })
  })
  .then(r => r.json())
  .then(data => {
    updateNavCount(data.cart_count);
    showToast(data.message);

    // Replace + button with qty control
    const control = document.getElementById(`control-${itemId}`);
    if (control) {
      // Check if qty control already exists
      const existing = control.querySelector('.qty-control');
      if (existing) {
        const numEl = control.querySelector('.qty-num');
        if (numEl) numEl.textContent = parseInt(numEl.textContent) + 1;
      } else {
        control.innerHTML = `
          <div class="qty-control">
            <button class="qty-btn" onclick="cartAdjust(${itemId}, -1)">−</button>
            <span class="qty-num" id="qtyDisp-${itemId}">1</span>
            <button class="qty-btn" onclick="cartAdjust(${itemId}, 1)">+</button>
          </div>`;
      }
    }
  })
  .catch(() => showToast('Could not add item — try again'));
}

function cartAdjust(itemId, delta) {
  const numEl = document.getElementById(`qtyDisp-${itemId}`);
  const currentQty = numEl ? parseInt(numEl.textContent) : 1;
  const newQty = currentQty + delta;

  fetch(`/orders/cart/update/${itemId}/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body: JSON.stringify({ quantity: newQty })
  })
  .then(r => r.json())
  .then(data => {
    updateNavCount(data.cart_count);
    const control = document.getElementById(`control-${itemId}`);
    if (newQty <= 0) {
      if (control) {
        control.innerHTML = `<button class="btn-add" onclick="cartAdd(${itemId}, this)">+</button>`;
      }
    } else if (numEl) {
      numEl.textContent = newQty;
    }
  });
}
