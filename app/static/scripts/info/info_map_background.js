const populateMapThumbnail = (map_name) => {
    fetch(`/info/thumbnail/${map_name}`, {
        method: "GET",
        headers: {
            "x-get-thumbnail": "1"
        }
    })
    .then((response) => {
        if (!response.ok) {
            return;
        } else {
            return response.text();
        }
    })
    .then((response) => {
        if (response) {
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
