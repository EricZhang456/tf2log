const favoriteScriptTag = document.currentScript;
const favoriteButton = document.querySelector(".info_header_favorite");
favoriteButton.style.display = "block";

const addServerToFavorite = () => {
    const favoritedServersStorage = window.localStorage.getItem("favorited_servers");
    let favoritedServers;
    if (favoritedServersStorage === null) {
        favoritedServers = new Array();
    } else {
        favoritedServers = JSON.parse(favoritedServersStorage);
    }
    const serverIP = favoriteScriptTag.getAttribute("data-server-ip");
    const serverPort = favoriteScriptTag.getAttribute("data-server-port");
    const serverObj = {server_ip: serverIP, server_port: serverPort};
    let duplicateServer = false;
    favoritedServers.some((item) => {
        if (item.server_ip === serverObj.server_ip && item.server_port === serverObj.server_port) {
            duplicateServer = true;
        }
    });
    if (!duplicateServer) {
        console.log("hi");
        favoritedServers.push(serverObj);
        window.localStorage.setItem("favorited_servers", JSON.stringify(favoritedServers));
    }
};
