const favoriteScriptTag = document.currentScript;
const favoriteButton = document.querySelector(".info_header_favorite");
favoriteButton.style.display = "block";

const serverIP = favoriteScriptTag.getAttribute("data-server-ip");
const serverPort = favoriteScriptTag.getAttribute("data-server-port");
const serverObj = {server_ip: serverIP, server_port: serverPort};

let duplicateServer = false;
let favoritedServers;

const getFavoritedServers = () => {
    const favoritedServersStorage = window.localStorage.getItem("favorited_servers");
    if (favoritedServersStorage === null || JSON.parse(favoritedServersStorage).length === 0) {
        favoritedServers = new Array();
    } else {
        favoritedServers = JSON.parse(favoritedServersStorage);
    }
}

const checkFavoriteDuplicate = () => {
    getFavoritedServers();
    if (favoritedServers.length) {
        favoritedServers.some((item) => {
            if (item.server_ip === serverObj.server_ip && item.server_port === serverObj.server_port) {
                duplicateServer = true;
                favoriteButton.innerHTML = "Remove from favorites";
            } else {
                duplicateServer = false;
                favoriteButton.innerHTML = "Favorite";
            }
        });
    } else {
        duplicateServer = false;
        favoriteButton.innerHTML = "Favorite";
    }
};

const addServerToFavorite = () => {
    getFavoritedServers();
    if (!duplicateServer) {
        favoritedServers.push(serverObj);
        window.localStorage.setItem("favorited_servers", JSON.stringify(favoritedServers));
    } else {
        filteredFavorites = favoritedServers.filter(item => item.server_ip !== serverObj.server_ip && item.server_port !== serverObj.server_port);
        window.localStorage.setItem("favorited_servers", JSON.stringify(filteredFavorites));
    }
    checkFavoriteDuplicate();
};

document.addEventListener("DOMContentLoaded", () => {
    checkFavoriteDuplicate();
});
