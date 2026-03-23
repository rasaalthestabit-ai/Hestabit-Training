import { saveTodos, loadTodos } from "./storage/localStorage.js";

const form = document.getElementById("todo-form");
const input = document.getElementById("todo-input");
const list = document.getElementById("todo-list");

let todos = loadTodos();

// Render todos
function renderTodos() {
  list.innerHTML = "";

  todos.forEach(todo => {
    const li = document.createElement("li");
    li.dataset.id = todo.id;

    li.innerHTML = `
      <span class="text">${todo.text}</span>
      <div class="actions">
        <button class="edit">Edit</button>
        <button class="delete">Delete</button>
      </div>
    `;

    list.appendChild(li);
  });
}

// Add todo
form.addEventListener("submit", e => {
  e.preventDefault();

  const text = input.value.trim();
  if (!text) return;

  const todo = {
    id: Date.now(),
    text,
    completed: false
  };

  todos.push(todo);
  saveTodos(todos);
  renderTodos();

  input.value = "";
});

// Delete + Edit using event delegation
list.addEventListener("click", e => {
  const li = e.target.closest("li");
  const id = Number(li.dataset.id);

  // Delete
  if (e.target.classList.contains("delete")) {
    todos = todos.filter(t => t.id !== id);
    saveTodos(todos);
    renderTodos();
  }

  // Edit
  if (e.target.classList.contains("edit")) {
    const newText = prompt("Edit todo:");
    if (!newText) return;

    todos = todos.map(t =>
      t.id === id ? { ...t, text: newText } : t
    );

    saveTodos(todos);
    renderTodos();
  }
});

// Initial render
renderTodos();
