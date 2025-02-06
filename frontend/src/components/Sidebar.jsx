import React from "react";
import { NavLink } from "react-router-dom";
const Sidebar = ({ isDarkMode }) => {
  return (
    <aside
      className={`h-screen w-64 fixed top-16 left-0 flex flex-col p-4 ${
        isDarkMode ? "bg-gray-800 text-white" : "bg-blue-100 text-gray-900"
      }`}
    >
      <nav className="flex flex-col space-y-4">
      <NavLink
          to="/profile"
          className={({ isActive }) =>
            `p-2 rounded-md ${isActive ? "bg-blue-500 text-white" : "hover:bg-blue-300"}`
          }
        >
          Dashboard
        </NavLink>
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `p-2 rounded-md ${isActive ? "bg-blue-500 text-white" : "hover:bg-blue-300"}`
          }
        >
          Dashboard
        </NavLink>
        <NavLink
          to="/budget"
          className={({ isActive }) =>
            `p-2 rounded-md ${isActive ? "bg-blue-500 text-white" : "hover:bg-blue-300"}`
          }
        >
          Budget
        </NavLink>
        <NavLink
          to="/shared-expense"
          className={({ isActive }) =>
            `p-2 rounded-md ${isActive ? "bg-blue-500 text-white" : "hover:bg-blue-300"}`
          }
        >
          Shared Expense
        </NavLink>
        <NavLink
          to="/transaction"
          className={({ isActive }) =>
            `p-2 rounded-md ${isActive ? "bg-blue-500 text-white" : "hover:bg-blue-300"}`
          }
        >
          Transaction
        </NavLink>
      </nav>
    </aside>
  );
};

export default Sidebar;
