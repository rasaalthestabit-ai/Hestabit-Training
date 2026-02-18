"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const linkClass = (path) =>
    `block px-4 py-2 rounded-lg ${
      pathname === path ? "bg-blue-500 text-white" : "text-gray-700 hover:bg-gray-100"
    }`;

  return (
    <aside className="w-64 h-screen bg-white border-r p-4 space-y-4">
      <h2 className="text-xl font-bold">Dashboard</h2>

      <nav className="space-y-2">
        <Link href="/dashboard" className={linkClass("/dashboard")}>
          Dashboard
        </Link>

        <Link href="/dashboard/profile" className={linkClass("/dashboard/profile")}>
          Profile
        </Link>

        <Link href="/about" className={linkClass("/about")}>
          About
        </Link>
      </nav>
    </aside>
  );
}
