(() => {
  const ready = (callback) => {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback);
      return;
    }
    callback();
  };

  const all = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  const normalizePath = (path) => {
    const normalized = path.replace(/\/+$/, "");
    return normalized || "/";
  };

  const setActiveNavigation = () => {
    const currentPath = normalizePath(window.location.pathname);

    all(".navbar .nav-link").forEach((link) => {
      const linkPath = normalizePath(new URL(link.href, window.location.origin).pathname);
      const isActive = linkPath === "/" ? currentPath === "/" : currentPath.startsWith(linkPath);

      link.classList.toggle("active", isActive);
      if (isActive) {
        link.setAttribute("aria-current", "page");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  };

  const setupReveal = () => {
    const elements = all(".card-soft, .metric-tile, .workflow-tile, .surface-panel, .product-card");

    if (!("IntersectionObserver" in window)) {
      elements.forEach((element) => element.classList.add("is-visible"));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
    );

    elements.forEach((element, index) => {
      element.classList.add("ui-reveal");
      element.style.setProperty("--reveal-delay", `${Math.min(index * 35, 210)}ms`);
      observer.observe(element);
    });
  };

  const setupProductFilter = () => {
    const input = document.querySelector("[data-live-search]");
    const grid = document.querySelector("[data-product-grid]");

    if (!input || !grid) {
      return;
    }

    const cards = all("[data-product-card]", grid);
    const count = document.querySelector("[data-product-count]");
    const emptyState = document.querySelector("[data-empty-state]");
    const total = cards.length;

    const pluralize = (value) => `${value} product${value === 1 ? "" : "s"}`;

    const update = () => {
      const terms = input.value
        .trim()
        .toLowerCase()
        .split(/\s+/)
        .filter(Boolean);
      let visible = 0;

      cards.forEach((card) => {
        const haystack = (card.dataset.search || "").toLowerCase();
        const matches = terms.every((term) => haystack.includes(term));

        card.classList.toggle("is-hidden", !matches);
        visible += matches ? 1 : 0;
      });

      if (count) {
        count.textContent = terms.length ? `${pluralize(visible)} match` : pluralize(total);
      }

      if (emptyState) {
        emptyState.classList.toggle("is-hidden", visible !== 0);
      }
    };

    input.addEventListener("input", update);
    update();
  };

  const setupQuantityControls = () => {
    all("[data-quantity-control]").forEach((control) => {
      const input = control.querySelector("input[type='number']");

      if (!input) {
        return;
      }

      all("[data-quantity-step]", control).forEach((button) => {
        button.addEventListener("click", () => {
          const step = Number(button.dataset.quantityStep || 0);
          const min = Number(input.min || 1);
          const max = input.max ? Number(input.max) : Infinity;
          const current = Number(input.value || min);
          const next = Math.min(max, Math.max(min, current + step));

          input.value = String(next);
          input.dispatchEvent(new Event("change", { bubbles: true }));
        });
      });
    });
  };

  const setupLoadingButtons = () => {
    all("form").forEach((form) => {
      form.addEventListener("submit", (event) => {
        const submitter = event.submitter;

        if (!submitter || !submitter.matches("[data-loading-label]") || submitter.disabled) {
          return;
        }

        submitter.dataset.originalText = submitter.innerHTML;
        submitter.disabled = true;
        submitter.innerHTML = `<span class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>${submitter.dataset.loadingLabel}`;
      });
    });
  };

  const setupPaymentPreview = () => {
    const form = document.querySelector("[data-payment-form]");

    if (!form) {
      return;
    }

    const cardInput = form.querySelector("[data-card-number]");
    const nameInput = form.querySelector("[data-card-name]");
    const monthInput = form.querySelector("#exp_month");
    const yearInput = form.querySelector("#exp_year");
    const numberPreview = document.querySelector("[data-card-preview='number']");
    const namePreview = document.querySelector("[data-card-preview='name']");
    const expiryPreview = document.querySelector("[data-card-preview='expiry']");

    const groupCardNumber = (value) =>
      value
        .replace(/\D/g, "")
        .slice(0, 19)
        .replace(/(.{4})/g, "$1 ")
        .trim();

    const update = () => {
      const grouped = groupCardNumber(cardInput.value);
      const visible = grouped || "•••• •••• •••• ••••";
      const month = monthInput.value.replace(/\D/g, "").slice(0, 2);
      const year = yearInput.value.replace(/\D/g, "").slice(-2);

      cardInput.value = grouped;
      numberPreview.textContent = visible;
      namePreview.textContent = nameInput.value.trim().toUpperCase() || "CARDHOLDER";
      expiryPreview.textContent = month || year ? `${month || "MM"}/${year || "YY"}` : "MM/YY";
    };

    [cardInput, nameInput, monthInput, yearInput].forEach((input) => {
      input.addEventListener("input", update);
    });

    update();
  };

  const setupTooltips = () => {
    if (!window.bootstrap) {
      return;
    }

    all("[data-bs-toggle='tooltip']").forEach((trigger) => {
      window.bootstrap.Tooltip.getOrCreateInstance(trigger);
    });
  };

  const closeMobileNavAfterClick = () => {
    const nav = document.getElementById("navMain");

    if (!nav || !window.bootstrap) {
      return;
    }

    all(".navbar .nav-link", nav).forEach((link) => {
      link.addEventListener("click", () => {
        const collapse = window.bootstrap.Collapse.getInstance(nav);

        if (collapse && nav.classList.contains("show")) {
          collapse.hide();
        }
      });
    });
  };

  ready(() => {
    setActiveNavigation();
    setupReveal();
    setupProductFilter();
    setupQuantityControls();
    setupLoadingButtons();
    setupPaymentPreview();
    setupTooltips();
    closeMobileNavAfterClick();
  });
})();
