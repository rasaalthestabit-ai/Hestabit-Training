export default function Badge({ text, color = "blue" }) {
  const colors = {
    blue: "bg-blue-100 text-blue-700",
    green: "bg-green-100 text-green-700",
    red: "bg-red-100 text-red-700",
  };

  return (
    <span className={`px-3 py-1 text-sm rounded-full ${colors[color]}`}>
      {text}
    </span>
  );
}
