"use client";

import Chat from "./components/Chat";

export default function Page() {
  return (
    <main
      style={{
        minHeight: "100vh",
        background: "#f4f6f8",
        padding: "60px 20px",
        fontFamily:
          "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
      }}
    >
      <div
        style={{
          maxWidth: "900px",
          margin: "0 auto",
          background: "white",
          padding: "40px",
          borderRadius: "16px",
          boxShadow: "0 10px 30px rgba(0,0,0,0.08)"
        }}
      >
        <h1
          style={{
            fontSize: "32px",
            fontWeight: 700,
            marginBottom: "8px"
          }}
        >
          Skylark Drones — BI Agent
        </h1>

        <p
          style={{
            color: "#666",
            fontSize: "16px",
            marginBottom: "30px"
          }}
        >
          Founder-level Business Intelligence powered by Monday.com
        </p>

        <Chat />
      </div>

      <footer
        style={{
          textAlign: "center",
          marginTop: "40px",
          fontSize: "14px",
          color: "#888"
        }}
      >
        © {new Date().getFullYear()} Skylark Drones • Business Intelligence Agent
      </footer>
    </main>
  );
}

