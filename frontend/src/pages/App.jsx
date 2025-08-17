
import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [role, setRole] = useState("Patient");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/auth/login`, {
        email,
        password,
      });
      alert(`Logged in as ${role}`);
    } catch (error) {
      console.error("Login failed:", error);
      alert("Login failed.");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>Welcome to We Treat Medical Consultation Platform</h1>
      <p>Please select your role:</p>
      <select value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="Patient">Patient</option>
        <option value="Admin">Admin</option>
        <option value="Consulting Physician">Consulting Physician</option>
      </select>
      <br /><br />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ padding: "10px", width: "250px" }}
      />
      <br /><br />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ padding: "10px", width: "250px" }}
      />
      <br /><br />
      <button onClick={handleLogin} style={{ padding: "10px 20px" }}>
        Login
      </button>
    </div>
  );
};

export default App;
