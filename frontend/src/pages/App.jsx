import React, { useState } from 'react';
import logo from '../../public/wt_logonew_whitecanvas.png';

const App = () => {
  const [role, setRole] = useState('');
  const [email, setEmail] = useState('');

  const handleLogin = () => {
    alert(`Logging in as ${role} with email: ${email}`);
    // TODO: Implement actual login call to backend
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <img src={logo} alt="WeTreat Logo" style={{ width: '200px', marginBottom: '20px' }} />
      <h1>Welcome to WeTreat</h1>
      <div style={{ margin: '20px' }}>
        <select value={role} onChange={(e) => setRole(e.target.value)} style={{ padding: '10px', fontSize: '16px' }}>
          <option value="" disabled>Your role</option>
          <option value="Patient Input">Patient Input</option>
          <option value="Medical Consultation">Medical Consultation</option>
          <option value="Admin Tasks">Admin Tasks</option>
        </select>
      </div>
      <div style={{ margin: '20px' }}>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ padding: '10px', fontSize: '16px', width: '250px' }}
        />
      </div>
      <button onClick={handleLogin} style={{ padding: '10px 20px', fontSize: '16px' }}>
        Login
      </button>
    </div>
  );
};

export default App;