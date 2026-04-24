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
            <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#1f1f1f"><path d="M426-160q-9-26-23-48t-33-41q-19-19-41-33.5T281-306q2 29 14 54t32 45q20 20 45 32.5t54 14.5Zm108 0q29-3 54-15t45-32q20-20 32-45t15-54q-26 9-48.5 23T590-250q-19 19-33 41.5T534-160Zm59-407q47-47 47-113v-48l-70 59-90-109-90 109-70-59v48q0 66 47 113t113 47q66 0 113-47ZM440-80q-100 0-170-70t-70-170v-80q71-1 134 29t106 81v-153q-86-14-143-80.5T240-680v-136q0-26 23-36.5t43 6.5l74 64 69-84q12-14 31-14t31 14l69 84 74-64q20-17 43-6.5t23 36.5v136q0 90-57 156.5T520-443v153q43-51 106-81t134-29v80q0 100-70 170T520-80h-80Zm40-569Zm127 416Zm-253 0Z"/></svg>
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
          <label className="text-sm text-gray-500">About me</label>
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
