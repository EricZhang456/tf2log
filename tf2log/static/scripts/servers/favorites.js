const favoritedAltText = document.currentScript.getAttribute("data-favorited-alt-text");
const removeFavoriteAltText = document.currentScript.getAttribute("data-remove-favorite-alt-text");

let favoritedServers;

function getFavoritedServers() {
    favoritedServers = JSON.parse(window.localStorage.getItem("favorited_servers")) || [];
}

function checkFavoriteDuplicate(serverObj) {
    getFavoritedServers();
    let result = false;
    if (favoritedServers.length) {
        favoritedServers.forEach(item => {
            if (item.server_ip === serverObj.server_ip && item.server_port === serverObj.server_port) {
                result = true;
            }
        });
    }
    return result;
}

function setStar(serverObj, serverFavoriteElement) {
    const serverFavoriteImg = serverFavoriteElement.firstElementChild;
    if (checkFavoriteDuplicate(serverObj)) {
        serverFavoriteImg.src = "/static/svg/star-fill.svg";
        serverFavoriteImg.title = removeFavoriteAltText;
    } else {
        serverFavoriteImg.src = "/static/svg/star.svg";
        serverFavoriteImg.title = favoritedAltText;
    }
}

function toggleServerFavorites(serverFavoriteElement, serverIP, serverPort) {
    const serverObj = {server_ip: serverIP, server_port: serverPort};
    getFavoritedServers();
    let finalFavorites = favoritedServers;
    if (!checkFavoriteDuplicate(serverObj)) {
        finalFavorites.push(serverObj);
    } else {
        finalFavorites = favoritedServers.filter(item => !(item.server_ip === serverObj.server_ip && item.server_port === serverObj.server_port));
    }
    window.localStorage.setItem("favorited_servers", JSON.stringify(finalFavorites));
    setStar(serverObj, serverFavoriteElement);
}

function attachFavoriteEventListener() {
    document.querySelectorAll(".server_list_favorite_button").forEach(item => {
        const serverObj = {server_ip: item.getAttribute("data-server-ip"), server_port: item.getAttribute("data-server-port")};
        setStar(serverObj, item);
        item.addEventListener("click", () => {
            toggleServerFavorites(item, item.getAttribute("data-server-ip"), item.getAttribute("data-server-port"));
        });
    });
}

document.addEventListener("DOMContentLoaded", () => attachFavoriteEventListener());

const observer = new MutationObserver(() => attachFavoriteEventListener());
observer.observe(document.querySelector(".target"), { childList: true });
