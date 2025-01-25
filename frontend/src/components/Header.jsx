import React from "react";
import { CiSun } from "react-icons/ci";
import { FaRegMoon } from "react-icons/fa";

const Header = ({ isDarkMode, themeSwitch }) => {
  return (
    <header className="dark:bg-gray-800">
      {/* Button for dark and light mode toggle */}
      <button
  onClick={themeSwitch}
  className={`absolute top-4 right-4 flex items-center justify-center w-10 h-10 rounded-full transition-colors ${
    isDarkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-200 hover:bg-gray-300'
  }`}
>
  {isDarkMode ? (
    <FaRegMoon size={20} className="text-white" />
  ) : (
    <CiSun size={20} className="text-black" />
  )}
</button>

    </header>
  );
};

export default Header;
