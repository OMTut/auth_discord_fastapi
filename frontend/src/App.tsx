import './App.css'
import LoginWithDiscord from './components/login/LoginWithDiscord'
import { useAuth } from './hooks'

function App() {
  const { isAuthenticated, user, loading, error, logout } = useAuth()

  if (loading) {
    return (
      <>
        <div>
          <p>Logo Area</p>
        </div>
        <div>
          <p>Loading...</p>
        </div>
      </>
    )
  }

  if (error) {
    console.error('Auth error:', error)
  }

  return (
    <>
      <div>
        <p>Logo Area</p>
      </div>
      {isAuthenticated ? (
        <div>
          <p>Session Found.</p>
          {user && (
            <div>
              <p>Welcome, {user.discord_username}!</p>
              <button onClick={logout}>Logout</button>
            </div>
          )}
        </div>
      ) : (
        <LoginWithDiscord />
      )}
    </>
  )
}

export default App
