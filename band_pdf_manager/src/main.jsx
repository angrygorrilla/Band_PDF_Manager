import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Auth0Provider } from '@auth0/auth0-react'
import './index.css'
import App from './App.jsx'


createRoot(document.getElementById('root')).render(
  <StrictMode>
  <Auth0Provider
    domain="dev-j3w5kkcgno5ahh5s.us.auth0.com"
    clientId="YwcVOEnJAUc9DaNgzIPFHWlfto0wSVbC"
    
    authorizationParams={{
      redirect_uri: window.location.origin,
      audience: "https://dev-j3w5kkcgno5ahh5s.us.auth0.com/api/v2/",
      //scope: "read:current_user update:current_user_metadata"
    }}
  >
    <App />
  </Auth0Provider>
  </StrictMode>
)