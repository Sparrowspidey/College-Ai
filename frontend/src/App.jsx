import { useState, useRef, useEffect } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const SUGGESTIONS = [
  "What is the fee structure for B.Tech CSE?",
  "Who are the faculty members at IIIT Kottayam?",
  "How do I apply for PhD admission?",
  "What facilities are available in the hostel?",
  "Tell me about placement at IIIT Kottayam",
];

function Message({ msg }) {
  const isUser = msg.role === "user";

  return (
    <div className={`message ${isUser ? "message-user" : "message-bot"}`}>
      {!isUser && (
        <div className="bot-avatar">
          <span>AI</span>
        </div>
      )}
      <div className={`bubble ${isUser ? "bubble-user" : "bubble-bot"}`}>
        <p className="bubble-text">{msg.content}</p>

        {/* Sources */}
        {msg.sources && msg.sources.length > 0 && (
          <div className="sources">
            <p className="sources-label">Sources</p>
            {msg.sources.map((src, i) => (
              <a
                key={i}
                href={src.url || "#"}
                target="_blank"
                rel="noopener noreferrer"
                className="source-item"
              >
                <span className="source-icon">🔗</span>
                <span className="source-text">
                  {src.url || src.source}
                </span>
                <span className="source-score">
                  {(src.score * 100).toFixed(0)}%
                </span>
              </a>
            ))}
          </div>
        )}

        {msg.time_taken && (
          <p className="time-taken">⏱ {msg.time_taken}s</p>
        )}
      </div>
      {isUser && <div className="user-avatar">You</div>}
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="message message-bot">
      <div className="bot-avatar"><span>AI</span></div>
      <div className="bubble bubble-bot typing">
        <span /><span /><span />
      </div>
    </div>
  );
}

export default function App() {
  const [messages, setMessages]   = useState([]);
  const [input, setInput]         = useState("");
  const [loading, setLoading]     = useState(false);
  const [apiStatus, setApiStatus] = useState("checking");
  const bottomRef                 = useRef(null);
  const inputRef                  = useRef(null);

  // Check API health on load
  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((r) => r.json())
      .then(() => setApiStatus("ok"))
      .catch(() => setApiStatus("error"));
  }, []);

  // Auto scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(question) {
    if (!question.trim() || loading) return;

    const userMsg = { role: "user", content: question };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ question, top_k: 5 }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role:       "bot",
          content:    data.answer,
          sources:    data.sources,
          time_taken: data.time_taken,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role:    "bot",
          content: "Sorry, I couldn't reach the server. Make sure the API and Ollama are running.",
        },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    sendMessage(input);
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  }

  const isEmpty = messages.length === 0;

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">🎓</span>
            <div>
              <h1 className="logo-title">College-AI</h1>
              <p className="logo-sub">IIIT Kottayam Assistant</p>
            </div>
          </div>
          <div className={`status-badge status-${apiStatus}`}>
            <span className="status-dot" />
            {apiStatus === "ok"
              ? "API Connected"
              : apiStatus === "checking"
              ? "Connecting..."
              : "API Offline"}
          </div>
        </div>
      </header>

      {/* Chat area */}
      <main className="chat-area">
        {isEmpty ? (
          <div className="empty-state">
            <div className="empty-icon">🎓</div>
            <h2 className="empty-title">Ask me anything about IIIT Kottayam</h2>
            <p className="empty-sub">
              I can answer questions about admissions, courses, faculty,
              facilities, placements, research, and more.
            </p>
            <div className="suggestions">
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  className="suggestion-btn"
                  onClick={() => sendMessage(s)}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="messages">
            {messages.map((msg, i) => (
              <Message key={i} msg={msg} />
            ))}
            {loading && <TypingIndicator />}
            <div ref={bottomRef} />
          </div>
        )}
      </main>

      {/* Input bar */}
      <footer className="input-bar">
        <form className="input-form" onSubmit={handleSubmit}>
          <textarea
            ref={inputRef}
            className="input-box"
            placeholder="Ask about admissions, courses, faculty, placements..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={loading}
          />
          <button
            type="submit"
            className="send-btn"
            disabled={!input.trim() || loading}
          >
            {loading ? (
              <span className="spinner" />
            ) : (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            )}
          </button>
        </form>
        <p className="input-hint">
          Press Enter to send · Shift+Enter for new line
        </p>
      </footer>
    </div>
  );
}
