import React from 'react';
import logo from './assets/logo.png';

const App = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-white text-gray-800">
      <img src={logo} alt="WeTreat Logo" className="w-24 mb-6" />
      <h1 className="text-2xl font-semibold mb-4">Welcome to WeTreat</h1>
      <p className="text-lg mb-6">Please choose your role to continue:</p>
      <div className="space-x-4">
        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Admin</button>
        <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Physician</button>
        <button className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">Patient Input</button>
      </div>
    </div>
  );
};

export default App;
