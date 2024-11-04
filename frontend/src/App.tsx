import React from 'react';
import './App.scss';
import { Navigate, Route, Routes } from 'react-router-dom';
import ChatDashboard from './components/chatDashboard/chatDashboard';
import LoginPage from './components/LoginPage/LoginPage';

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);
  React.useEffect(() => {
    const bodyElement = document.body;
    bodyElement.className = 'carbon-theme--g100';
    const authCredentials = localStorage.getItem('authCredentials');
    if (authCredentials) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false); 
    }
  }, []);

  return (
    <Routes>
      <Route
        path=""
        element={
          isAuthenticated ? (
            <Navigate to="/chat-dashboard" replace />
          ) : (
            <Navigate to="/sign-in" replace />
          )
        }
      />
      <Route path="/sign-in" element={<LoginPage />} />
      <Route path="/chat-dashboard" element={<ChatDashboard />} />
      <Route
        path="*"
        element={
          <Navigate
            to={isAuthenticated ? '/chat-dashboard' : '/sign-in'}
            replace
          />
        }
      />
    </Routes>
  );
}

export default App;
