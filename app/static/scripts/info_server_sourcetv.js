const showSourceTVButton = (serverIP, serverPort) => {
    fetch(`/info/sourcetv/${serverIP}?port=${serverPort}`)
    .then((response) => response.json())
    .then((response) => {
        if(response) {
            const sourceTVButton = document.querySelector(".info_header_sourcetv");
            sourceTVButton.setAttribute("href", `steam://connect/${response.address}`);
            sourceTVButton.style.setProperty("display", "flex");
            if(response.password) {
                document.querySelector(".info_header_sourcetv_password").style.setAttribute("display", "block");
            }
        }
    })
}

document.addEventListener("DOMContentLoaded", () => {
    const sourceTVScript = document.getElementById("info_server_sourcetv_script")
    showSourceTVButton(sourceTVScript.getAttribute("x-server-ip"), sourceTVScript.getAttribute("x-server-port"));
});
