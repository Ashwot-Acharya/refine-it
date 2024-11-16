import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';

import './App.css'
import Dashboard from './Dashboard'
import RefineItLandingPage from './RefineItLandingPage';
import PaperFInder from './PaperFInder';

function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <Router>
      <Routes>
        <Route path="/" element={<RefineItLandingPage/>} />

        
        <Route path="/dashboard" element={<Dashboard />} />{/*access only when auth */}
        <Route path="/finder" element={<PaperFInder />} />{/*access only when auth */}
      </Routes>
    </Router>

    </div>
  )
}

export default App
