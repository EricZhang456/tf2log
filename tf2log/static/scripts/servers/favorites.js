const favoritedAltText = document.currentScript.getAttribute("data-favorited-alt-text");
const removeFavoriteAltText = document.currentScript.getAttribute("data-remove-favorite-alt-text");

let favoritedServers;

const getFavoritedServers = () => {
    const favoritedServersStorage = window.localStorage.getItem("favorited_servers");
    if (favoritedServersStorage === null || JSON.parse(favoritedServersStorage).length === 0) {
        favoritedServers = new Array();
    } else {
        favoritedServers = JSON.parse(favoritedServersStorage);
    }
};

const checkFavoriteDuplicate = (serverObj) => {
    getFavoritedServers();
    let result = false;
    if (favoritedServers.length) {
        favoritedServers.forEach((item) => {
            if (item.server_ip === serverObj.server_ip && item.server_port === serverObj.server_port) {
                result = true;
            }
        });
    }
    return result;
};

const setStar = (serverObj, serverFavoriteElement) => {
    const serverFavoriteImg = serverFavoriteElement.firstElementChild;
    if (checkFavoriteDuplicate(serverObj)) {
        serverFavoriteImg.src = "/static/svg/star-fill.svg";
    } else {
        serverFavoriteImg.src = "/static/svg/star.svg";
    }
}

const toggleServerFavorites = (serverFavoriteElement, serverIP, serverPort) => {
    const serverObj = {server_ip: serverIP, server_port: serverPort};
    getFavoritedServers();
    if (!checkFavoriteDuplicate(serverObj)) {
        favoritedServers.push(serverObj);
        window.localStorage.setItem("favorited_servers", JSON.stringify(favoritedServers));
    } else {
        let filteredFavorites = favoritedServers;
        filteredFavorites = favoritedServers.filter(item => !(item.server_ip === serverObj.server_ip && item.server_port === serverObj.server_port));
        window.localStorage.setItem("favorited_servers", JSON.stringify(filteredFavorites));
    }
    setStar(serverObj, serverFavoriteElement);
};

const attachFavoriteEventListener = () => {
    document.querySelectorAll(".server_list_favorite_button").forEach((item) => {
        const serverObj = {server_ip: item.getAttribute("data-server-ip"), server_port: item.getAttribute("data-server-port")};
        setStar(serverObj, item);
        item.addEventListener("click", () => {
            toggleServerFavorites(item, item.getAttribute("data-server-ip"), item.getAttribute("data-server-port"));
        });
    });
};

document.addEventListener("DOMContentLoaded", () => {
    attachFavoriteEventListener();
});

const observer = new MutationObserver((_) => {
    attachFavoriteEventListener();
});

observer.observe(document.querySelector(".target"), {childList: true})
