export default function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/50">
      <div className="bg-white p-6 rounded-xl w-[400px]">
        {children}

        <button
          onClick={onClose}
          className="mt-4 bg-gray-200 px-4 py-2 rounded"
        >
          Close
        </button>
      </div>
    </div>
  );
}