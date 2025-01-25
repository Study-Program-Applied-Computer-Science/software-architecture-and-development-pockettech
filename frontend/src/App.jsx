import React, { useState, useEffect } from "react";
import Header from "./components/Header";
import LoginPage from "./pages/LoginPage";

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const userTheme = localStorage.getItem('theme');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

  const themeCheck = () => {
    if (userTheme === 'dark' || (!userTheme && systemTheme === 'dark')) {
      setIsDarkMode(true);
      document.documentElement.classList.add('dark');
    } else {
      setIsDarkMode(false);
      document.documentElement.classList.remove('dark');
    }
  };

  const themeSwitch = () => {
    const newTheme = isDarkMode ? 'light' : 'dark';
    localStorage.setItem('theme', newTheme);
    setIsDarkMode(!isDarkMode);
    document.documentElement.classList.toggle('dark');
  };

  useEffect(() => {
    themeCheck();
  }, []);

  return (
    <div>
      <Header isDarkMode={isDarkMode} themeSwitch={themeSwitch} />
      <LoginPage isDarkMode={isDarkMode} themeSwitch={themeSwitch} />
    </div>
  );
};

export default App;
