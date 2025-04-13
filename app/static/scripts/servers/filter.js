const disabledTextColor = "#aba8a5";
const enabledTextColor = "#fff";

const filterServerFull = document.getElementById("server_filter_full");
const filterHasUserPlaying = document.getElementById("server_filter_has_users_playing");
const filterNoPassword = document.getElementById("server_filter_no_password");

const filterPresetVanilla = document.getElementById("server_filter_vanilla");
const filterPresetSemiVanilla = document.getElementById("server_filter_vanilla_custom");
const filterPresetCustom = document.getElementById("server_filter_custom");
const filterPresetAll = document.getElementById("server_filter_all");

const filterAlltalk = document.getElementById("server_filter_alltalk");
const filterNocrits = document.getElementById("server_filter_nocrits");
const filterDmgSpread = document.getElementById("server_filter_dmgspread");
const filterIncreasedMaxPlayers = document.getElementById("server_filter_increased_maxplayers");
const filterNoRespawnTime = document.getElementById("server_filter_norespawntime");
const filterRespawnTimes = document.getElementById("server_filter_respawntimes");
const filterFriendlyFire = document.getElementById("server_filter_friendlyfire");
const filterGravity = document.getElementById("server_filter_gravity");
const filterReplay = document.getElementById("server_filter_replay");

const filterRegion = document.getElementById("server_filter_region_select");

const filterForm = document.querySelector(".server_filter_form");
const filterHint = document.getElementById("server_filter_hint");
const filterButton = document.getElementById("server_filter_button");

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const queryServerFull = urlParams.get("not_full");
const queryHasUserPlaying = urlParams.get("has_user_playing");
const queryNoPassword = urlParams.get("password");
const queryPreset = urlParams.get("vanilla");
const queryAlltalk = urlParams.get("alltalk")
const queryNocrits = urlParams.get("nocrits")
const queryDmgSpread = urlParams.get("dmgspread");
const queryIncreasedMaxPlayers = urlParams.get("increased_maxplayers");
const queryNoRespawnTime = urlParams.get("norespawntime");
const queryRespawnTimes = urlParams.get("respawntimes");
const queryFriendlyFire = urlParams.get("friendlyfire");
const queryGravity = urlParams.get("gravity");
const queryReplay = urlParams.get("replay");
const queryRegion = urlParams.get("region");

const populateFilteredServerCount = () => {
    const filteredServerCount = document.querySelectorAll(".server_list_item").length;
    document.getElementById("server_list_filtered_server_count").innerHTML = `(${filteredServerCount})`;
}

const setFilterFormInput = () => {
    filterServerFull.checked = Boolean(parseInt(queryServerFull));
    filterHasUserPlaying.checked = Boolean(parseInt(queryHasUserPlaying));
    filterNoPassword.checked = Boolean(parseInt(queryNoPassword));
    filterAlltalk.checked = Boolean(parseInt(queryAlltalk));
    filterNocrits.checked = Boolean(parseInt(queryNocrits));
    filterDmgSpread.checked = Boolean(parseInt(queryDmgSpread));
    filterIncreasedMaxPlayers.checked = Boolean(parseInt(queryIncreasedMaxPlayers));
    filterNoRespawnTime.checked = Boolean(parseInt(queryNoRespawnTime));
    filterRespawnTimes.checked = Boolean(parseInt(queryRespawnTimes));
    filterFriendlyFire.checked = Boolean(parseInt(queryFriendlyFire));
    filterGravity.checked = Boolean(parseInt(queryGravity));
    filterReplay.checked = Boolean(parseInt(queryReplay));
    if (queryPreset) {
        switch (queryPreset) {
            case "1": filterPresetVanilla.checked = true; disableCustomFilters(); break;
            case "2": filterPresetSemiVanilla.checked = true; break;
            case "3": filterPresetCustom.checked = true; break;
            case "4": filterPresetAll.checked = true; break;
            default: filterPresetVanilla.checked = true; break;
        }
    }
    if (queryRegion) {
        switch (queryRegion) {
            case "-1": filterRegion.selectedIndex = 0; break;
            case "0": filterRegion.selectedIndex = 1; break;
            case "1": filterRegion.selectedIndex = 2; break;
            case "2": filterRegion.selectedIndex = 3; break;
            case "3": filterRegion.selectedIndex = 4; break;
            case "4": filterRegion.selectedIndex = 5; break;
            case "5": filterRegion.selectedIndex = 6; break;
            case "6": filterRegion.selectedIndex = 7; break;
            case "7": filterRegion.selectedIndex = 8; break;
            case "255": filterRegion.selectedIndex = 9; break;
            default: filterRegion.selectedIndex = 9; break;
        }
    }

    if (queryHasUserPlaying === null) {
        filterHasUserPlaying.checked = true;
    }
    if (queryPreset === null) {
        filterPresetVanilla.checked = true;
        disableCustomFilters();
    }
    if (queryRegion === null) {
        filterRegion.selectedIndex = 0;
    }
}

