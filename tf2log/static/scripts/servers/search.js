const hintColor = "#aba8a5";
const activeColor = "#fff";

const searchBox = document.getElementById("server_search_box");

const setSearchBoxStyle = (value) => {
    if (value.length > 0) {
        searchBox.style.color = activeColor;
        searchBox.style.fontStyle = "normal";
    } else {
        searchBox.style.color = hintColor;
        searchBox.style.fontStyle = "italic";
    }
};

searchBox.addEventListener("input", (field) => {
    const value = field.target.value.trim().toLowerCase();
    document.querySelectorAll(".server_list_item").forEach((server) => {
        const visible = server.getAttribute("data-server-name").toLowerCase().includes(value) 
                        || server.getAttribute("data-server-readable-map").toLowerCase().includes(value)
                        || server.getAttribute("data-server-mode").toLowerCase().includes(value)
                        || server.getAttribute("data-server-region").toLowerCase().includes(value);
        server.classList.toggle("hide", !visible);
    });
    setSearchBoxStyle(value);
    const visibleServerItems = document.querySelectorAll(".server_list_item:not(.hide)").length;
    document.getElementById("server_list_filtered_server_count").innerHTML = `(${visibleServerItems})`;
});

document.addEventListener("DOMContentLoaded", () => {
    document.querySelector(".server_search").style.display = "flex";
    searchBox.value = "";
    setSearchBoxStyle(searchBox.value);
});
