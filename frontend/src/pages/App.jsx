import React, { useState } from "react";

export default function App() {
  const [role, setRole] = useState("admin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    alert(\`Logging in as \${role} with email: \${email}\`);
    // TODO: Implement actual login call to backend
  };

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#f5f5f5",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: "2rem"
    }}>
      <img src="/wt_logonew_whitecanvas.png" alt="WeTreat Logo" style={{ maxWidth: "200px", marginBottom: "2rem" }} />

      <div style={{ background: "#fff", padding: "2rem", borderRadius: "12px", boxShadow: "0 2px 10px rgba(0,0,0,0.1)", width: "100%", maxWidth: "400px" }}>
        <h2 style={{ textAlign: "center", marginBottom: "1.5rem" }}>Welcome to WeTreat</h2>

        <label>Role:</label>
        <select value={role} onChange={e => setRole(e.target.value)} style={{ width: "100%", marginBottom: "1rem", padding: "0.5rem" }}>
          <option value="admin">Admin</option>
          <option value="patient">Patient Input</option>
          <option value="physician">Consulting Physician</option>
        </select>

        <label>Email:</label>
        <input
          type="email"
          placeholder="Enter email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          style={{ width: "100%", marginBottom: "1rem", padding: "0.5rem" }}
        />

        <label>Password:</label>
        <input
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          style={{ width: "100%", marginBottom: "1.5rem", padding: "0.5rem" }}
        />

        <button
          onClick={handleLogin}
          style={{
            backgroundColor: "#0066cc",
            color: "#fff",
            padding: "0.75rem",
            width: "100%",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer"
          }}
        >
          Login
        </button>
      </div>
    </div>
  );
}
