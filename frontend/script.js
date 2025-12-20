const API = "http://127.0.0.1:8000";

let tempBook = {};

// STEP 1 → STEP 2
function goToAuthor() {
    const title = document.getElementById("title").value;
    const year = document.getElementById("year").value;

    if (!title || !year) {
        alert("Please enter book title and published year");
        return;
    }

    tempBook.title = title;
    tempBook.year = year;

    document.getElementById("step-book").classList.remove("active");
    document.getElementById("step-author").classList.add("active");
}

// SUBMIT BOOK
async function submitBook() {
    const author = document.getElementById("authorName").value;

    if (!author) {
        alert("Please enter author name");
        return;
    }

    // Add author
    const authorRes = await fetch(`${API}/authors?name=${author}`, {
        method: "POST"
    });
    const authorData = await authorRes.json();

    // Add book
    await fetch(
        `${API}/books?title=${tempBook.title}&author_id=${authorData.id}&published_year=${tempBook.year}`,
        { method: "POST" }
    );

    document.getElementById("step-author").classList.remove("active");
    document.getElementById("success").classList.add("active");
    document.getElementById("view-books").classList.add("active");
}

// RESET FORM
function resetForm() {
    document.getElementById("success").classList.remove("active");
    document.getElementById("step-book").classList.add("active");

    document.querySelectorAll("input").forEach(i => i.value = "");
}

// LOAD BOOKS
async function loadBooks() {
    const res = await fetch(`${API}/books`);
    const books = await res.json();

    const list = document.getElementById("bookList");
    list.innerHTML = "";

    books.forEach(b => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>${b.title}</strong><br>
            👤 Author: ${b.author}<br>
            📅 Year: ${b.published_year}
        `;
        list.appendChild(li);
    });
}
