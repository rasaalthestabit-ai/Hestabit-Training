import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";

export default function SettingsPage() {
  return (
    <div className="space-y-6">

      <h1 className="text-2xl font-bold">Settings</h1>

      <Card>
        <h2 className="text-lg font-semibold mb-4">Profile Settings</h2>

        <div className="space-y-4">
          <Input placeholder="Full Name" />
          <Input placeholder="Email Address" />

          <div className="flex items-center gap-3">
            <span>Status:</span>
            <Badge text="Active"></Badge>
          </div>

          <Button variant="primary">Save Changes</Button>
        </div>
      </Card>

    </div>
  );
}
