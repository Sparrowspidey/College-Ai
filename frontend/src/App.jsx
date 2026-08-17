import { useState, useRef, useEffect } from "react";
import "./App.css";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import WelcomeScreen from "./components/WelcomeScreen";
import Message from "./components/Message";
import TypingIndicator from "./components/TypingIndicator";
import ChatInput from "./components/ChatInput";
import FloatingBackground from "./components/FloatingBackground";
import CampusRandomizer from "./components/CampusRandomizer";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState("checking");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((response) => {
        if (!response.ok) throw new Error("Health check failed");
        return response.json();
      })
      .then(() => setApiStatus("ok"))
      .catch(() => setApiStatus("error"));
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(question) {
    const cleanQuestion = question.trim();

    if (!cleanQuestion || loading) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: cleanQuestion },
    ]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: cleanQuestion,
          top_k: 5,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: data.answer,
          sources: data.sources || [],
          time_taken: data.time_taken,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content:
            "I couldn't reach the College-AI server. Please make sure the FastAPI backend and Ollama are running.",
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  function startNewChat() {
    setMessages([]);
    setInput("");
    setSidebarOpen(false);
    setTimeout(() => inputRef.current?.focus(), 50);
  }

  const isEmpty = messages.length === 0;

  return (
    <div className="app-shell">
      <FloatingBackground />

      <Sidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onNewChat={startNewChat}
        hasMessages={!isEmpty}
      />

      <div className="app-main">
        <Header
          apiStatus={apiStatus}
          onMenu={() => setSidebarOpen(true)}
        />

        <main className="chat-area">
  {isEmpty ? (
    <>
      <WelcomeScreen onSuggestion={sendMessage} />
      <CampusRandomizer />
    </>
  ) : (
            <div className="messages">
              {messages.map((message, index) => (
                <Message key={`${message.role}-${index}`} msg={message} />
              ))}

              {loading && <TypingIndicator />}

              <div ref={bottomRef} />
            </div>
          )}
        </main>

        <ChatInput
          input={input}
          setInput={setInput}
          onSend={sendMessage}
          loading={loading}
          inputRef={inputRef}
        />
      </div>
    </div>
  );
}
