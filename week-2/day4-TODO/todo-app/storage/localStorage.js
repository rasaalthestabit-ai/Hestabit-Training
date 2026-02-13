const KEY = "todos";

export function saveTodos(todos) {
  try {
    localStorage.setItem(KEY, JSON.stringify(todos));
  } catch (err) {
    console.error("Error saving todos", err);
  }
}

export function loadTodos() {
  try {
    const data = localStorage.getItem(KEY);
    return data ? JSON.parse(data) : [];
  } catch (err) {
    console.error("Error loading todos", err);
    return [];
  }
}
