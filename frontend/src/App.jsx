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
import CreateGroupPage from "./pages/CreateGroupPage";
import GroupParticipantsPage from "./pages/GroupParticipantsPage";
import SharedTransactionsPage from "./pages/SharedTransactionsPage";
import CreateSharedTransactionPage from "./pages/CreateSharedTransactionPage";

const ProtectedRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem("user_id") !== null;
  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }
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
          path="*"
          element={
            <Layout isDarkMode={isDarkMode} themeSwitch={themeSwitch} showSidebar={true}>
              <Routes>
                <Route path="/dashboard" element={<ProtectedRoute><Dashboard isDarkMode={isDarkMode} /></ProtectedRoute>} />
                <Route path="/profile" element={<ProtectedRoute><UserProfile /></ProtectedRoute>} />
                
                {/* Budget Routes */}
                <Route path="/budget" element={<ProtectedRoute><BudgetOverviewPage isDarkMode={isDarkMode} /></ProtectedRoute>} />
                <Route path="/budget/create" element={<ProtectedRoute><CreateBudgetPage isDarkMode={isDarkMode} /></ProtectedRoute>} />
                <Route path="/budget/edit/:budgetId" element={<ProtectedRoute><EditBudgetPage isDarkMode={isDarkMode} /></ProtectedRoute>} />
                
                {/* Expense Routes */}
                <Route path="/expenses" element={<ProtectedRoute><ExpenseList isDarkMode={isDarkMode} /></ProtectedRoute>} />
                <Route path="/expenses/new" element={<ProtectedRoute><ExpenseForm isDarkMode={isDarkMode} /></ProtectedRoute>} />
                <Route path="/expenses/edit/:expenseId" element={<ProtectedRoute><ExpenseForm isDarkMode={isDarkMode} /></ProtectedRoute>} />
                <Route path="/expenses/:expenseId" element={<ProtectedRoute><ExpenseView isDarkMode={isDarkMode} /></ProtectedRoute>} />
                
                {/* Group & Shared Transactions */}
                <Route path="/CreateGroupPage" element={<ProtectedRoute><CreateGroupPage isDarkMode={isDarkMode} /></ProtectedRoute>} />
                <Route path="/GroupParticipantsPage" element={<ProtectedRoute><GroupParticipantsPage isDarkMode={isDarkMode} /></ProtectedRoute>} />
                <Route path="/SharedTransactionsPage/:groupId" element={<ProtectedRoute><SharedTransactionsPage /></ProtectedRoute>} />
                <Route path="/CreateSharedTransactionPage/:groupId" element={<ProtectedRoute><CreateSharedTransactionPage /></ProtectedRoute>} />
                
                {/* Catch-All Route */}
                <Route path="*" element={<NotFound />} />
              </Routes>
            </Layout>
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
