import Image from "next/image";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";

export const metadata = {
  title: "Purity UI — Modern SaaS Dashboard",
  description: "Responsive SaaS landing page built with Next.js, Tailwind and optimized images.",
};

export default function HomePage() {
  return (
    <div className="flex flex-col">

      {/* HERO SECTION */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">

          {/* Left content */}
          <div>
            <Badge text="New Release" />

            <h1 className="text-4xl lg:text-6xl font-bold mt-4 leading-tight">
              Build Modern Dashboards Faster
            </h1>

            <p className="text-gray-600 mt-4 text-lg">
              Create scalable SaaS dashboards using reusable components,
              optimized performance and responsive design.
            </p>

            <div className="mt-6 flex gap-4">
              <Button variant="primary">Get Started</Button>
              <Button variant="secondary">Live Demo</Button>
            </div>
          </div>

          {/* Right image */}
          <div className="relative w-full h-[350px] lg:h-[450px]">
            <Image
              src="/Dashboard_preview.avif"
              alt="Dashboard preview"
              fill
              className="object-contain"
            />
          </div>

        </div>
      </section>

      {/* FEATURES SECTION */}
      <section className="py-20 bg-gray-50 px-6">
        <div className="max-w-6xl mx-auto">

          <h2 className="text-3xl font-bold text-center mb-10">
            Powerful Features
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

            <Card>
              <h3 className="font-semibold text-lg">Reusable Components</h3>
              <p className="text-gray-600 mt-2">
                Build once and reuse across your entire dashboard.
              </p>
            </Card>

            <Card>
              <h3 className="font-semibold text-lg">Optimized Performance</h3>
              <p className="text-gray-600 mt-2">
                Automatic image optimization and fast loading.
              </p>
            </Card>

            <Card>
              <h3 className="font-semibold text-lg">Responsive Layout</h3>
              <p className="text-gray-600 mt-2">
                Looks perfect on mobile, tablet and desktop.
              </p>
            </Card>

          </div>
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">

          <h2 className="text-3xl font-bold text-center mb-10">
            What Users Say
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

            <Card>
              <p className="text-gray-600">
                "This dashboard UI saved us weeks of development time."
              </p>
              <h4 className="mt-4 font-semibold">— Product Manager</h4>
            </Card>

            <Card>
              <p className="text-gray-600">
                "Clean architecture and reusable components made scaling easy."
              </p>
              <h4 className="mt-4 font-semibold">— Frontend Engineer</h4>
            </Card>

            <Card>
              <p className="text-gray-600">
                "Performance and SEO improvements were noticeable instantly."
              </p>
              <h4 className="mt-4 font-semibold">— Startup Founder</h4>
            </Card>

          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-gray-800 text-white py-10 px-6">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">

          <div>
            <h3 className="font-semibold mb-3">Product</h3>
            <p className="text-gray-400">Features</p>
            <p className="text-gray-400">Pricing</p>
            <p className="text-gray-400">Updates</p>
          </div>

          <div>
            <h3 className="font-semibold mb-3">Company</h3>
            <p className="text-gray-400">About</p>
            <p className="text-gray-400">Careers</p>
            <p className="text-gray-400">Contact</p>
          </div>

          <div>
            <h3 className="font-semibold mb-3">Legal</h3>
            <p className="text-gray-400">Privacy Policy</p>
            <p className="text-gray-400">Terms of Service</p>
          </div>

        </div>

        <p className="text-center text-gray-500 mt-8">
          © 2026 Purity UI. All rights reserved.
        </p>
      </footer>

    </div>
  );
}

