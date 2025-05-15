function sortTable(table, column, asc = true) {
    const sortDir = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));

    const sortedRows = rows.sort((a, b) => {
        let aCol, bCol;
        const aColObj = a.querySelector(`td:nth-child(${column + 1})`);
        const bColObj = b.querySelector(`td:nth-child(${column + 1})`);
        switch (column) {
            case 0:
                aCol = aColObj.textContent.trim().toLowerCase();
                bCol = bColObj.textContent.trim().toLowerCase();
                break;
            case 1:
                aCol = parseInt(aColObj.textContent);
                bCol = parseInt(bColObj.textContent);
                break;
            case 2:
                aCol = parseInt(aColObj.getAttribute("data-duration"));
                bCol = parseInt(bColObj.getAttribute("data-duration"));
                break;
            default:
                aCol = aColObj.textContent.trim();
                bCol = bColObj.textContent.trim();
                break;
        }
        return aCol > bCol ? (1 * sortDir) : (-1 * sortDir);
    });

    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }

    tBody.append(...sortedRows);

    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-asc", asc);
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-desc", !asc);
}

document.querySelectorAll(".sort_table_info th").forEach(headerCell => {
    headerCell.addEventListener("click", () => {
        const tableElement = headerCell.parentElement.parentElement.parentElement;
        const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
        const currentIsAscending = headerCell.classList.contains("th-sort-asc");
        sortTable(tableElement, headerIndex, !currentIsAscending);
    });
    headerCell.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            headerCell.click();
        }
    });
});
