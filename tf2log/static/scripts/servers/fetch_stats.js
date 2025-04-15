const fetchServerCount = () => {
    fetch("/servers/server_count")
    .then((respnse) => respnse.text())
    .then((reponse) => {
        document.getElementById("server_header_server_count_number").innerHTML = reponse;
    });
};

const fetchPlayerCount = () => {
    console.log("hi");
    fetch("/servers/player_count")
    .then((respnse) => respnse.text())
    .then((reponse) => {
        document.getElementById("server_header_player_count_number").innerHTML = reponse;
    });
};

document.addEventListener("DOMContentLoaded" , () => {
    fetchServerCount();
    fetchPlayerCount();
});
    
setInterval(fetchServerCount, 600000);
setInterval(fetchPlayerCount, 500000);
