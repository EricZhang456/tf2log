"use strict";
const showSourceTVButton = (serverIP, serverPort) => {
    fetch(`/info/sourcetv/${serverIP}?port=${serverPort}`, {
        method: "GET",
        headers: {
            "x-get-sourcetv": "1"
        }
    })
    .then((response) => {
        if (!response.ok) {
            return;
        } else {
            return response.json();
        }
    })
    .then((response) => {
        if (response) {
            const sourceTVButton = document.querySelector(".info_header_sourcetv");
            sourceTVButton.setAttribute("href", `steam://connect/${response.address}`);
            sourceTVButton.style.setProperty("display", "flex");
            if (response.password) {
                document.querySelector(".info_header_sourcetv_password").style.setProperty("display", "block");
            }
        }
    })
}

document.addEventListener("DOMContentLoaded", () => {
    const sourceTVScript = document.getElementById("info_server_sourcetv_script")
    showSourceTVButton(sourceTVScript.getAttribute("x-server-ip"), sourceTVScript.getAttribute("x-sourcetv-port"));
});
