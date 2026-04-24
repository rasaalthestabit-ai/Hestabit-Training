"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const linkClass = (path) =>
    `block px-4 py-2 rounded-lg ${
      pathname === path ? "bg-pink-500 text-white" : "text-gray-500 hover:bg-gray-100"
    }`;

  return (
    <aside className="w-64 min-h-screen bg-white border-r p-4 space-y-4">
      <div className="flex justify-space-between">
      <h2 className="text-xl font-bold">Dashboard</h2>
      <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#1f1f1f"><path d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z"/></svg>
      </div>

      <nav className="space-y-2">
        <Link href="/dashboard" className={linkClass("/dashboard")}>
          Dashboard
        </Link>

        <Link href="/dashboard/profile" className={linkClass("/dashboard/profile")}>
          Profile
        </Link>

        <Link href="/dashboard/users" className={linkClass("/dashboard/users")}>
          Users
        </Link>

        <Link href="/dashboard/billing" className={linkClass("/dashboard/billing")}>
          Billing
        </Link>

        <Link href="/about" className={linkClass("/about")}>
          About
        </Link>
      </nav>
    </aside>
  );
}
