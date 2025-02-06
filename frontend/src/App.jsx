import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./Layout";
import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import UserProfile from "./pages/UserProfile";
import CreateUserPage from "./pages/CreateUserPage";
import NotFound from "./pages/NotFound";

import BudgetOverviewPage from "./pages/BudgetOverviewPage";
import CreateBudgetPage from "./pages/CreateBudgetPage";
import EditBudgetPage from "./pages/EditBudgetPage";
import ExpenseList from "./pages/ExpenseList";
import ExpenseForm from "./pages/ExpenseForm";
import ExpenseView from "./pages/ExpenseView";

const ProtectedRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem("user_id") !== null;
  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  return children;
};

import CreateGroupPage from "./pages/CreateGroupPage";
import GroupParticipantsPage from "./pages/GroupParticipantsPage";
import SharedTransactionsPage from "./pages/SharedTransactionsPage";
import CreateSharedTransactionPage from "./pages/CreateSharedTransactionPage";


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
    <Router>

      <Routes>
        {/* Public Routes - No Sidebar */}
        <Route 
          path="/" 
          element={
            <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={false}>
              <LoginPage isDarkMode={isDarkMode} />
            </Layout>
          }
        />
        <Route 
          path="/create-user" 
          element={
            <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={false}>
              <CreateUserPage />
            </Layout>
          }
        />
        
        {/* Protected Routes - With Sidebar */}
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
        <Route
          path="/ExpenseList"
          element={
            <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={true}>
              <ProtectedRoute>
                <ExpenseList isDarkMode={isDarkMode} />
              </ProtectedRoute>
            </Layout>
          }
        />
        <Route
          path="/ExpenseForm"
          element={
            <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={true}>
              <ProtectedRoute>
                <ExpenseForm isDarkMode={isDarkMode} />
              </ProtectedRoute>
            </Layout>
          }
        />
        <Route
          path="/ExpenseView"
          element={
            <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={true}>
              <ProtectedRoute>
                <ExpenseView isDarkMode={isDarkMode} />
              </ProtectedRoute>
            </Layout>
          }
        />
        <Route
          path="/profile"
          element={
            <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={true}>
              <ProtectedRoute>
                <UserProfile />
              </ProtectedRoute>
            </Layout>
          }
        />
        <Route
          path="/budget"
          element={
            <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={true}>
              <ProtectedRoute>
                <BudgetOverviewPage isDarkMode={isDarkMode} />
              </ProtectedRoute>
            </Layout>
          }
        />
        <Route
          path="/budget/create"
          element={
            <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={true}>
              <ProtectedRoute>
                <CreateBudgetPage isDarkMode={isDarkMode} />
              </ProtectedRoute>
            </Layout>
          }
        />
        <Route
          path="/budget/edit/:budgetId"
          element={
            <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={true}>
              <ProtectedRoute>
                <EditBudgetPage isDarkMode={isDarkMode} />
              </ProtectedRoute>
            </Layout>
          }
        />
        
        {/* Catch-All */}
          <Route path="/expenses" element={<ExpenseList isDarkMode={isDarkMode}/>} />
          <Route path="/expenses/new" element={<ExpenseForm isDarkMode={isDarkMode}/>} />
          <Route path="/expenses/edit/:expenseId" element={<ExpenseForm isDarkMode={isDarkMode}/>} />
          <Route path="/expenses/:expenseId" element={<ExpenseView isDarkMode={isDarkMode}/>} />
        <Route path="*" element={<NotFound />} />
      </Routes>

      <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch}>
        <Routes>
          <Route path="/" element={<LoginPage isDarkMode={isDarkMode} />} />
          <Route path="/dashboard" element={<Dashboard isDarkMode={isDarkMode} />} />
          <Route path="/CreateGroupPage" element={<CreateGroupPage isDarkMode={isDarkMode} />} />
          <Route path="/GroupParticipantsPage" element={<GroupParticipantsPage isDarkMode={isDarkMode} />} />
          <Route path="/SharedTransactionsPage/:groupId" element={<SharedTransactionsPage />} />
          <Route path="/CreateSharedTransactionPage/:groupId" element={<CreateSharedTransactionPage />} /> 
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>

    </Router>
  );
};

export default App;