const toggleFilters = () => {
    if (filterForm.style.display === "none") {
        filterForm.style.display = "flex";
    } else {
        filterForm.style.display = "none";
    }
}

const reenableCustomFilters = () => {
    const targetElements = [filterNocrits, filterDmgSpread, filterNoRespawnTime, filterRespawnTimes, 
                            filterFriendlyFire, filterGravity, filterGravity];
    targetElements.forEach((item) => {
        item.disabled = false;
        item.labels.item(0).style.color = enabledTextColor;
    });
}

const disableCustomFilters = () => {
    const targetElements = [filterNocrits, filterDmgSpread, filterNoRespawnTime, filterRespawnTimes, 
                            filterFriendlyFire, filterGravity, filterGravity];
    targetElements.forEach((item) => {
        item.checked = false;
        item.disabled = true;
        item.labels.item(0).style.color = disabledTextColor;
    });
}

filterPresetVanilla.addEventListener("click", () => disableCustomFilters());
filterPresetSemiVanilla.addEventListener("click" , () => reenableCustomFilters());
filterPresetCustom.addEventListener("click" , () => reenableCustomFilters());
filterPresetAll.addEventListener("click" , () => reenableCustomFilters());

const getPreset = () => {
    const filterPresets = [filterPresetVanilla, filterPresetSemiVanilla, filterPresetCustom, filterPresetAll];
    let presetValue;
    filterPresets.forEach((item) => {
        if (item.checked) {
            presetValue = item.value;
        }
    });
    return presetValue;
}

const constructFilterUrlParams = () => {
    const targetFilterElements = [filterServerFull, filterHasUserPlaying, filterNoPassword, filterAlltalk,
                                filterNocrits, filterDmgSpread, filterIncreasedMaxPlayers, filterNoRespawnTime,
                                filterRespawnTimes, filterFriendlyFire, filterGravity, filterReplay]
    let targetUrl = new URL(location.protocol + '//' + location.host + location.pathname);
    targetFilterElements.forEach((item) => {
        targetUrl.searchParams.set(item.value, +item.checked);
    });
    targetUrl.searchParams.set("vanilla", getPreset());
    targetUrl.searchParams.set("region", filterRegion.value);
    return targetUrl.toString();
}

const filterApply = () => {
    const filteredURL = constructFilterUrlParams();
    const target = document.querySelector(".target");
    const fetchingHint = document.querySelector(".server_list_fetching");
    const searchBox = document.getElementById("server_search_box");
    const sortPlayerCountButton = document.querySelector(".server_list_player_count_hint");
    const sortNameButton = document.querySelector(".server_list_sort_name");
    const sortMapButton = document.querySelector(".server_list_sort_map");
    const sortGameModeButton = document.querySelector(".server_list_sort_mode");
    const sortRegionButton = document.querySelector(".server_list_sort_region");
    searchBox.value = "";
    searchBox.style.color = "#aba8a5";
    searchBox.style.fontStyle = "italic";
    const sortElements = [sortPlayerCountButton, sortNameButton, sortMapButton, sortGameModeButton, sortRegionButton];
    sortElements.forEach((item) => {
       item.classList.remove("sort_asc", "sort_desc"); 
    });
    
    fetchingHint.style.display = "block";
    document.getElementById("server_list_filtered_server_count").innerHTML = "";
    target.innerHTML = "";
    fetch(filteredURL, {
        method: "GET",
        headers: {
            "x-fetch-subview": "1"
        }
    })
    .then((response) => response.text())
    .then((response) => {
        fetchingHint.style.display = "none";
        target.innerHTML = response;
        window.history.pushState({}, '', filteredURL);
        populateFilteredServerCount();
    });
}

const populateFilterHint = () => {
    let filterHintText = new Array();
    const targetElements = [filterServerFull, filterHasUserPlaying, filterNoPassword,
                            filterPresetVanilla, filterPresetSemiVanilla, filterPresetCustom,
                            filterPresetAll, filterAlltalk, filterNocrits, filterDmgSpread,
                            filterIncreasedMaxPlayers, filterNoRespawnTime, filterRespawnTimes,
                            filterFriendlyFire, filterGravity, filterReplay]
    targetElements.forEach((item) => {
        if (item.checked) {
            filterHintText.push(item.labels.item(0).innerHTML);
        }
    });
    if (filterRegion.selectedIndex != 0) {
        filterHintText.push(filterRegion.options[filterRegion.selectedIndex].text);
    }
    filterHint.innerHTML = filterHintText.join(", ");
}

filterForm.addEventListener("change", () => {
    populateFilterHint();
});

document.addEventListener("DOMContentLoaded", () => {
    document.querySelector(".server_filter").style.display = "flex";
    filterForm.style.display = "none";
    setFilterFormInput();
    populateFilteredServerCount();
    populateFilterHint();
});
