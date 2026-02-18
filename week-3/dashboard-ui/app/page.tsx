import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";

export default function HomePage() {
  return (
    <div className="space-y-6">

      {/* Page heading */}
      <div>
        <h1 className="text-2xl font-bold">Welcome Back 👋</h1>
        <p className="text-gray-600">Here’s what’s happening with your dashboard today.</p>
      </div>

      {/* Quick stats */}
      <div className="grid grid-cols-3 gap-6">

        <Card>
          <h3 className="text-sm text-gray-500">Projects</h3>
          <p className="text-2xl font-bold">12</p>
          <Badge text="Active"></Badge>
        </Card>

        <Card>
          <h3 className="text-sm text-gray-500">Tasks</h3>
          <p className="text-2xl font-bold">48</p>
          <Badge text="In Progress"></Badge>
        </Card>

        <Card>
          <h3 className="text-sm text-gray-500">Notifications</h3>
          <p className="text-2xl font-bold">7</p>
          <Badge text="New"></Badge>
        </Card>

      </div>

      {/* Search + action section */}
      <Card>
        <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>

        <div className="flex items-center gap-4">
          <Input placeholder="Search anything..." />
          <Button variant="primary">Create Project</Button>
          <Button variant="secondary">View Reports</Button>
        </div>
      </Card>

    </div>
  );
}
