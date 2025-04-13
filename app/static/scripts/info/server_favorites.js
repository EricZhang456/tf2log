const favoriteScriptTag = document.currentScript;
const favoriteButton = document.querySelector(".info_header_favorite");
favoriteButton.style.display = "block";

const addServerToFavorite = () => {
    const serverIP = favoriteScriptTag.getAttribute("data-server-ip");
    const serverPort = favoriteScriptTag.getAttribute("data-server-port");

};
