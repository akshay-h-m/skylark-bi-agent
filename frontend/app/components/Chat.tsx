"use client";

import { useState, useRef, useEffect } from "react";

export default function Chat() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await fetch(
        process.env.NEXT_PUBLIC_BACKEND_URL + "/chat",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: input })
        }
      );

      const data = await res.json();

      const botMessage = { role: "assistant", content: data.response };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: "assistant", content: "Error connecting to backend." }
      ]);
    }

    setInput("");
    setLoading(false);
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div style={{ marginTop: 20 }}>
      <div
        style={{
          height: "400px",
          overflowY: "auto",
          border: "1px solid #ddd",
          padding: 15,
          borderRadius: 10,
          background: "#fafafa"
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              marginBottom: 15,
              textAlign: msg.role === "user" ? "right" : "left"
            }}
          >
            <div
              style={{
                display: "inline-block",
                padding: "10px 14px",
                borderRadius: 12,
                background:
                  msg.role === "user" ? "#000" : "#e5e5e5",
                color: msg.role === "user" ? "#fff" : "#000",
                maxWidth: "80%",
                whiteSpace: "pre-wrap",
		fontFamily: "system-ui, -apple-system, sans-serif",
		lineHeight: 1.5
              }}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
  <div
    style={{
      marginBottom: 15,
      textAlign: "left"
    }}
  >
    <div
      style={{
        display: "inline-block",
        padding: "10px 14px",
        borderRadius: 12,
        background: "#e5e5e5",
        color: "#000",
        maxWidth: "80%",
        fontFamily: "system-ui, -apple-system, sans-serif",
        lineHeight: 1.5
      }}
    >
      Analyzing business metrics...
    </div>
  </div>
)}

        <div ref={chatEndRef} />
      </div>

      <div style={{ display: "flex", marginTop: 10 }}>
        <input
          type="text"
          value={input}
          placeholder="Ask a business question..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          style={{
            flex: 1,
            padding: 10,
            borderRadius: 8,
            border: "1px solid #ccc"
          }}
        />
        <button
          onClick={sendMessage}
          style={{
            marginLeft: 10,
            padding: "10px 20px",
            background: "black",
            color: "white",
            border: "none",
            borderRadius: 8
          }}
        >
          Ask
        </button>
      </div>
    </div>
  );
}

