const populateMapThumbnail = (map_name) => {
    fetch(`/info/thumbnail/${map_name}`)
    .then(response => response.text())
    .then((response) => {
        if(response) {
            const infoHeader = document.querySelector(".info_header_server");
            infoHeader.style.setProperty("background-image", `url(${response})`);
            infoHeader.style.setProperty("background-position", "center");
            infoHeader.style.setProperty("background-size", "cover");
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    populateMapThumbnail(document.getElementById("info_map_background_script").getAttribute("x-map-name"));
});
