// Campus-AI: Intelligent Student Support System Frontend Controller
document.addEventListener("DOMContentLoaded", () => {
  // App State
  const state = {
    theme: localStorage.getItem("campusai_theme") || "dark",
    ttsEnabled: localStorage.getItem("campusai_tts") === "true",
    soundEnabled: localStorage.getItem("campusai_sound") !== "false",
    isRecording: false,
    activeTab: "tab-chat",
    recognition: null,
  };

  // Sound Engine using Web Audio API
  const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  function playSound(type) {
    if (!state.soundEnabled) return;
    try {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.connect(gain);
      gain.connect(audioCtx.destination);

      if (type === "send") {
        osc.frequency.setValueAtTime(440, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.1);
        gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.1);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.1);
      } else if (type === "receive") {
        osc.frequency.setValueAtTime(600, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(750, audioCtx.currentTime + 0.15);
        gain.gain.setValueAtTime(0.06, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.15);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.15);
      }
    } catch (e) {
      // AudioContext autostart restrictions handled gracefully
    }
  }

  // Theme Management
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    state.theme = theme;
    localStorage.setItem("campusai_theme", theme);
    const icon = document.getElementById("theme-icon");
    if (icon) {
      icon.className = theme === "dark" ? "fa-solid fa-moon" : "fa-solid fa-sun";
    }
  }
  applyTheme(state.theme);

  document.getElementById("toggle-theme-btn")?.addEventListener("click", () => {
    applyTheme(state.theme === "dark" ? "light" : "dark");
  });

  // Sound Toggle
  const soundIcon = document.getElementById("sound-icon");
  if (soundIcon) {
    soundIcon.className = state.soundEnabled ? "fa-solid fa-bell" : "fa-solid fa-bell-slash text-red-400";
  }
  document.getElementById("toggle-sound-btn")?.addEventListener("click", () => {
    state.soundEnabled = !state.soundEnabled;
    localStorage.setItem("campusai_sound", state.soundEnabled);
    if (soundIcon) {
      soundIcon.className = state.soundEnabled ? "fa-solid fa-bell" : "fa-solid fa-bell-slash text-red-400";
    }
  });

  // TTS Toggle
  const ttsIcon = document.getElementById("tts-icon");
  if (ttsIcon) {
    ttsIcon.className = state.ttsEnabled ? "fa-solid fa-volume-high text-indigo-400" : "fa-solid fa-volume-xmark";
  }
  document.getElementById("toggle-tts-btn")?.addEventListener("click", () => {
    state.ttsEnabled = !state.ttsEnabled;
    localStorage.setItem("campusai_tts", state.ttsEnabled);
    if (ttsIcon) {
      ttsIcon.className = state.ttsEnabled ? "fa-solid fa-volume-high text-indigo-400" : "fa-solid fa-volume-xmark";
    }
    if (!state.ttsEnabled && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  });

  // Text-To-Speech Reader Helper
  function speakText(text) {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    // Strip markdown tags for natural speech
    const cleanText = text
      .replace(/[#*`_~]/g, "")
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
      .replace(/\|/g, " ")
      .slice(0, 500);

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  }

  // Tab Switching
  const navTabs = document.querySelectorAll(".nav-tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  function switchTab(targetTabId) {
    navTabs.forEach((tab) => {
      tab.classList.toggle("active", tab.dataset.tab === targetTabId);
    });
    tabContents.forEach((content) => {
      content.classList.toggle("hidden", content.id !== targetTabId);
    });
    state.activeTab = targetTabId;

    // Load data when certain tabs are first opened
    if (targetTabId === "tab-programs") loadPrograms();
    if (targetTabId === "tab-directory") loadDirectory();
    if (targetTabId === "tab-clubs") loadClubs();
  }

  navTabs.forEach((btn) => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });

  // Mobile Menu Logic
  const mobileMenuBtn = document.getElementById("mobile-menu-btn");
  const mobileMenuModal = document.getElementById("mobile-menu-modal");
  const closeMobileMenu = document.getElementById("close-mobile-menu");
  const mobileTabsContainer = document.getElementById("mobile-tabs-container");

  if (mobileTabsContainer) {
    mobileTabsContainer.innerHTML = document.querySelector("#sidebar-nav .glass-panel")?.innerHTML || "";
    mobileTabsContainer.querySelectorAll(".nav-tab-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        switchTab(btn.dataset.tab);
        mobileMenuModal?.classList.add("hidden");
      });
    });
  }

  mobileMenuBtn?.addEventListener("click", () => {
    mobileMenuModal?.classList.remove("hidden");
  });
  closeMobileMenu?.addEventListener("click", () => {
    mobileMenuModal?.classList.add("hidden");
  });

  // ================= CHAT ASSISTANT ENGINE =================
  const chatMessages = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const categorySelect = document.getElementById("chat-category-select");

  window.sendQuickPrompt = function (text) {
    if (chatInput) {
      chatInput.value = text;
      switchTab("tab-chat");
      chatForm?.dispatchEvent(new Event("submit"));
    }
  };

  function appendUserMessage(text) {
    const userDiv = document.createElement("div");
    userDiv.className = "flex gap-3 justify-end animate-slide-up";
    userDiv.innerHTML = `
      <div class="max-w-[80%] rounded-2xl rounded-tr-sm bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-3.5 shadow-md">
        <p class="text-sm font-medium leading-relaxed">${escapeHtml(text)}</p>
      </div>
      <div class="w-9 h-9 rounded-xl bg-slate-700 flex items-center justify-center flex-shrink-0 text-white text-xs font-bold shadow-md">
        YOU
      </div>
    `;
    chatMessages.appendChild(userDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    playSound("send");
  }

  function showTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.id = "typing-indicator";
    typingDiv.className = "flex gap-3 animate-slide-up";
    typingDiv.innerHTML = `
      <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center flex-shrink-0 text-white shadow-md">
        <i class="fa-solid fa-robot text-sm"></i>
      </div>
      <div class="glass-panel p-3.5 rounded-2xl rounded-tl-sm flex items-center gap-2">
        <span class="text-xs text-[var(--text-secondary)] font-medium">Consulting ABES Knowledge Base</span>
        <div class="flex items-center gap-1 ml-1">
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
        </div>
      </div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function removeTypingIndicator() {
    document.getElementById("typing-indicator")?.remove();
  }

  function appendBotMessage(data) {
    removeTypingIndicator();
    playSound("receive");

    const botDiv = document.createElement("div");
    botDiv.className = "flex gap-3 animate-slide-up";

    const parsedHtml = marked.parse(data.answer);

    // Build source citations
    let sourcesHtml = "";
    if (data.sources && data.sources.length > 0) {
      sourcesHtml = `
        <div class="mt-3 pt-3 border-t border-[var(--border-subtle)]">
          <details class="cursor-pointer">
            <summary class="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1.5 list-none select-none">
              <i class="fa-solid fa-circle-nodes text-[11px]"></i>
              <span>Verified Sources & Citations (${data.sources.length})</span>
              <span class="text-[10px] text-[var(--text-muted)] ml-auto">Click to inspect</span>
            </summary>
            <div class="mt-2 space-y-1.5">
              ${data.sources
                .map(
                  (s) => `
                <div class="source-card">
                  <div class="flex items-center justify-between font-mono text-[11px] text-indigo-300 mb-1">
                    <span class="font-bold">[${s.id}]</span>
                    <span class="badge-pill badge-year py-0 px-1.5 text-[9px]">${s.academic_year || "Official"}</span>
                  </div>
                  <p class="text-[11px] text-[var(--text-secondary)] mb-1">${escapeHtml(s.content)}</p>
                  <a href="${s.source_url}" target="_blank" class="text-[10px] text-emerald-400 hover:underline flex items-center gap-1">
                    <i class="fa-solid fa-arrow-up-right-from-square text-[8px]"></i>
                    ${s.source_url}
                  </a>
                </div>
              `
                )
                .join("")}
            </div>
          </details>
        </div>
      `;
    }

    // Build Follow-up prompt chips
    let followUpsHtml = "";
    if (data.follow_ups && data.follow_ups.length > 0) {
      followUpsHtml = `
        <div class="flex flex-wrap gap-1.5 mt-3">
          ${data.follow_ups
            .map(
              (f) => `
            <button class="chip-btn text-[11px] py-1 px-3" onclick="sendQuickPrompt('${escapeAttr(f)}')">
              ${escapeHtml(f)}
            </button>
          `
            )
            .join("")}
        </div>
      `;
    }

    botDiv.innerHTML = `
      <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center flex-shrink-0 text-white shadow-md">
        <i class="fa-solid fa-robot text-sm"></i>
      </div>
      <div class="flex-1 max-w-[88%]">
        <div class="glass-panel p-4 rounded-2xl rounded-tl-sm chat-prose">
          ${parsedHtml}
          ${sourcesHtml}
          ${followUpsHtml}
        </div>

        <!-- Bot Message Actions -->
        <div class="flex items-center gap-3 mt-1.5 px-2 text-[11px] text-[var(--text-muted)]">
          <span>${data.timestamp || "Just now"}</span>
          <button class="hover:text-white transition flex items-center gap-1" onclick="copyMessageText(this)">
            <i class="fa-regular fa-copy"></i> Copy
          </button>
          <button class="hover:text-white transition flex items-center gap-1" onclick="speakMessageText(this)">
            <i class="fa-solid fa-volume-high"></i> Listen
          </button>
          <button class="hover:text-emerald-400 transition flex items-center gap-1" onclick="toggleHelpful(this)">
            <i class="fa-regular fa-thumbs-up"></i> Helpful
          </button>
        </div>
      </div>
    `;

    chatMessages.appendChild(botDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Auto TTS if enabled
    if (state.ttsEnabled) {
      speakText(data.answer);
    }
  }

  // Form Submission
  chatForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = chatInput.value.trim();
    if (!query) return;

    appendUserMessage(query);
    chatInput.value = "";
    showTypingIndicator();

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: query,
          category: categorySelect?.value || "all",
        }),
      });
      const data = await res.json();
      appendBotMessage(data);
    } catch (err) {
      removeTypingIndicator();
      appendBotMessage({
        answer: "⚠️ **Error connecting to Campus-AI backend.** Please make sure the local server is running.",
        sources: [],
        timestamp: "Now",
      });
    }
  });

  // Clear Chat History
  document.getElementById("clear-chat-btn")?.addEventListener("click", () => {
    const welcome = chatMessages.firstElementChild;
    chatMessages.innerHTML = "";
    if (welcome) chatMessages.appendChild(welcome);
  });

  // Action Button Helpers
  window.copyMessageText = function (btn) {
    const prose = btn.closest(".flex-1")?.querySelector(".chat-prose");
    if (prose) {
      navigator.clipboard.writeText(prose.innerText);
      const originalText = btn.innerHTML;
      btn.innerHTML = `<i class="fa-solid fa-check text-emerald-400"></i> Copied`;
      setTimeout(() => (btn.innerHTML = originalText), 2000);
    }
  };

  window.speakMessageText = function (btn) {
    const prose = btn.closest(".flex-1")?.querySelector(".chat-prose");
    if (prose) {
      speakText(prose.innerText);
    }
  };

  window.toggleHelpful = function (btn) {
    btn.classList.toggle("text-emerald-400");
    btn.innerHTML = btn.classList.contains("text-emerald-400")
      ? `<i class="fa-solid fa-thumbs-up text-emerald-400"></i> Upvoted`
      : `<i class="fa-regular fa-thumbs-up"></i> Helpful`;
  };

  // Speech Recognition (Voice Input)
  const voiceBtn = document.getElementById("voice-input-btn");
  const micIcon = document.getElementById("mic-icon");

  if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    state.recognition = new SpeechRec();
    state.recognition.continuous = false;
    state.recognition.lang = "en-IN";

    state.recognition.onstart = () => {
      state.isRecording = true;
      micIcon.className = "fa-solid fa-microphone-lines text-rose-500 animate-pulse";
    };

    state.recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      if (chatInput) {
        chatInput.value = transcript;
        chatForm?.dispatchEvent(new Event("submit"));
      }
    };

    state.recognition.onend = () => {
      state.isRecording = false;
      micIcon.className = "fa-solid fa-microphone text-[var(--text-muted)]";
    };

    voiceBtn?.addEventListener("click", () => {
      if (state.isRecording) {
        state.recognition.stop();
      } else {
        state.recognition.start();
      }
    });
  } else {
    if (voiceBtn) voiceBtn.style.display = "none";
  }

  // ================= FEE CALCULATOR =================
  const calcProgram = document.getElementById("calc-program");
  const calcHostel = document.getElementById("calc-hostel");
  const calcUniform = document.getElementById("calc-uniform");
  const calcPreEnroll = document.getElementById("calc-pre-enroll");
  const calcBreakdownList = document.getElementById("calc-breakdown-list");
  const calcGrandTotal = document.getElementById("calc-grand-total");

  function updateCalculator() {
    if (!calcBreakdownList || !calcGrandTotal) return;

    const baseFee = parseInt(calcProgram?.value || "181200", 10);
    const hostelFee = parseInt(calcHostel?.value || "0", 10);
    const uniformFee = calcUniform?.checked ? 9900 : 0;
    const preEnrollFee = parseInt(calcPreEnroll?.value || "0", 10);

    const grandTotal = baseFee + hostelFee + uniformFee + preEnrollFee;

    const items = [
      { name: "Academic Tuition & Program Fee", amt: baseFee, badge: "Mandatory" },
      { name: "Hostel Lodging, Boarding & Laundry", amt: hostelFee, badge: hostelFee > 0 ? "Opted" : "None" },
      { name: "Official College Uniform Set", amt: uniformFee, badge: uniformFee > 0 ? "Mandatory" : "Waived" },
      { name: "Direct Admission Pre-Enrollment Charge", amt: preEnrollFee, badge: preEnrollFee > 0 ? "Direct Route" : "Counselling" },
    ];

    calcBreakdownList.innerHTML = items
      .map(
        (i) => `
      <div class="flex items-center justify-between py-1.5 border-b border-[var(--border-subtle)]">
        <div>
          <span class="text-xs text-[var(--text-primary)] font-medium">${i.name}</span>
          <span class="badge-pill bg-white/5 text-[9px] py-0 px-1 ml-1">${i.badge}</span>
        </div>
        <span class="font-bold font-mono ${i.amt > 0 ? "text-emerald-400" : "text-[var(--text-muted)]"}">
          ₹${i.amt.toLocaleString("en-IN")}
        </span>
      </div>
    `
      )
      .join("");

    calcGrandTotal.textContent = `₹${grandTotal.toLocaleString("en-IN")}`;
  }

  [calcProgram, calcHostel, calcUniform, calcPreEnroll].forEach((el) => {
    el?.addEventListener("change", updateCalculator);
  });
  updateCalculator();

  // ================= DATA LOADERS =================
  let programsLoaded = false;
  async function loadPrograms() {
    if (programsLoaded) return;
    try {
      const res = await fetch("/api/programs");
      const list = await res.json();
      const tbody = document.getElementById("programs-tbody");
      if (tbody) {
        tbody.innerHTML = list
          .map(
            (p) => `
          <tr class="hover:bg-white/5 transition">
            <td class="py-2.5 font-bold text-indigo-400">${p.degree}</td>
            <td class="py-2.5 font-medium">${p.name}</td>
            <td class="py-2.5 text-center font-mono font-bold text-emerald-400">${p.intake}</td>
            <td class="py-2.5 text-[var(--text-muted)]">${p.duration}</td>
            <td class="py-2.5 text-[var(--text-secondary)] text-[11px]">${p.entrance}</td>
          </tr>
        `
          )
          .join("");
        programsLoaded = true;
      }
    } catch (e) {
      console.error("Failed to load programs:", e);
    }
  }

  // Program Search Filter
  document.getElementById("program-search")?.addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase();
    document.querySelectorAll("#programs-tbody tr").forEach((row) => {
      row.style.display = row.innerText.toLowerCase().includes(term) ? "" : "none";
    });
  });

  let directoryLoaded = false;
  async function loadDirectory() {
    if (directoryLoaded) return;
    try {
      const res = await fetch("/api/directory");
      const data = await res.json();

      const deansGrid = document.getElementById("deans-grid");
      if (deansGrid) {
        deansGrid.innerHTML = data.deans
          .map(
            (d) => `
          <div class="glass-panel p-4 border-l-4 border-indigo-500">
            <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-400 block">${d.role}</span>
            <h4 class="font-bold text-sm text-white mt-1">${d.name}</h4>
            <a href="mailto:${d.email}" class="text-xs text-emerald-400 hover:underline flex items-center gap-1 mt-2">
              <i class="fa-regular fa-envelope text-[10px]"></i> ${d.email}
            </a>
          </div>
        `
          )
          .join("");
      }

      const hodsGrid = document.getElementById("hods-grid");
      if (hodsGrid) {
        hodsGrid.innerHTML = data.hods
          .map(
            (h) => `
          <div class="glass-panel p-4 border-l-4 border-purple-500">
            <span class="text-[10px] font-bold uppercase tracking-wider text-purple-400 block">${h.dept}</span>
            <h4 class="font-bold text-sm text-white mt-1">${h.name}</h4>
            <a href="mailto:${h.email}" class="text-xs text-emerald-400 hover:underline flex items-center gap-1 mt-2">
              <i class="fa-regular fa-envelope text-[10px]"></i> ${h.email}
            </a>
          </div>
        `
          )
          .join("");
      }
      directoryLoaded = true;
    } catch (e) {
      console.error("Failed to load directory:", e);
    }
  }

  let clubsLoaded = false;
  async function loadClubs() {
    if (clubsLoaded) return;
    try {
      const res = await fetch("/api/clubs");
      const list = await res.json();
      const clubsGrid = document.getElementById("clubs-grid");
      if (clubsGrid) {
        clubsGrid.innerHTML = list
          .map(
            (c) => `
          <div class="glass-panel p-4 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="badge-pill badge-official text-[9px]">${c.category}</span>
                <span class="text-[10px] font-mono text-purple-300 font-bold">${c.intake}</span>
              </div>
              <h4 class="font-bold text-sm text-white mt-2">${c.name}</h4>
              <p class="text-xs text-[var(--text-secondary)] mt-1 leading-relaxed">${c.focus}</p>
            </div>
            <div class="mt-3 pt-2 border-t border-[var(--border-subtle)] text-[10px] text-[var(--text-muted)]">
              <strong class="text-indigo-400">Recruitment:</strong> ${c.recruitment}
            </div>
          </div>
        `
          )
          .join("");
        clubsLoaded = true;
      }
    } catch (e) {
      console.error("Failed to load clubs:", e);
    }
  }

  // ================= GRIEVANCE GENERATOR =================
  const grvForm = document.getElementById("grievance-form");
  const grvOutput = document.getElementById("grievance-output");

  grvForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      name: document.getElementById("grv-name")?.value || "Student",
      department: document.getElementById("grv-dept")?.value || "CSE",
      year: document.getElementById("grv-year")?.value || "1st Year",
      category: document.getElementById("grv-category")?.value || "Academic",
      subject: document.getElementById("grv-subject")?.value || "Grievance",
      details: document.getElementById("grv-details")?.value || "",
    };

    try {
      const res = await fetch("/api/grievance-draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (grvOutput) {
        grvOutput.textContent = data.draft_text;
      }
    } catch (err) {
      alert("Failed to generate draft. Please check server.");
    }
  });

  window.copyGrievanceDraft = function () {
    if (grvOutput) {
      navigator.clipboard.writeText(grvOutput.textContent);
      alert("Official Grievance Draft copied to clipboard!");
    }
  };

  window.printGrievanceDraft = function () {
    if (!grvOutput || !grvOutput.textContent.trim()) return;
    const printWin = window.open("", "_blank");
    printWin.document.write(`
      <html>
        <head>
          <title>Student Grievance Draft — ABESEC</title>
          <style>
            body { font-family: monospace; padding: 40px; line-height: 1.5; white-space: pre-wrap; }
          </style>
        </head>
        <body>${escapeHtml(grvOutput.textContent)}</body>
      </html>
    `);
    printWin.document.close();
    printWin.print();
  };

  // ================= RAG INSPECTOR MODAL =================
  const ragModal = document.getElementById("rag-inspector-modal");
  const toggleRagBtn = document.getElementById("toggle-rag-btn");
  const closeRagBtn = document.getElementById("close-rag-btn");
  const ragSearchInput = document.getElementById("rag-search-input");
  const ragSearchBtn = document.getElementById("rag-search-btn");
  const ragResultsContainer = document.getElementById("rag-results-container");

  toggleRagBtn?.addEventListener("click", () => {
    ragModal?.classList.remove("hidden");
    if (!ragSearchInput.value) {
      ragSearchInput.value = "academic fee structure";
      triggerRagSearch();
    }
  });

  closeRagBtn?.addEventListener("click", () => {
    ragModal?.classList.add("hidden");
  });

  async function triggerRagSearch() {
    const q = ragSearchInput?.value.trim();
    if (!q || !ragResultsContainer) return;

    ragResultsContainer.innerHTML = `<p class="text-center py-4 text-indigo-400">Searching neural index...</p>`;
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
      const chunks = await res.json();
      if (!chunks.length) {
        ragResultsContainer.innerHTML = `<p class="text-center py-4 text-slate-400">No matching chunks found.</p>`;
        return;
      }
      ragResultsContainer.innerHTML = chunks
        .map(
          (c) => `
        <div class="glass-panel p-3 border-l-2 border-indigo-400">
          <div class="flex items-center justify-between text-[11px] mb-1">
            <span class="font-bold text-indigo-300 font-mono">${c.id}</span>
            <div class="flex gap-2">
              <span class="badge-pill badge-year py-0 px-1 text-[9px]">${c.academic_year || "2026-27"}</span>
              <span class="badge-pill badge-official py-0 px-1 text-[9px]">${c.relevance}% Match</span>
            </div>
          </div>
          <h5 class="font-bold text-white text-xs mb-1">${c.title}</h5>
          <p class="text-[11px] text-[var(--text-secondary)] leading-relaxed mb-2">${c.content}</p>
          <a href="${c.source_url}" target="_blank" class="text-[10px] text-emerald-400 hover:underline flex items-center gap-1 font-mono">
            <i class="fa-solid fa-link text-[8px]"></i> ${c.source_url}
          </a>
        </div>
      `
        )
        .join("");
    } catch (e) {
      ragResultsContainer.innerHTML = `<p class="text-center py-4 text-red-400">Failed to query RAG index.</p>`;
    }
  }

  ragSearchBtn?.addEventListener("click", triggerRagSearch);
  ragSearchInput?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") triggerRagSearch();
  });

  // Utilities
  function escapeHtml(text) {
    if (!text) return "";
    return text.replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[m]));
  }
  function escapeAttr(text) {
    if (!text) return "";
    return text.replace(/'/g, "\\'");
  }
});
