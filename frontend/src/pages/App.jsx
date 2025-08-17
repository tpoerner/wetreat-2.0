import React, { useState } from "react";

const App = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async () => {
    try {
      const response = await fetch("https://wetreat-2.0.up.railway.app/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        setMessage(`Login successful! Welcome, ${role}.`);
      } else {
        setMessage("Login failed. Please check your credentials.");
      }
    } catch (error) {
      setMessage("Network error.");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "2rem", fontFamily: "Arial" }}>
      <h1>Welcome to We Treat Medical Consultation Platform</h1>
      <p>Please select your role and log in.</p>
      <div style={{ marginBottom: "1rem" }}>
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="">Your Role</option>
          <option value="patient">Patient Input</option>
          <option value="admin">Admin</option>
          <option value="doctor">Medical Consultation</option>
        </select>
      </div>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ marginBottom: "0.5rem", display: "block", margin: "auto" }}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ marginBottom: "1rem", display: "block", margin: "auto" }}
      />
      <button onClick={handleLogin}>Login</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default App;