document.addEventListener("DOMContentLoaded", function () {
  const chatForm = document.getElementById("chat-form");
  const chatMessages = document.getElementById("chat-messages");
  const questionInput = document.getElementById("question");
  const landingView = document.getElementById("landing-view");
  const conversationView = document.getElementById("conversation-view");
  const chatContainer = document.getElementById("chat-container");
  const promptCards = document.querySelectorAll(".prompt-card");
  const refreshPrompts = document.getElementById("refresh-prompts");

  if (!chatForm || !chatMessages || !questionInput) {
    console.error("Required elements not found");
    return;
  }

  // Character counter
  questionInput.addEventListener("input", function () {
    const counter = document.querySelector(".char-counter");
    if (counter) {
      counter.textContent = `${this.value.length}/${this.maxLength}`;
    }
  });

  // Add Enter key support
  questionInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      chatForm.dispatchEvent(new Event("submit", { bubbles: true }));
    }
  });

  // Handle form submission
  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const question = questionInput.value.trim();
    if (!question) return;

    // Hide landing view and show conversation view
    hideInitialContent();

    // Clear input immediately
    questionInput.value = "";
    document.querySelector(
      ".char-counter"
    ).textContent = `0/${questionInput.maxLength}`;
    questionInput.focus();

    // Add user message
    const userMessage = document.createElement("div");
    userMessage.className = "chat-message-user rounded-3 p-3 mb-3 ms-auto";
    userMessage.style.maxWidth = "75%";
    userMessage.textContent = question;
    chatMessages.appendChild(userMessage);

    // Add typing indicator
    const loadingMessage = document.createElement("div");
    loadingMessage.className = "chat-message-bot rounded-3 p-3 mb-3";
    loadingMessage.style.maxWidth = "75%";
    loadingMessage.innerHTML = `
      <div class="d-flex align-items-center">
        <span class="me-2">Thinking</span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>
    `;
    chatMessages.appendChild(loadingMessage);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
      const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;
      const response = await fetch("/ask/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken,
        },
        body: `question=${encodeURIComponent(question)}`,
      });

      const data = await response.json();

      // Remove loading message
      loadingMessage.remove();

      // Add bot response
      const botMessage = document.createElement("div");
      botMessage.className = "chat-message-bot rounded-3 p-3 mb-3";
      botMessage.style.maxWidth = "75%";

      // Format response with paragraphs
      const formattedResponse = data.response
        .split("\n\n")
        .map((paragraph) => {
          if (paragraph.trim()) {
            return `<p class="mb-2">${paragraph.trim()}</p>`;
          }
          return "";
        })
        .join("");

      botMessage.innerHTML =
        formattedResponse || `<p class="mb-0">${data.response}</p>`;
      chatMessages.appendChild(botMessage);
    } catch (error) {
      console.error("Error:", error);
      // Remove loading message
      loadingMessage.remove();

      // Add error message
      const errorMessage = document.createElement("div");
      errorMessage.className = "alert alert-danger rounded-3 p-3 mb-3";
      errorMessage.style.maxWidth = "75%";
      errorMessage.innerHTML =
        "<p class='mb-0'>Sorry, I encountered an error. Please try again.</p>";
      chatMessages.appendChild(errorMessage);
    }

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
  });

  // Helper function to completely hide initial content
  function hideInitialContent() {
    // First check if we've already switched to conversation view
    if (conversationView.classList.contains("d-none")) {
      // If this is the first message, do the complete switch
      landingView.style.display = "none"; // Force hide with inline style
      conversationView.classList.remove("d-none");
      conversationView.classList.add("d-block");
      conversationView.style.backgroundColor = "#fffff"; // Set background color

      // Add welcome message
      const welcomeMessage = document.createElement("div");
      welcomeMessage.className = "chat-message-bot rounded-3 p-3 mb-3";
      welcomeMessage.style.maxWidth = "75%";
      welcomeMessage.innerHTML =
        "<p class='mb-0'>Hello! I'm your legal assistant. How can I help you today?</p>";
      chatMessages.appendChild(welcomeMessage);
    }
  }

  // Helper function to handle the quick question cards
  function sendQuickQuestion(question) {
    questionInput.value = question;
    // Trigger the same logic as the form submission
    const submitEvent = new Event("submit", {
      bubbles: true,
      cancelable: true,
    });
    chatForm.dispatchEvent(submitEvent);
  }

  // Quick prompt cards
  promptCards.forEach((card) => {
    card.addEventListener("click", function () {
      const question = this.getAttribute("data-question");
      if (question) {
        sendQuickQuestion(question);
      }
    });
  });

  // Refresh prompts functionality
  if (refreshPrompts) {
    refreshPrompts.addEventListener("click", function () {
      // You can implement dynamic prompt refreshing here
      console.log("Refresh prompts clicked");
      // For example, you could make an API call to get new prompts
    });
  }
});
