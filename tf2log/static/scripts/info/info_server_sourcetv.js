function showSourceTVButton(serverIP, serverPort) {
    fetch(`/info/sourcetv/${serverIP}?port=${serverPort}`, {
        method: "GET",
        headers: {
            "x-get-sourcetv": "1"
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return Promise.reject(response);
    })
    .then(response => {
        const sourceTVButton = document.querySelector(".info_header_sourcetv");
        sourceTVButton.setAttribute("href", `steam://connect/${response.address}`);
        sourceTVButton.style.display = "flex";
        if (response.password) {
            document.querySelector(".info_header_sourcetv_password").style.display = "block";
        }
    })
    .catch(() => {
        return;
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const sourceTVScript = document.getElementById("info_server_sourcetv_script");
    showSourceTVButton(sourceTVScript.getAttribute("data-server-ip"), sourceTVScript.getAttribute("data-sourcetv-port"));
});
