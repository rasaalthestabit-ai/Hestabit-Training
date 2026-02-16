export default function Sidebar() {
  return (
    <div className="w-64 h-screen bg-gray-900 text-white p-5">
      
      <h2 className="text-lg font-bold mb-6">Menu</h2>

      <ul className="space-y-4">
        <li className="cursor-pointer hover:text-gray-300">Dashboard</li>
        <li className="cursor-pointer hover:text-gray-300">Users</li>
        <li className="cursor-pointer hover:text-gray-300">Analytics</li>
        <li className="cursor-pointer hover:text-gray-300">Settings</li>
      </ul>

    </div>
  );
}
