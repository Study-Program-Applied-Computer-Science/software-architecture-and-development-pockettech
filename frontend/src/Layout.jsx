import React from "react";
import Header from "./components/Header"; // Import the Header

const Layout = ({ children, isDarkMode, themeSwitch }) => {
  return (
    <div className={`min-h-screen ${isDarkMode ? "dark" : ""}`}>
      {/* Header at the top */}
      <Header isDarkMode={isDarkMode} themeSwitch={themeSwitch} />

      {/* Page content */}
      <main className="pt-16">{children}</main>
    </div>
  );
};

export default Layout;
