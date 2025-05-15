const serverListContainer = document.querySelector(".server_list_servers");
const sortPlayerCountButton = document.querySelector(".server_list_player_count_hint");
const sortNameButton = document.querySelector(".server_list_sort_name");
const sortMapButton = document.querySelector(".server_list_sort_map");
const sortGameModeButton = document.querySelector(".server_list_sort_mode");
const sortRegionButton = document.querySelector(".server_list_sort_region");

function sortServerItems(asc = true, sortColumn) {
    const sortDir = asc ? 1 : -1;
    const serverItems = Array.from(document.querySelectorAll(".server_list_item:not(.hide)"));
    const sortedServerItems = serverItems.sort((a, b) => {
        let aValue, bValue;
        switch (sortColumn) {
            case 1:
                aValue = parseInt(a.getAttribute("data-player-count"));
                bValue = parseInt(b.getAttribute("data-player-count"));
                break;
            case 2:
                aValue = a.getAttribute("data-server-name").trim().toLowerCase();
                bValue = b.getAttribute("data-server-name").trim().toLowerCase();
                break;
            case 3:
                aValue = a.getAttribute("data-server-readable-map").trim().toLowerCase();
                bValue = b.getAttribute("data-server-readable-map").trim().toLowerCase();
                break;
            case 4:
                aValue = a.getAttribute("data-server-mode").trim().toLowerCase();
                bValue = b.getAttribute("data-server-mode").trim().toLowerCase();
                break;
            case 5:
                aValue = a.getAttribute("data-server-region").trim().toLowerCase();
                bValue = b.getAttribute("data-server-region").trim().toLowerCase();
                break;
        }
        return aValue > bValue ? (1 * sortDir) : (-1 * sortDir);
    });
    while (serverListContainer.firstChild) {
        serverListContainer.removeChild(serverListContainer.firstChild);
    }
    serverListContainer.append(...sortedServerItems);
    const target = [sortPlayerCountButton, sortNameButton, sortMapButton, sortGameModeButton, sortRegionButton];
    target.forEach(item => item.classList.remove("sort_asc", "sort_desc"));
    switch (sortColumn) {
        case 1:
            sortPlayerCountButton.classList.toggle("sort_asc", asc);
            sortPlayerCountButton.classList.toggle("sort_desc", !asc);
            break;
        case 2:
            sortNameButton.classList.toggle("sort_asc", asc);
            sortNameButton.classList.toggle("sort_desc", !asc);
            break;
        case 3:
            sortMapButton.classList.toggle("sort_asc", asc);
            sortMapButton.classList.toggle("sort_desc", !asc);
            break;
        case 4:
            sortGameModeButton.classList.toggle("sort_asc", asc);
            sortGameModeButton.classList.toggle("sort_desc", !asc);
            break;
        case 5:
            sortRegionButton.classList.toggle("sort_asc", asc);
            sortRegionButton.classList.toggle("sort_desc", !asc);
            break;
    }
}

sortPlayerCountButton.addEventListener("click", () => sortServerItems(!sortPlayerCountButton.classList.contains("sort_asc"), 1));

sortNameButton.addEventListener("click", () => sortServerItems(!sortNameButton.classList.contains("sort_asc"), 2));

sortMapButton.addEventListener("click", () => sortServerItems(!sortMapButton.classList.contains("sort_asc"), 3));

sortGameModeButton.addEventListener("click", () => sortServerItems(!sortGameModeButton.classList.contains("sort_asc"), 4));

sortRegionButton.addEventListener("click", () => sortServerItems(!sortRegionButton.classList.contains("sort_asc"), 5));

const sortButtons = [sortPlayerCountButton, sortNameButton, sortMapButton, sortGameModeButton, sortRegionButton];
sortButtons.forEach(item => {
    item.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            item.click();
        }
    });
});
