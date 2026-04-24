import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";

export default function SignInPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-pink-50 px-4">
      
      <div className="w-full max-w-lg">
        <Card>

          <h2 className="text-2xl font-semibold text-center mb-6">
            Log In 
          </h2>

          <div className="space-y-5">

            <Input placeholder="Email" />
            <Input placeholder="Password" type="password" />

          <div className="mt-4 flex justify-center">
            <Button variant="primary">Log In</Button>
          </div>

          </div>

        </Card>
      </div>

    </div>
  );
}
