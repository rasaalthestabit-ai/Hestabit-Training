import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";

export default function Profile() {
  return (
    <Card>
      <h2 className="text-xl font-semibold mb-4">Profile</h2>

      <div className="space-y-4">
        <Input placeholder="Name" />
        <Input placeholder="Email" />
        <Input placeholder="Role" />

        <Button variant="primary">Save</Button>
      </div>
    </Card>
  );
}
