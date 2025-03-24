const API_URL = "http://localhost:5000/api/tasks/"

document.addEventListener("DOMContentLoaded", () => {
    loadTasks()

    document.getElementById("task-form").addEventListener("submit", async (e) => {
        e.preventDefault()
        const titleInput = document.getElementById("task-title")
        const title = titleInput.value.trim()
        if (!title) return;
    
        await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ title })
        });
    
        titleInput.value = ""
        loadTasks();
      })
})

async function loadTasks() {
    const res   = await fetch(API_URL)
    const tasks = await res.json()
    const list = document.getElementById("task-list")
    list.innerHTML = ""

    tasks.forEach(task => {
        const item = document.createElement("li")
        item.className = "list-group-item d-flex justify-content-between align-items-center"

        const span = document.createElement("span")
        span.textContent = task.title
        if (task.completed) span.classList.add("text-decoration-line-through")

        const btnGroup = document.createElement("div")
        btnGroup.classList.add("btn-group", "btn-group-sm")

        const toggleBtn = document.createElement("button")
        toggleBtn.className = "btn btn-outline-success"
        toggleBtn.textContent = task.completed ? "Desfazer" : "Concluir"
        toggleBtn.onclick = async () => {
            await fetch(API_URL + task.id, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ completed: !task.completed })
            })
            loadTasks()
        }

        const deleteBtn = document.createElement("button");
        deleteBtn.className = "btn btn-outline-danger"
        deleteBtn.textContent = "Excluir"
        deleteBtn.onclick = async () => {
            await fetch(API_URL + task.id, { method: "DELETE" })
            loadTasks();
        }

        btnGroup.appendChild(toggleBtn)
        btnGroup.appendChild(deleteBtn)
        item.appendChild(span)
        item.appendChild(btnGroup)
        list.appendChild(item)
    });
}