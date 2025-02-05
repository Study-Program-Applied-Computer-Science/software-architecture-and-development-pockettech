import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./Layout";
import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import NotFound from "./pages/NotFound";
import UserProfile from "./pages/UserProfile";
import CreateUserPage from "./pages/CreateUserPage";

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const userTheme = localStorage.getItem("theme");
    const systemPrefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;

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
    <Router>
      <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch}>
        <Routes>
          <Route path="/" element={<LoginPage isDarkMode={isDarkMode} />} />
          <Route path="/dashboard" element={<Dashboard isDarkMode={isDarkMode} />} />
          <Route path="/profile" element={<UserProfile />} />
          <Route path="/create-user" element={<CreateUserPage />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;
