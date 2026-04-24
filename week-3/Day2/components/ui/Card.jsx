export default function Card({ children }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow">
      {children}
    </div>
  );
}