"use client";

import { useRouter } from "next/navigation";
import Input from "./Input";

export default function Navbar() {
  const router = useRouter();

  return (
    <header className="w-full bg-white border-b px-6 py-4 flex items-center justify-between">

      <h1 className="text-lg font-bold">Purity UI Dashboard</h1>

      <div className="flex items-center gap-6">
        <Input placeholder="Search..." />

        <span
          onClick={() => router.push("/signin")}
          className="cursor-pointer text-sm font-medium text-gray-700 hover:text-black transition"
        >
          SignIn
        </span>

        <span
          onClick={() => router.push("/settings")}
          className="cursor-pointer text-sm font-medium text-gray-700 hover:text-black transition"
        >
          Settings
        </span>
      </div>

    </header>
  );
}
