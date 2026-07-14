function ChatMessage({ sender, text }) {
  return (
    <div
      style={{
        marginBottom: "10px",
        textAlign: sender === "user" ? "right" : "left",
      }}
    >
      <div
        style={{
          display: "inline-block",
          padding: "10px",
          borderRadius: "8px",
          background: sender === "user" ? "#1976d2" : "#f1f1f1",
          color: sender === "user" ? "#fff" : "#000",
          maxWidth: "80%",
        }}
      >
        {text}
      </div>
    </div>
  );
}

export default ChatMessage;