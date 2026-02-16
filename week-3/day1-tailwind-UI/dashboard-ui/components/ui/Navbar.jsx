export default function Navbar() {
  return (
    <div className="w-full h-16 bg-white shadow flex items-center justify-between px-6">
      
      <div className="text-xl font-semibold">
        Dashboard
      </div>

      <div className="flex items-center gap-4">
        <span className="text-gray-600">Notifications</span>
        <span className="text-gray-600">Profile</span>
      </div>

    </div>
  );
}
