import React, { useState } from 'react';

export default function PatientInput() {
  const [form, setForm] = useState({
    name: '', dob: '', email: '',
    symptoms: '', history: '', medication: '', notes: ''
  });

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = () => {
    console.log("Submitted patient:", form);
  };

  return (
    <div style={{ padding: '2rem', maxWidth: 600, margin: 'auto' }}>
      <h2 style={{ fontSize: '1.5rem', marginBottom: 20 }}>Patient Intake Form</h2>
      {Object.keys(form).map(key => (
        <input
          key={key}
          name={key}
          value={form[key]}
          onChange={update}
          placeholder={key.charAt(0).toUpperCase() + key.slice(1)}
          style={{ width: '100%', padding: 10, marginBottom: 10 }}
        />
      ))}
      <button style={{ padding: 10, background: '#4b5563', color: '#fff', border: 'none', borderRadius: 8 }} onClick={handleSubmit}>
        Submit
      </button>
    </div>
  );
}
