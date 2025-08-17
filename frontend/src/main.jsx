import React from 'react';
import ReactDOM from 'react-dom/client';

const App = () => {
  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h1 style={{ fontSize: '2rem', color: '#333' }}>✅ WeTreat Frontend is Working!</h1>
      <p style={{ color: '#666' }}>If you see this message, React is alive.</p>
    </div>
  );
};

const root = document.getElementById('root');
if (root) {
  ReactDOM.createRoot(root).render(<App />);
} else {
  console.error('❌ Could not find #root in index.html');
}
