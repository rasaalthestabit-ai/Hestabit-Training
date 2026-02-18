import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";

export default function Dashboard() {
  return (
    <div className="space-y-6">

      {/* Top stats */}
      <div className="grid grid-cols-4 gap-4">

        <Card>
          <h3 className="text-sm text-gray-500">Today's Money</h3>
          <p className="text-xl font-bold">$53,000</p>
          <Badge text="+55%" color="green" />
        </Card>

        <Card>
          <h3 className="text-sm text-gray-500">Today's Users</h3>
          <p className="text-xl font-bold">2,300</p>
          <Badge text="+5%" color="green" />
        </Card>

        <Card>
          <h3 className="text-sm text-gray-500">New Clients</h3>
          <p className="text-xl font-bold">+3,052</p>
          <Badge text="-14%" color="red" />
        </Card>

        <Card>
          <h3 className="text-sm text-gray-500">Total Sales</h3>
          <p className="text-xl font-bold">$173,000</p>
          <Badge text="+8%" color="green" />
        </Card>

      </div>

      {/* Welcome section */}
      <div className="grid grid-cols-2 gap-6">

        <Card>
          <h2 className="text-xl font-semibold">Welcome</h2>
          <p className="text-gray-600">
            Build dashboards using reusable components.
          </p>

          <div className="mt-4">
            <Button variant="primary">Read More</Button>
          </div>
        </Card>

        <Card>
          <h2 className="text-xl font-semibold">Work with the team</h2>
          <p className="text-gray-600">
            Collaborate and build products faster.
          </p>

          <div className="mt-4">
            <Button variant="secondary">Explore</Button>
          </div>
        </Card>

      </div>

      {/* Active users block */}
      <Card>
        <h2 className="text-lg font-semibold mb-4">Active Users</h2>

        <div className="grid grid-cols-4 gap-4">
          <div>
            <p className="text-sm text-gray-500">Users</p>
            <p className="font-bold">32,984</p>
          </div>

          <div>
            <p className="text-sm text-gray-500">Clicks</p>
            <p className="font-bold">2.4m</p>
          </div>

          <div>
            <p className="text-sm text-gray-500">Sales</p>
            <p className="font-bold">$2,400</p>
          </div>

          <div>
            <p className="text-sm text-gray-500">Items</p>
            <p className="font-bold">320</p>
          </div>
        </div>
      </Card>

    </div>
  );
}
