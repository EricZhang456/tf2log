function populateMapThumbnail(map_name) {
    fetch(`/info/thumbnail/${map_name}`)
    .then(response => {
        if (response.ok) {
            return response.text();
        }
        return Promise.reject(response);
    })
    .then(response => {
        const infoHeader = document.querySelector(".info_header_server");
        infoHeader.style.backgroundImage = `url(${response})`;
        infoHeader.style.backgroundPosition = "center";
        infoHeader.style.backgroundSize = "cover";
    })
    .catch(() => {
        return;
    });
}

document.addEventListener("DOMContentLoaded", () => populateMapThumbnail(document.getElementById("info_map_background_script").getAttribute("data-map-name")));
