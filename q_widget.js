// q_widget.js
// Floating AI widget "Q" – vanilla JS, no dependencies.
// When included on any page, it injects a floating Q button and a small chat panel.

(function () {
  // === CONFIGURATION =======================================================
  // Replace this with your backend AI endpoint.
  // For now it's a placeholder; you can point it to your Render service.
  const API_URL = "/api/chat"; // e.g. "https://your-render-service.onrender.com/chat"

  // If your endpoint needs authentication, handle it server-side.
  // Do NOT hard-code secrets here in production.

  // === STYLES ==============================================================
  const style = document.createElement("style");
  style.innerHTML = `
    #q-widget-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 999999;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    #q-widget-button {
      width: 52px;
      height: 52px;
      border-radius: 9999px;
      border: none;
      cursor: pointer;
      font-weight: 700;
      font-size: 20px;
      background: linear-gradient(135deg, #111827, #1f2933);
      color: #f9fafb;
      box-shadow: 0 10px 20px rgba(15, 23, 42, 0.35);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.2s ease;
    }

    #q-widget-button:hover {
      transform: translateY(-1px);
      box-shadow: 0 14px 30px rgba(15, 23, 42, 0.45);
      background: linear-gradient(135deg, #020617, #111827);
    }

    #q-widget-button:active {
      transform: translateY(0);
      box-shadow: 0 8px 15px rgba(15, 23, 42, 0.3);
    }

    #q-chat-window {
      position: fixed;
      bottom: 90px;
      right: 24px;
      width: 340px;
      max-height: 480px;
      background: #0b1120;
      color: #e5e7eb;
      border-radius: 18px;
      box-shadow: 0 18px 45px rgba(15, 23, 42, 0.85);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      opacity: 0;
      pointer-events: none;
      transform: translateY(8px);
      transition: opacity 0.18s ease, transform 0.18s ease;
      z-index: 999998;
    }

    #q-chat-window.q-open {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }

    #q-chat-header {
      padding: 10px 14px;
      background: radial-gradient(circle at top left, #1f2937, #020617);
      border-bottom: 1px solid rgba(55, 65, 81, 0.8);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    #q-chat-header-left {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    #q-header-avatar {
      width: 26px;
      height: 26px;
      border-radius: 9999px;
      background: linear-gradient(135deg, #14b8a6, #22c55e);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      font-weight: 800;
      color: #020617;
    }

    #q-header-title {
      display: flex;
      flex-direction: column;
    }

    #q-header-title span:first-child {
      font-size: 13px;
      font-weight: 600;
    }

    #q-header-title span:last-child {
      font-size: 11px;
      color: #9ca3af;
    }

    #q-chat-close {
      background: transparent;
      border: none;
      color: #9ca3af;
      cursor: pointer;
      font-size: 18px;
      line-height: 1;
      padding: 4px;
      border-radius: 9999px;
      transition: background 0.15s ease, color 0.15s ease;
    }

    #q-chat-close:hover {
      background: rgba(148, 163, 184, 0.15);
      color: #e5e7eb;
    }

    #q-chat-messages {
      flex: 1;
      padding: 10px 12px 6px;
      overflow-y: auto;
      font-size: 13px;
      scrollbar-width: thin;
      scrollbar-color: rgba(75, 85, 99, 0.9) transparent;
    }

    #q-chat-messages::-webkit-scrollbar {
      width: 6px;
    }

    #q-chat-messages::-webkit-scrollbar-track {
      background: transparent;
    }

    #q-chat-messages::-webkit-scrollbar-thumb {
      background-color: rgba(75, 85, 99, 0.9);
      border-radius: 9999px;
    }

    .q-message-row {
      margin-bottom: 8px;
      display: flex;
    }

    .q-message-row.q-user {
      justify-content: flex-end;
    }

    .q-message-row.q-assistant {
      justify-content: flex-start;
    }

    .q-message {
      max-width: 74%;
      padding: 7px 9px;
      border-radius: 12px;
      line-height: 1.35;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    .q-message.q-user-bubble {
      background: linear-gradient(135deg, #22c55e, #15803d);
      color: #022c22;
      border-bottom-right-radius: 4px;
      font-weight: 500;
    }

    .q-message.q-assistant-bubble {
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(75, 85, 99, 0.8);
      border-bottom-left-radius: 4px;
      color: #e5e7eb;
    }

    #q-chat-input-area {
      border-top: 1px solid rgba(55, 65, 81, 0.75);
      padding: 8px 9px;
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(2, 6, 23, 0.96);
    }

    #q-chat-input {
      flex: 1;
      resize: none;
      border-radius: 9999px;
      border: 1px solid rgba(55, 65, 81, 0.9);
      background: rgba(15, 23, 42, 0.9);
      color: #e5e7eb;
      font-size: 12px;
      padding: 8px 10px;
      outline: none;
      max-height: 72px;
    }

    #q-chat-input::placeholder {
      color: #6b7280;
    }

    #q-chat-input:focus {
      border-color: #22c55e;
      box-shadow: 0 0 0 1px rgba(34, 197, 94, 0.4);
    }

    #q-send-button {
      border-radius: 9999px;
      border: none;
      padding: 7px 10px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      background: linear-gradient(135deg, #22c55e, #14b8a6);
      color: #022c22;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: transform 0.15s ease, box-shadow 0.15s ease, opacity 0.15s ease;
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }

    #q-send-button:disabled {
      opacity: 0.5;
      cursor: default;
      box-shadow: none;
      transform: none;
    }

    #q-send-button:not(:disabled):hover {
      transform: translateY(-0.5px);
      box-shadow: 0 6px 16px rgba(16, 185, 129, 0.55);
    }

    #q-send-button:not(:disabled):active {
      transform: translateY(0);
      box-shadow: 0 3px 9px rgba(16, 185, 129, 0.45);
    }

    #q-status-text {
      font-size: 10px;
      color: #6b7280;
      margin-left: 2px;
    }
  `;
  document.head.appendChild(style);

  // === DOM CREATION ========================================================
  const container = document.createElement("div");
  container.id = "q-widget-container";

  const button = document.createElement("button");
  button.id = "q-widget-button";
  button.setAttribute("type", "button");
  button.textContent = "Q";

  const chatWindow = document.createElement("div");
  chatWindow.id = "q-chat-window";

  const header = document.createElement("div");
  header.id = "q-chat-header";

  const headerLeft = document.createElement("div");
  headerLeft.id = "q-chat-header-left";

  const avatar = document.createElement("div");
  avatar.id = "q-header-avatar";
  avatar.textContent = "Q";

  const title = document.createElement("div");
  title.id = "q-header-title";

  const titleLine1 = document.createElement("span");
  titleLine1.textContent = "Quantum Assistant";

  const titleLine2 = document.createElement("span");
  titleLine2.textContent = "Ask Q about your plan.";

  title.appendChild(titleLine1);
  title.appendChild(titleLine2);

  headerLeft.appendChild(avatar);
  headerLeft.appendChild(title);

  const closeBtn = document.createElement("button");
  closeBtn.id = "q-chat-close";
  closeBtn.setAttribute("type", "button");
  closeBtn.innerHTML = "&times;";

  header.appendChild(headerLeft);
  header.appendChild(closeBtn);

  const messages = document.createElement("div");
  messages.id = "q-chat-messages";

  const inputArea = document.createElement("div");
  inputArea.id = "q-chat-input-area";

  const input = document.createElement("textarea");
  input.id = "q-chat-input";
  input.rows = 1;
  input.placeholder = "Ask Q anything about this plan…";

  const sendButton = document.createElement("button");
  sendButton.id = "q-send-button";
  sendButton.setAttribute("type", "button");
  sendButton.textContent = "Send";

  const status = document.createElement("div");
  status.id = "q-status-text";
  status.textContent = "";

  inputArea.appendChild(input);
  inputArea.appendChild(sendButton);

  chatWindow.appendChild(header);
  chatWindow.appendChild(messages);
  chatWindow.appendChild(inputArea);
  chatWindow.appendChild(status);

  container.appendChild(button);
  container.appendChild(chatWindow);
  document.body.appendChild(container);

  // === BEHAVIOR ============================================================
  let isOpen = false;
  let isSending = false;

  function toggleChat(open) {
    isOpen = typeof open === "boolean" ? open : !isOpen;
    if (isOpen) {
      chatWindow.classList.add("q-open");
      setTimeout(() => {
        input.focus();
      }, 100);
    } else {
      chatWindow.classList.remove("q-open");
    }
  }

  function appendMessage(text, role) {
    const row = document.createElement("div");
    row.className = "q-message-row " + (role === "user" ? "q-user" : "q-assistant");
    const bubble = document.createElement("div");
    bubble.className =
      "q-message " +
      (role === "user" ? "q-user-bubble" : "q-assistant-bubble");
    bubble.textContent = text;
    row.appendChild(bubble);
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
  }

  function setStatus(text) {
    status.textContent = text || "";
  }

  async function sendMessage() {
    const content = input.value.trim();
    if (!content || isSending) return;

    appendMessage(content, "user");
    input.value = "";
    input.style.height = "auto";
    isSending = true;
    sendButton.disabled = true;
    setStatus("Thinking…");

    try {
      // Basic JSON chat schema; adjust to match your backend.
      const body = {
        message: content
      };

      const resp = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
      });

      if (!resp.ok) {
        throw new Error("HTTP " + resp.status);
      }

      const data = await resp.json();
      // Expect data.reply or similar; adjust to match your API.
      const reply =
        (data && (data.reply || data.answer || data.message)) ||
        "Q received your message, but the server did not return text.";

      appendMessage(reply, "assistant");
      setStatus("");
    } catch (err) {
      console.error("Q widget error:", err);
      appendMessage("There was a problem talking to Q's brain. Please try again.", "assistant");
      setStatus("Error. Check console / backend.");
    } finally {
      isSending = false;
      sendButton.disabled = false;
    }
  }

  // Initial assistant welcome message
  appendMessage(
    "Hi, I’m Q. I can help interpret this Quantum plan, explain slides, and summarize scenarios.",
    "assistant"
  );

  // === EVENT LISTENERS =====================================================
  button.addEventListener("click", function () {
    toggleChat();
  });

  closeBtn.addEventListener("click", function () {
    toggleChat(false);
  });

  sendButton.addEventListener("click", function () {
    sendMessage();
  });

  input.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });

  input.addEventListener("input", function () {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 72) + "px";
  });
})();
