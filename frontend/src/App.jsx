import React from 'react';
import { useNavigate } from 'react-router-dom';
import logo from './assets/logo.png';

export default function App() {
  const navigate = useNavigate();
  return (
    <div style={{minHeight:'100vh',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',padding:'1rem'}}>
      <img src={logo} alt="WeTreat Logo" style={{ width: 64, marginBottom: 16 }} />
      <h1 style={{ fontSize: '1.5rem', marginBottom: 8 }}>Welcome to WeTreat</h1>
      <p style={{ fontSize: '1rem', marginBottom: 24 }}>Please choose your role to continue:</p>
      <div style={{ display: 'flex', gap: 12 }}>
        <button onClick={() => navigate('/admin-login')} style={btn('#2563eb')}>Admin</button>
        <button onClick={() => navigate('/physician-login')} style={btn('#16a34a')}>Physician</button>
        <button onClick={() => navigate('/input')} style={btn('#4b5563')}>Patient Input</button>
      </div>
    </div>
  );
}

const btn = (bg) => ({
  background: bg,
  color: '#fff',
  padding: '0.5rem 1rem',
  borderRadius: 10,
  border: 'none',
  cursor: 'pointer'
});
