import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";

export default function SignUpPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-pink-50 px-4">
      
      <div className="w-full max-w-lg">
        <Card>

          <h2 className="text-2xl font-semibold text-center mb-6">
            Sign Up
          </h2>

          <div className="space-y-5">

            <Input placeholder="Email" />
            <Input placeholder="Create Password" type="password" />
          <div className="mt-4 flex justify-center">
            <Button variant="primary">Sign Up</Button>
          </div>
          </div>

        </Card>
      </div>

    </div>
  );
}
