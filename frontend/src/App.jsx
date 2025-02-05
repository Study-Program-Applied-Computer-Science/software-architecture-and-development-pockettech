import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Provider } from "react-redux";
import { store } from "./redux/store";
import Layout from "./Layout";
import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import NotFound from "./pages/NotFound";

const ProtectedRoute = ({ children }) => {
  // ... your protected route logic here
  return children;
};

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const userTheme = localStorage.getItem("theme");
    const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    if (userTheme === "dark" || (!userTheme && systemPrefersDark)) {
      setIsDarkMode(true);
      document.documentElement.classList.add("dark");
    } else {
      setIsDarkMode(false);
      document.documentElement.classList.remove("dark");
    }
  }, []);

  const themeSwitch = () => {
    const newTheme = isDarkMode ? "light" : "dark";
    setIsDarkMode(!isDarkMode);
    document.documentElement.classList.toggle("dark", !isDarkMode);
    localStorage.setItem("theme", newTheme);
  };

  return (
    <Provider store={store}>
      <Router>
        <Routes>
          {/* For login, use a layout that doesn't show the sidebar */}
          <Route 
            path="/" 
            element={
              <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={false}>
                <LoginPage isDarkMode={isDarkMode} />
              </Layout>
            } 
          />
          {/* For dashboard, show the sidebar */}
          <Route 
            path="/dashboard" 
            element={
              <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={true}>
                <ProtectedRoute>
                  <Dashboard isDarkMode={isDarkMode} />
                </ProtectedRoute>
              </Layout>
            } 
          />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </Provider>
  );
};

export default App;
