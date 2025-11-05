const API_URL = "/expenses";
let editingId = null;

function renderEmpty() {
  const list = document.getElementById("expenses-list");
  list.innerHTML = "<li style='color:#777'>Нет записей</li>";
}

function renderList(items) {
  const list = document.getElementById("expenses-list");
  list.innerHTML = "";

  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.title} — ${item.amount}₽ (${item.category || "без категории"})`;

    // Кнопка "Редактировать"
    const editBtn = document.createElement("button");
    editBtn.textContent = "✏️";
    editBtn.style.marginLeft = "10px";
    editBtn.onclick = () => editExpense(item);

    // Кнопка "Удалить"
    const delBtn = document.createElement("button");
    delBtn.textContent = "🗑️";
    delBtn.style.marginLeft = "5px";
    delBtn.onclick = () => deleteExpense(item.id);

    li.appendChild(editBtn);
    li.appendChild(delBtn);
    list.appendChild(li);
  });
}

async function loadExpenses(filters = {}) {
  try {
    let url = new URL(API_URL, window.location.origin);

    // Добавляем фильтры в URL
    if (filters.category) url.searchParams.append("category", filters.category);
    if (filters.date_from) url.searchParams.append("date_from", filters.date_from);
    if (filters.date_to) url.searchParams.append("date_to", filters.date_to);

    const res = await fetch(url);
    const data = await res.json();

    if (!Array.isArray(data) || data.length === 0) {
      renderEmpty();
      return;
    }
    renderList(data);
  } catch (err) {
    console.error(err);
    const list = document.getElementById("expenses-list");
    list.innerHTML = `<li style="color:red">Ошибка: ${err.message}</li>`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("expense-form");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("title").value.trim();
    const amount = parseFloat(document.getElementById("amount").value);
    const category = document.getElementById("category").value.trim();

    if (!title || amount <= 0) {
      alert("Введите корректные данные");
      return;
    }

    const method = editingId ? "PUT" : "POST";
    const url = editingId ? `${API_URL}/${editingId}` : API_URL;

    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, amount, category }),
    });

    if (res.ok) {
      editingId = null; // сбрасываем флаг редактирования
      form.reset();
      await loadExpenses();
    } else {
      const err = await res.json();
      alert("Ошибка: " + (err.detail || "неизвестная"));
    }
  });

  // Фильтры
  const filterBtn = document.getElementById("apply-filters");
  filterBtn.addEventListener("click", (e) => {
    e.preventDefault();
    const category = document.getElementById("filter-category").value.trim();
    const date_from = document.getElementById("filter-date-from").value;
    const date_to = document.getElementById("filter-date-to").value;
    loadExpenses({ category, date_from, date_to });
  });

  // Загрузка всех расходов при старте
  loadExpenses();
});

async function deleteExpense(id) {
  if (!confirm("Удалить этот расход?")) return;
  const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  if (res.ok) {
    await loadExpenses(); // Обновляем список
  } else {
    alert("Ошибка при удалении");
  }
}

function editExpense(item) {
  editingId = item.id;
  document.getElementById("title").value = item.title;
  document.getElementById("amount").value = item.amount;
  document.getElementById("category").value = item.category || "";
}
