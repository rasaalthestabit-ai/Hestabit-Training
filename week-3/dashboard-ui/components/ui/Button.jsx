export default function Button({
  children,
  variant = "primary",
  size = "md",
  ...props
}) {
  const base = "rounded-lg font-medium transition";

  const variants = {
    primary: "bg-pink-500 text-white hover:bg-gray-500",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
    danger: "bg-red-600 text-white hover:bg-red-700",
  };

  const sizes = {
    sm: "px-3 py-1 text-sm",
    md: "px-4 py-2",
    lg: "px-6 py-3 text-lg",
  };

  return (
    <button
      className={`${base} ${variants[variant]} ${sizes[size]}`}
      {...props}
    >
      {children}
    </button>
  );
}