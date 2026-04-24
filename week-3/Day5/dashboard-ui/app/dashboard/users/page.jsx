import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";

const users = [
  {
    id: 1,
    name: "Rasaal Tewari",
    role: "Frontend Developer",
    email: "rt@gmail.com",
    status: "online",
    joined: "12 Jan 2025",
  },
  {
    id: 2,
    name: "Aman Sharma",
    role: "Backend Developer",
    email: "aman@gmail.com",
    status: "offline",
    joined: "03 Feb 2025",
  },
  {
    id: 3,
    name: "Priya Verma",
    role: "UI/UX Designer",
    email: "priya@gmail.com",
    status: "online",
    joined: "21 Mar 2025",
  },
];

export default function UsersPage() {
  return (
    <div className="space-y-6">

      <h1 className="text-2xl font-bold">Users</h1>

      <Card>
        <div className="overflow-x-auto">

          <table className="w-full text-left border-collapse">

            {/* Table Head */}
            <thead className="border-b">
              <tr className="text-sm text-gray-600">
                <th className="py-3">Name</th>
                <th className="py-3">Role</th>
                <th className="py-3">Email</th>
                <th className="py-3">Status</th>
                <th className="py-3">Date Joined</th>
                <th className="py-3 text-right">Actions</th>
              </tr>
            </thead>

            {/* Table Body */}
            <tbody>
              {users.map((user) => (
                <tr
                  key={user.id}
                  className="border-b last:border-none hover:bg-gray-50 transition"
                >
                  <td className="py-4 font-medium">{user.name}</td>
                  <td className="py-4 text-gray-600">{user.role}</td>
                  <td className="py-4 text-gray-600">{user.email}</td>
                  <td className="py-4">
                    <Badge
                      text={user.status}
                      color={
                        user.status === "online"
                          ? "green"
                          :"red"
                      }
                    />
                  </td>

                  <td className="py-4 text-gray-600">{user.joined}</td>
                  <td className="py-4 text-right space-x-2">
                    <Button variant="secondary" size="sm">
                      Edit
                    </Button>
                    <Button variant="danger" size="sm">
                      Delete
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>

          </table>
        </div>
      </Card>

    </div>
  );
}
