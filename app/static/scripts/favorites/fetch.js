const fetchingHint = document.querySelector(".server_list_fetching");
const target = document.querySelector(".target");
const favoritedServersStorage = window.localStorage.getItem("favorited_servers")

const populateFilteredServerCount = () => {
    const filteredServerCount = document.querySelectorAll(".server_list_item").length;
    document.getElementById("server_list_filtered_server_count").innerHTML = `(${filteredServerCount})`;
};

const fetchServers = () => {
    fetchingHint.style.display = "block";
    if (favoritedServersStorage === null) {
        fetchingHint.style.fontStyle = "normal";
        fetchingHint.innerHTML = "No favorited servers."
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
    .then((response) => response.text())
    .then((response) => {
        fetchingHint.style.display = "none";
        target.innerHTML = response;
        populateFilteredServerCount();
    });
};

document.addEventListener("DOMContentLoaded", () => {
    fetchServers();
});
