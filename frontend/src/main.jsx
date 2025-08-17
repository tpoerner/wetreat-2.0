import React from 'react'
import ReactDOM from 'react-dom/client'

const App = () => (
  <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 text-gray-800">
    <h1 className="text-4xl font-bold mb-4">WeTreat Platform</h1>
    <p className="text-lg">Welcome! Select your role to continue.</p>
    <div className="mt-6 space-x-4">
      <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Admin</button>
      <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Physician</button>
      <button className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">Patient Input</button>
    </div>
  </div>
)

ReactDOM.createRoot(document.getElementById('root')).render(<App />)

