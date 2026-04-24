import Card from "@/components/ui/Card";

export default function About() {
  return (
    <div className="space-y-6">

      <Card>
        <h1 className="text-2xl font-bold mb-4">
          About This Dashboard
        </h1>

        <p className="text-gray-600 leading-relaxed">
          This project is a modern, reusable UI-based dashboard built using 
          component-driven architecture. It simulates a real-world industry 
          admin panel where users can manage profiles, settings, authentication, 
          and team data in a clean and scalable environment.
        </p>
      </Card>

      <Card>
        <h2 className="text-xl font-semibold mb-3">
          What This Website Does
        </h2>

        <ul className="space-y-2 text-gray-600 list-disc pl-5">
          <li>User authentication (Sign In / Sign Up UI)</li>
          <li>User management with status badges (Online / Offline)</li>
          <li>Profile and account settings management</li>
          <li>Reusable UI components (Card, Button, Input, Badge)</li>
          <li>Responsive dashboard layout with sidebar + navbar</li>
        </ul>
      </Card>

      <Card>
        <h2 className="text-xl font-semibold mb-3">
          Architecture & Approach
        </h2>

        <p className="text-gray-600 leading-relaxed">
          The application follows a reusable component-based structure. 
          Instead of repeating UI styles everywhere, common components like 
          buttons, inputs, cards, and badges are abstracted and reused across 
          pages. This improves scalability, maintainability, and consistency.
        </p>

        <p className="text-gray-600 leading-relaxed mt-3">
          The layout uses a structured dashboard system with a fixed navbar 
          and sidebar, similar to real admin panels used in production SaaS 
          platforms.
        </p>
      </Card>

      <Card>
        <h2 className="text-xl font-semibold mb-3">
          Tech Stack
        </h2>

        <ul className="space-y-2 text-gray-600 list-disc pl-5">
          <li>React / Next.js App Router</li>
          <li>Tailwind CSS for styling</li>
          <li>Reusable UI Component System</li>
          <li>Modern responsive layout design</li>
        </ul>
      </Card>

      <Card>
        <h2 className="text-xl font-semibold mb-3">
          Future Improvements
        </h2>

        <ul className="space-y-2 text-gray-600 list-disc pl-5">
          <li>Backend integration with real database</li>
          <li>Authentication</li>
          <li>Role-based access control</li>
          <li>Dark mode support</li>
          <li>Real-time online status tracking</li>
        </ul>
      </Card>

    </div>
  );
}
