"use client";

import { useState } from "react";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";

export default function ProfilePage() {

  // Editable state (real-world pattern)
  const [skills, setSkills] = useState(["UI Design", "JavaScript"]);
  const [techStack, setTechStack] = useState(["React", "Next.js", "Tailwind"]);

  const addSkill = () => {
    setSkills([...skills, "New Skill"]);
  };

  const addTech = () => {
    setTechStack([...techStack, "New Tech"]);
  };

  return (
    <div className="max-w-4xl mx-auto">

      {/* Page Title */}
      <h1 className="text-2xl font-bold mb-6">My Profile</h1>

      {/* Main container */}
      <div className="bg-white rounded-2xl shadow-sm border border-pink-100 p-8">

        {/* Header */}
        <div className="flex items-center gap-6">

          {/* Avatar */}
          <div className="w-20 h-20 rounded-full bg-pink-100 flex items-center justify-center text-2xl">
            🌸
          </div>

          <div>
            <h2 className="text-xl font-semibold">Rasaal Tewari</h2>
            <p className="text-gray-500 text-sm">Frontend Learner • UI Enthusiast</p>

            <div className="mt-2">
              <Badge text="Active learner" />
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className="my-8 border-t border-pink-100"></div>

        {/* Basic Info */}
        <div className="grid grid-cols-2 gap-6">

          <div>
            <label className="text-sm text-gray-500">Full name</label>
            <Input placeholder="Rasaal Tewari" />
          </div>

          <div>
            <label className="text-sm text-gray-500">Email</label>
            <Input placeholder="rt@gmail.com" />
          </div>

          <div>
            <label className="text-sm text-gray-500">Phone</label>
            <Input placeholder="+91 9876543210" />
          </div>

          <div>
            <label className="text-sm text-gray-500">Location</label>
            <Input placeholder="India" />
          </div>

        </div>

        {/* About */}
        <div className="mt-8">
          <label className="text-sm text-gray-500">✨ About me</label>
          <textarea
            defaultValue="I enjoy designing clean UIs, learning JavaScript, and building small projects daily."
            className="w-full mt-2 px-4 py-3 rounded-xl border border-pink-100 focus:outline-none focus:ring-2 focus:ring-pink-200"
            rows={4}
          />
        </div>

        {/* Skills Section */}
        <div className="mt-8">
          <div className="flex justify-between items-center">
            <label className="text-sm text-gray-500">Skills</label>
            <button
              onClick={addSkill}
              className="text-sm text-pink-500 hover:text-gray-600"
            >
              + Add skill
            </button>
          </div>

          <div className="flex flex-wrap gap-2 mt-3">
            {skills.map((skill, index) => (
              <Badge key={index} text={skill} />
            ))}
          </div>
        </div>

        {/* Tech Stack */}
        <div className="mt-8">
          <div className="flex justify-between items-center">
            <label className="text-sm text-gray-500">Tech Stack</label>
            <button
              onClick={addTech}
              className="text-sm text-pink-500 hover:text-gray-600"
            >
              + Add tech
            </button>
          </div>

          <div className="flex flex-wrap gap-2 mt-3">
            {techStack.map((tech, index) => (
              <Badge key={index} text={tech} />
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="mt-10 flex justify-end">
          <Button>Save Changes</Button>
        </div>

      </div>
    </div>
  );
}
