const favoriteScriptTag = document.currentScript;
const favoriteButton = document.querySelector(".info_header_favorite");
favoriteButton.style.display = "block";

const serverIP = favoriteScriptTag.getAttribute("data-server-ip");
const serverPort = favoriteScriptTag.getAttribute("data-server-port");
const serverObj = {server_ip: serverIP, server_port: serverPort};

const favoriteHint = favoriteScriptTag.getAttribute("data-favorite-text");
const removeFavoriteHint = favoriteScriptTag.getAttribute("data-remove-favorite-text");

let duplicateServer = false;
let favoritedServers;

const getFavoritedServers = () => {
    const favoritedServersStorage = window.localStorage.getItem("favorited_servers");
    if (favoritedServersStorage === null || JSON.parse(favoritedServersStorage).length === 0) {
        favoritedServers = new Array();
    } else {
        favoritedServers = JSON.parse(favoritedServersStorage);
    }
};

const checkFavoriteDuplicate = () => {
    getFavoritedServers();
    if (favoritedServers.length) {
        for (const item of favoritedServers) {
            if (item.server_ip === serverObj.server_ip && item.server_port === serverObj.server_port) {
                duplicateServer = true;
                favoriteButton.innerHTML = removeFavoriteHint;
                return;
            } else {
                duplicateServer = false;
                favoriteButton.innerHTML = favoriteHint;
            }
        }
    } else {
        duplicateServer = false;
        favoriteButton.innerHTML = favoriteHint;
    }
};

const addServerToFavorite = () => {
    getFavoritedServers();
    if (!duplicateServer) {
        favoritedServers.push(serverObj);
        window.localStorage.setItem("favorited_servers", JSON.stringify(favoritedServers));
    } else {
        let filteredFavorites = favoritedServers;
        filteredFavorites = favoritedServers.filter(item => !(item.server_ip === serverObj.server_ip && item.server_port === serverObj.server_port));
        window.localStorage.setItem("favorited_servers", JSON.stringify(filteredFavorites));
    }
    checkFavoriteDuplicate();
};

document.addEventListener("DOMContentLoaded", () => {
    checkFavoriteDuplicate();
});
