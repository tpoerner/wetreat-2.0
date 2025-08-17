import React, { useState } from 'react';

export default function PhysicianLogin() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  return (
    <div style={{ padding: '2rem', maxWidth: 400, margin: 'auto', textAlign: 'center' }}>
      <h2 style={{ fontSize: '1.5rem', marginBottom: 20 }}>Physician Login</h2>
      <input style={inputStyle} type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input style={inputStyle} type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
      <button style={{...buttonStyle, background: '#16a34a'}}>Login</button>
    </div>
  );
}

const inputStyle = { width: '100%', padding: 10, marginBottom: 10 };
const buttonStyle = { padding: 10, color: '#fff', border: 'none', borderRadius: 8, width: '100%' };
