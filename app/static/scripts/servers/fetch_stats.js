"use strict";
const fetchServerCount = () => {
    fetch("/servers/server_count")
    .then((respnse) => respnse.text())
    .then((reponse) => {
        document.getElementById("server_header_server_count_number").innerHTML = reponse;
    });
}

const fetchPlayerCount = () => {
    fetch("/servers/player_count")
    .then((respnse) => respnse.text())
    .then((reponse) => {
        document.getElementById("server_header_player_count_number").innerHTML = reponse;
    });
}

document.addEventListener("DOMContentLoaded" , () => {
    fetchServerCount();
    fetchPlayerCount();
});
