import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";

export default function SignInPage() {
  return (
    <div className="max-w-md mx-auto mt-10">
      <Card>
        <h2 className="text-xl font-semibold mb-4">Sign In</h2>

        <div className="space-y-4">
          <Input placeholder="Email" />
          <Input placeholder="Password" type="password" />

          <Button variant="primary">Login</Button>
        </div>
      </Card>
    </div>
  );
}
