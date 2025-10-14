import { buildFullCardContainer } from "./build-media-card.js"
import { extract_filename_from_path, formatDateFromCamToGB } from "./util.js";

const path = window.location.pathname; // Get the path name to get the date
console.debug(path)

const path_parts = path.split("/");
const dateCamFormat = path_parts[path_parts.length - 1] // Split and extract just the date (assumes date is at the end, as it should be unless the endpoint changes)
const dateGBFormat = formatDateFromCamToGB(dateCamFormat)

console.debug(dateCamFormat)

const cardListEl: HTMLDivElement = document.getElementById("card-list") as HTMLDivElement

const filterMediaTypeSelectEl: HTMLSelectElement = document.getElementById("filter-media-type") as HTMLSelectElement
const filterRecordTypeSelectEl: HTMLSelectElement = document.getElementById("filter-record-type") as HTMLSelectElement
const filterResetButtonEl: HTMLButtonElement = document.getElementById("filter-reset") as HTMLButtonElement
const dateEl: HTMLHeadElement = document.getElementById("page-date") as HTMLHeadElement
dateEl.textContent = dateGBFormat
/**
 * Used to show a message to the user when processing data, e.g. a request, retrieval, etc.
 */
const cardMessage: HTMLHeadElement = document.createElement("h3")

filterMediaTypeSelectEl.addEventListener("change", applyTransformationToMediaList)
filterRecordTypeSelectEl.addEventListener("change", applyTransformationToMediaList)
filterResetButtonEl.addEventListener("click", resetFilters)

let masterCardListEls: HTMLDivElement;
let transformedList: HTMLDivElement[];

async function initialiseCards() {
    showCardMessage("Retrieving Data")
    wait(1000).then(() => {
        console.log("1 second passed");
    });
    const response = await fetch(`/api/${dateCamFormat}/paths`)

    showCardMessage("Processing Data")
    wait(1000).then(() => {
        console.log("1 second passed");
    });

    const paths = await response.json()

    emptyCardList()
    for (const path of paths) {
        if (path === "") { // used as temp fix until db is fixed
            continue

        }
        const filename = extract_filename_from_path(path)
        let cardContainer = buildFullCardContainer(filename, path)
        cardListEl.appendChild(cardContainer)
    }

    masterCardListEls = cardListEl.cloneNode(true) as HTMLDivElement
}

function applyTransformationToMediaList() {
    showCardMessage("Applying Query")
    wait(1000).then(() => {
        console.log("1 second passed");
    });
    //Create deep copy so to not edit original list
    transformedList = Array.from(masterCardListEls.children).map(child => child.cloneNode(true) as HTMLDivElement); //.map needed to create more deep copies from master list

    const filterBy: string[] = [];
    if (filterMediaTypeSelectEl.value === "all") {
        filterBy.push("image")
        filterBy.push("video")
    }
    else {
        filterBy.push(filterMediaTypeSelectEl.value)
    }

    if (filterRecordTypeSelectEl.value === "all") {
        filterBy.push("periodic")
        filterBy.push("alert")
    }
    else {
        filterBy.push(filterRecordTypeSelectEl.value)
    }

    let shownCardAmount = 0

    for (const child of transformedList) {
        if (!filterBy.includes(child.getAttribute("data-media-type")!)) {
            child.classList.add("hidden")
        }
        else {
            shownCardAmount++
        }
    }

    for (const child of transformedList) {
        if (!filterBy.includes(child.getAttribute("data-record-type")!)) {
            child.classList.add("hidden")
        }
        else {
            shownCardAmount++
        }
    }

    emptyCardList()

    for (const child of transformedList) {
        cardListEl.appendChild(child);
    }
}


function resetFilters() {
    filterMediaTypeSelectEl.value = "all";
    filterRecordTypeSelectEl.value = "all";
    applyTransformationToMediaList();
}

function showCardMessage(message: string): void {
    cardListEl.innerHTML = ""
    cardMessage.textContent = message
    cardListEl.appendChild(cardMessage)
}

function emptyCardList() {
    cardListEl.innerHTML = ""
}

function wait(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

initialiseCards()
