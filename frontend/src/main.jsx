import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App.jsx';
import AdminLogin from './pages/AdminLogin.jsx';
import PhysicianLogin from './pages/PhysicianLogin.jsx';
import PatientInput from './pages/PatientInput.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/admin-login" element={<AdminLogin />} />
        <Route path="/physician-login" element={<PhysicianLogin />} />
        <Route path="/input" element={<PatientInput />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
