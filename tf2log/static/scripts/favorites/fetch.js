const fetchingHint = document.querySelector(".server_list_fetching");
const target = document.querySelector(".target");
const favoritedServersStorage = window.localStorage.getItem("favorited_servers")
const missingFavoritesHint = document.currentScript.getAttribute("data-missing-favorites-text");

function populateFilteredServerCount() {
    const filteredServerCount = document.querySelectorAll(".server_list_item").length;
    document.getElementById("server_list_filtered_server_count").innerHTML = `(${filteredServerCount})`;
}

function fetchServers() {
    fetchingHint.style.display = "block";
    if (favoritedServersStorage === null || !JSON.parse(favoritedServersStorage).length) {
        fetchingHint.style.fontStyle = "normal";
        fetchingHint.innerHTML = missingFavoritesHint;
        return;
    }
    const favoritedServers = JSON.parse(favoritedServersStorage);
    fetch("/servers/fetch_favorites_subview", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({servers: favoritedServers}),
    })
    .then(response => response.text())
    .then(response => {
        fetchingHint.style.display = "none";
        target.innerHTML = response;
        populateFilteredServerCount();
        const sortButtons = ["server_list_sort_name", "server_list_sort_map",
                            "server_list_sort_mode", "server_list_sort_region"];
        sortButtons.forEach(item => document.querySelector(`.${item}`).classList.remove("sort_asc", "sort_desc"));
    });

}

document.addEventListener("DOMContentLoaded", () => fetchServers());
