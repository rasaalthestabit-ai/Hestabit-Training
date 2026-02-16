import "./globals.css";
import Navbar from "@/components/ui/Navbar";
import Sidebar from "@/components/ui/Sidebar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>

        {/* Top Navbar */}
        <Navbar />

        {/* Sidebar + page area */}
        <div className="flex">

          {/* Sidebar */}
          <Sidebar />

          {/* Page content */}
          <main className="flex-1 p-6">
            {children}
          </main>

        </div>

      </body>
    </html>
  );
}

