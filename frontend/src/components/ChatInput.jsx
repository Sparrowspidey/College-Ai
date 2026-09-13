export default function ChatInput({
  input,
  setInput,
  onSend,
  loading,
  inputRef,
}) {
  function handleSubmit(event) {
    event.preventDefault();
    onSend(input);
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      onSend(input);
    }
  }

  return (
    <footer className="input-area">
      <div className="input-wrapper">
        <form className="input-form" onSubmit={handleSubmit}>
          <textarea
            ref={inputRef}
            className="input-box"
            placeholder="Ask anything about IIIT Kottayam..."
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={loading}
            aria-label="Ask College-AI"
          />

          <button
            type="submit"
            className="send-btn"
            disabled={!input.trim() || loading}
            aria-label="Send message"
          >
            {loading ? (
              <span className="spinner" />
            ) : (
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M5 12h13" />
                <path d="m13 6 6 6-6 6" />
              </svg>
            )}
          </button>
        </form>

        <div className="input-meta">
          <span>Built by students, for students.</span>
          <span className="keyboard-hint">
            <kbd>Enter</kbd> send <kbd>Shift</kbd> + <kbd>Enter</kbd> new line
          </span>
        </div>
      </div>
    </footer>
  );
}
