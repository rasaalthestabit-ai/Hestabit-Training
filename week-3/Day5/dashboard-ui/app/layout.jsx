import "./globals.css";
import Navbar from "@/components/ui/Navbar";
import Sidebar from "@/components/ui/Sidebar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="h-screen flex flex-col">

        {/* Navbar */}
        <Navbar />

        {/* Sidebar + content wrapper */}
        <div className="flex flex-1">

          {/* Sidebar */}
          <Sidebar />

          {/* Page content */}
          <main className="flex-1 p-6 bg-gray-50">
            {children}
          </main>

        </div>

      </body>
    </html>
  );
}
