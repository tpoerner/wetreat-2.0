import React from 'react';
import logo from './assets/logo.png';

export default function App() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#fff',
      color: '#1f2937',
      padding: '1rem'
    }}>
      {/* Force the logo to 64px width no matter what */}
      <img src={logo} alt="WeTreat Logo" style={{ width: 64, height: 'auto', marginBottom: 16 }} />

      <h1 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: 8 }}>Welcome to WeTreat</h1>
      <p style={{ fontSize: '1rem', color: '#6b7280', marginBottom: 24 }}>
        Please choose your role to continue:
      </p>

      <div style={{ display: 'flex', gap: 12 }}>
        <button style={btn('#2563eb')}>Admin</button>
        <button style={btn('#16a34a')}>Physician</button>
        <button style={btn('#4b5563')}>Patient Input</button>
      </div>
    </div>
  );
}

function btn(bg) {
  return {
    background: bg,
    color: '#fff',
    padding: '0.5rem 1rem',
    borderRadius: 10,
    border: 'none',
    cursor: 'pointer',
    boxShadow: '0 2px 6px rgba(0,0,0,0.15)'
  };
}
