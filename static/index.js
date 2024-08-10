
function set_fav(url,token,el) {
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': token // Dynamically fetch CSRF token
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_fav == "True") {
            el.classList.remove("fa-regular");
            el.classList.add("fa-solid");
        } else {
            el.classList.remove("fa-solid");
            el.classList.add("fa-regular");
        }
    })
    .catch(error => console.error('Error:', error));
}
