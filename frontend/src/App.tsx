import { useState } from 'react'
import './App.css'
import LoginWithDiscord from './components/login/LoginWithDiscord'

function App() {

  return (
    <>
      <div>
        <p>Logo Area</p>
      </div>
      <LoginWithDiscord />
      <div className="discord-login">
        <button>Login with Discord</button>
      </div>              
    </>
  )
}

export default App
