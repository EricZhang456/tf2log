function populateMapThumbnail(map_name) {
    fetch(`/info/thumbnail/${map_name}`, {
        method: "GET",
        headers: {
            "x-get-thumbnail": "1"
        }
    })
    .then(response => {
        if (response.ok) {
            return response.text();
        }
        return Promise.reject(response);
    })
    .then(response => {
        const infoHeader = document.querySelector(".info_header_server");
        infoHeader.style.setProperty("background-image", `url(${response})`);
        infoHeader.style.setProperty("background-position", "center");
        infoHeader.style.setProperty("background-size", "cover");
    })
    .catch(() => {
        return;
    });
}

document.addEventListener("DOMContentLoaded", () => populateMapThumbnail(document.getElementById("info_map_background_script").getAttribute("data-map-name")));
