import React from "react";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";

const Layout = ({ children, isDarkMode, themeSwitch, showSidebar = true }) => {
  return (
    <div>
      <Header isDarkMode={isDarkMode} themeSwitch={themeSwitch} />
      <div className="flex">
        {showSidebar && <Sidebar isDarkMode={isDarkMode} />}
        <main className="flex-1">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
