import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";

export default function SettingsPage() {
  return (
    <div className="space-y-8">

      <h1 className="text-2xl font-bold">Settings</h1>

      {/* ================= Profile Settings ================= */}
      <Card>
        <h2 className="text-lg font-semibold mb-6">Profile Information</h2>

        <div className="space-y-4">
          <Input placeholder="Full Name" default Value="Rasaal Tewari"/>
          <Input placeholder="Email Address" defaultValue="rt@gmail.com" />
          <Input placeholder="Phone Number" defaultValue="+91 9876543210" />
          <Input placeholder="Role" defaultValue="Frontend Developer" />
          <Input placeholder="Location" defaultValue="India" />

          <div className="flex items-center gap-3">
            <span className="text-sm font-medium">Account Status:</span>
            <Badge text="Active" />
          </div>

          <div className="pt-2">
            <Button variant="primary">Save Profile</Button>
          </div>
        </div>
      </Card>

      {/* ================= Security Settings ================= */}
      <Card>
        <h2 className="text-lg font-semibold mb-6">Account Security</h2>

        <div className="space-y-4">
          <Input type="password" placeholder="Current Password" />
          <Input type="password" placeholder="New Password" />
          <Input type="password" placeholder="Confirm New Password" />

          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">
              Two-Factor Authentication
            </span>
            <Badge text="Disabled" />
          </div>

          <Button variant="primary">Update Password</Button>
        </div>
      </Card>

      {/* ================= Preferences ================= */}
      <Card>
        <h2 className="text-lg font-semibold mb-6">Preferences</h2>

        <div className="space-y-4">

          <div className="flex items-center justify-between">
            <span>Email Notifications</span>
            <Badge text="Enabled" />
          </div>

          <div className="flex items-center justify-between">
            <span>Theme</span>
            <Badge text="Light Mode" />
          </div>

          <div className="flex items-center justify-between">
            <span>Language</span>
            <Badge text="English" />
          </div>

          <Button variant="secondary">Update Preferences</Button>
        </div>
      </Card>

      {/* ================= Danger Zone ================= */}
      <Card>
        <h2 className="text-lg font-semibold mb-4 text-red-600">
          Danger Zone
        </h2>

        <p className="text-sm text-gray-600 mb-4">
          Once you delete your account, there is no going back.
        </p>

        <Button variant="danger">
          Delete Account
        </Button>
      </Card>

    </div>
  );
}
