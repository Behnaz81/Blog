function createCategoryLink(cat) {
    const a = document.createElement('a');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    a.textContent = `${cat.title}`;
    a.classList.add('dropdown-item');
    a.classList.add('text-center');
    a.href = `http://localhost:8000/api/categories/${cat.id}/`;

    dropdownMenu.appendChild(a)
}

function fetchCategories() {
    const apiUrl = "http://localhost:8000/api/categories/";
    const dropdownMenu = document.querySelector('.dropdown-menu');

    fetch(apiUrl)
        .then(response => {
            if(!response.ok) {
                throw new Error("There is something wrong");
            }
            return response.json();
        })
        .then(data => {
            dropdownMenu.innerHTML = ''
            data.forEach(createCategoryLink);
        })
        .catch(error => {
            console.error(error.message);
        });
}


document.addEventListener('DOMContentLoaded', function() {
    fetchCategories();
});