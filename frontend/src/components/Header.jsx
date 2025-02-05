import React from "react";
import { CiSun } from "react-icons/ci";
import { FaRegMoon } from "react-icons/fa";

const Header = ({ isDarkMode, themeSwitch }) => {
  return (
    <header
      className={`absolute fixed top-0 left-0 w-full h-16 flex items-center justify-between px-4 ${
        isDarkMode ? "bg-gray-900 text-white" : "bg-blue-50 text-gray-900"
      }`}
    >
      {/* Left: FinancePlanner Title */}
      <h1 className="text-xl font-bold">FinancePlanner</h1>

      {/* Right: Theme Toggle */}
      <button
        onClick={themeSwitch}
        className={`flex items-center justify-center w-10 h-10 rounded-full transition-colors ${
          isDarkMode
            ? "bg-gray-800 hover:bg-gray-700 text-white"
            : "bg-blue-200 hover:bg-blue-300 text-blue-600"
        }`}
      >
        {isDarkMode ? <FaRegMoon size={20} /> : <CiSun size={20} />}
      </button>
    </header>
  );
};

export default Header;
