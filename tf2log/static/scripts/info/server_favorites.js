const favoriteScriptTag = document.currentScript;
const favoriteButton = document.querySelector(".info_header_favorite");

const serverIP = favoriteScriptTag.getAttribute("data-server-ip");
const serverPort = favoriteScriptTag.getAttribute("data-server-port");
const serverObj = {server_ip: serverIP, server_port: serverPort};

const favoriteHint = favoriteScriptTag.getAttribute("data-favorite-text");
const removeFavoriteHint = favoriteScriptTag.getAttribute("data-remove-favorite-text");

let favoritedServers;

function getFavoritedServers() {
    favoritedServers = JSON.parse(window.localStorage.getItem("favorited_servers")) || [];
}

function checkFavoriteDuplicate() {
    favoriteButton.innerHTML = favoriteHint;
    getFavoritedServers();
    if (!favoritedServers.length) {
        return false;
    }
    for (const item of favoritedServers) {
        const duplicateServer = item.server_ip === serverObj.server_ip && item.server_port === serverObj.server_port;
        if (duplicateServer) {
            favoriteButton.innerHTML = removeFavoriteHint;
            return duplicateServer;
        }
    }
    return false;
}

favoriteButton.addEventListener("click", () => {
    let finalFavorites = favoritedServers;
    if (!checkFavoriteDuplicate()) {
        finalFavorites.push(serverObj);
    } else {
        finalFavorites = favoritedServers.filter(item => !(item.server_ip === serverObj.server_ip && item.server_port === serverObj.server_port));
    }
    window.localStorage.setItem("favorited_servers", JSON.stringify(finalFavorites));
    checkFavoriteDuplicate();
});

document.addEventListener("DOMContentLoaded", () => {
    checkFavoriteDuplicate();
    favoriteButton.style.display = "block";
});
