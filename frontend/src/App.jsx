import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Provider, useSelector, useDispatch } from "react-redux";
import { store } from "./redux/store";
import { verifyUser } from "./redux/authSlice";
import Layout from "./Layout";
import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import NotFound from "./pages/NotFound";

const ProtectedRoute = ({ children }) => {
  const { user, token } = useSelector((state) => state.auth);
  if (!user && !token) {
    return <Navigate to="/" />;
  }
  return children;
};

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(verifyUser());
    const userTheme = localStorage.getItem("theme");
    const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    if (userTheme === "dark" || (!userTheme && systemPrefersDark)) {
      setIsDarkMode(true);
      document.documentElement.classList.add("dark");
    } else {
      setIsDarkMode(false);
      document.documentElement.classList.remove("dark");
    }
  }, [dispatch]);

  const themeSwitch = () => {
    const newTheme = isDarkMode ? "light" : "dark";
    setIsDarkMode(!isDarkMode);
    document.documentElement.classList.toggle("dark", !isDarkMode);
    localStorage.setItem("theme", newTheme);
  };

  return (
    <Provider store={store}>
      <Router>
        <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch}>
          <Routes>
            <Route path="/" element={<LoginPage isDarkMode={isDarkMode} />} />
            <Route path="/dashboard" element={<ProtectedRoute><Dashboard isDarkMode={isDarkMode} /></ProtectedRoute>} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Layout>
      </Router>
    </Provider>
  );
};

export default App;
