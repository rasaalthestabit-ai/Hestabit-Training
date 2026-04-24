import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";

export default function BillingPage() {
  return (
    <div className="space-y-8">

      <h1 className="text-2xl font-bold">Billing</h1>

      <Card>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold">Current Plan</h2>
            <p className="text-gray-600 mt-1">
              You are currently on the <strong>Pro Plan</strong>.
            </p>
          </div>

          <Badge text="Active" className="bg-green-100 text-green-700" />
        </div>

        <div className="mt-6">
          <p className="text-3xl font-bold">$29<span className="text-base font-medium text-gray-600"> / month</span></p>
        </div>

        <div className="mt-6">
          <Button variant="secondary">Change Plan</Button>
        </div>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">Usage Overview</h2>

        <div className="space-y-3 text-gray-600">
          <p>Projects Used: 8 / 10</p>
          <p>Team Members: 5 / 10</p>
          <p>Storage Used: 12GB / 50GB</p>
        </div>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">Payment Method</h2>

        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium">Visa ending in 4242</p>
            <p className="text-sm text-gray-600">Expires 12/27</p>
          </div>

          <Button variant="secondary" size="sm">
            Update
          </Button>
        </div>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">Billing History</h2>

        <div className="space-y-4">

          <div className="flex justify-between items-center border-b pb-3">
            <div>
              <p className="font-medium">Jan 2026</p>
              <p className="text-sm text-gray-600">Pro Plan Subscription</p>
            </div>
            <p className="font-semibold">$29</p>
          </div>

          <div className="flex justify-between items-center border-b pb-3">
            <div>
              <p className="font-medium">Dec 2025</p>
              <p className="text-sm text-gray-600">Pro Plan Subscription</p>
            </div>
            <p className="font-semibold">$29</p>
          </div>

          <div className="flex justify-between items-center">
            <div>
              <p className="font-medium">Nov 2025</p>
              <p className="text-sm text-gray-600">Pro Plan Subscription</p>
            </div>
            <p className="font-semibold">$29</p>
          </div>

        </div>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-3">
          Need More Features?
        </h2>

        <p className="text-gray-600 mb-4">
          Upgrade to the Enterprise plan for unlimited projects,
          priority support and advanced analytics.
        </p>

        <Button variant="primary">
          Upgrade to Enterprise
        </Button>
      </Card>

    </div>
  );
}
