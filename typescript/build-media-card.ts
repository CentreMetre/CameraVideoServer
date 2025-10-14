import {
    calculateDuration, convertDurationToSeconds,
    extractDateFromFilename,
    extractTimeFromImageFileName,
    extractTimeRangeFromVideoFileName,
    formatDateFromCamToGB,
    formatDateFromGBtoISO,
    formatTimeFromCamToUTC,
    getUnixTimeFromTimeAndISODate,
    TimeDuration,
    TimeRange
} from "./util.js";

/**
 *
 * @param filename The filename of the media.
 */
export function buildMediaCard(filename: string): HTMLElement {

    // console.debug(filename)

    if (filename.slice(-3).toLowerCase() === "jpg") {
        return buildImageCard(filename)
    }
    else {
        //Assume it's a video otherwise. Saves checking for mp4 and 265
        return buildVideoCard(filename)
    }
}

function buildVideoCard(filename: string): HTMLElement {

    // console.debug("In buildVideoCard for " + filename)

    // CREATING DATA TO FILL HTML WITH //

    let date: string = extractDateFromFilename(filename)
    date = formatDateFromCamToGB(date)

    const mediaType: "video" = "video"
    const mediaTypeCapital: "Video" = "Video"
    let recordType: string | undefined = undefined;
    let recordTypeCapital: string | undefined = undefined

    if (filename[0].toLowerCase() === "a") {
        recordType = "alert"
        recordTypeCapital = "Alert"
    }
    else { // Assume periodic
        recordType = "periodic"
        recordTypeCapital = "Periodic"
    }

    const timeRange: TimeRange = extractTimeRangeFromVideoFileName(filename)

    const videoDuration: TimeDuration = calculateDuration(timeRange)

    const videoDurationSeconds = convertDurationToSeconds(videoDuration)

    const startTime: string = formatTimeFromCamToUTC(timeRange.startTime)
    const endTime: string = formatTimeFromCamToUTC(timeRange.endTime)

    const timeRangeString: string = `${startTime} - ${endTime}`

    // CREATING HTML //

    const card = document.createElement("div")
    card.classList.add("card")
    card.classList.add("grid-container") // used to have it be a grid for easier management.
    card.classList.add(recordType)
    card.classList.add(mediaType)

    // Use start time since that makes more sense for searching/filtering/sorting
    card.setAttribute("data-time", getUnixTimeFromTimeAndISODate(startTime, formatDateFromGBtoISO(date)).toString())
    card.setAttribute("data-media-type", mediaType)
    card.setAttribute("data-record-type", recordType)
    card.setAttribute("data-duration-seconds", videoDurationSeconds.toString())


    // FIRST ROW //
    const dateEl = document.createElement("p")
    dateEl.classList.add("date")
    dateEl.textContent = date;

    const timeRangeEl = document.createElement("p")
    timeRangeEl.classList.add("time")
    timeRangeEl.textContent = timeRangeString

    // SECOND ROW //
    const mediaTypeEl = document.createElement("p")
    mediaTypeEl.classList.add("media-type")
    mediaTypeEl.textContent = mediaTypeCapital

    const recordTypeEl = document.createElement("p")
    recordTypeEl.classList.add("record-type")
    recordTypeEl.textContent = recordTypeCapital

    const videoDurationEl = document.createElement("p")
    videoDurationEl.classList.add("duration")
    videoDurationEl.textContent = videoDuration.hours === 0 ? `${videoDuration.minutes}m ${videoDuration.seconds}s` :
        `${videoDuration.hours}h ${videoDuration.minutes}m ${videoDuration.seconds}s`

    // THIRD ROW
    const filenameEl = document.createElement("p")
    filenameEl.classList.add("filename")
    filenameEl.textContent = filename;

    // FIRST ROW
    card.appendChild(dateEl)
    card.appendChild(timeRangeEl)

    // SECOND ROW
    card.appendChild(mediaTypeEl)
    card.appendChild(recordTypeEl)
    card.appendChild(videoDurationEl)

    // THIRD ROW
    card.appendChild(filenameEl)

    return card
}

function buildImageCard(filename: string): HTMLElement {

    // console.debug("In buildImageCard for " + filename)

    // CREATING DATA TO FILL HTML WITH //

    let  date: string = extractDateFromFilename(filename)
    date = formatDateFromCamToGB(date)

    let time: string = extractTimeFromImageFileName(filename)
    time = formatTimeFromCamToUTC(time)

    const mediaType: "image" = "image"
    const mediaTypeCapital: "Image" = "Image"
    let recordType: string | undefined = undefined;
    let recordTypeCapital: string | undefined = undefined

    if (filename[0].toLowerCase() === "a") {
        recordType = "alert"
        recordTypeCapital = "Alert"
    }
    else { // Assume periodic
        recordType = "periodic"
        recordTypeCapital = "Periodic"
    }

    // CREATING HTML //
    const card = document.createElement("div")
    card.classList.add("card")
    card.classList.add("grid-container") // used to have it be a grid for easier management.
    card.classList.add(recordType)
    card.classList.add(mediaType)

    card.setAttribute("data-time", getUnixTimeFromTimeAndISODate(time, formatDateFromGBtoISO(date)).toString())
    card.setAttribute("data-media-type", mediaType)
    card.setAttribute("data-record-type", recordType)

    // FIRST ROW
    const dateEl = document.createElement("p")
    dateEl.classList.add("date")
    dateEl.textContent = date

    const timeEl = document.createElement("p")
    timeEl.classList.add("time")
    timeEl.textContent = time

    // SECOND ROW //
    const mediaTypeEl = document.createElement("p")
    mediaTypeEl.classList.add("media-type")
    mediaTypeEl.textContent = mediaTypeCapital

    const recordTypeEl = document.createElement("p")
    recordTypeEl.classList.add("record-type")
    recordTypeEl.textContent = recordTypeCapital

    // THIRD ROW
    const filenameEl = document.createElement("p")
    filenameEl.classList.add("filename")
    filenameEl.textContent = filename

    // FIRST ROW
    card.appendChild(dateEl)
    card.appendChild(timeEl)

    // SECOND ROW
    card.appendChild(mediaTypeEl)
    card.appendChild(recordTypeEl)

    // THIRD ROW
    card.appendChild(filenameEl)

    return card
}

/**
 *
 * @param path The path of the file. Example: "20251011/images000/A25101106590700.jpg". Can be retrieved from the server.
 * @param action Thea action to do. Is either "view" or "download"
 */
export function buildActionButton(path: string, action: "view" | "download"): HTMLElement {
    if (action != "view" && action != "download") {
        throw new Error("'action' parameter must be 'view' or 'download'")
    }
    const path_parts = path.split("/")

    let aEl: HTMLAnchorElement = document.createElement("a")

    aEl.href = `/file/${path_parts[0]}/${path_parts[1]}/${path_parts[2]}/${action}`
    // aEl.href = `/file/${path}/${action}`

    let buttonEl: HTMLButtonElement = document.createElement("button")
    buttonEl.classList.add("action-button")
    buttonEl.classList.add(`action-${action}`)

    if (action === "view") {
        buttonEl.textContent = "View"
    }
    else {
        buttonEl.textContent = "Download"
    }

    aEl.appendChild(buttonEl)

    return aEl
}

/**
 * Builds a div that contains both view and download buttons
 * @param path The path of the file the button is being created for.
 */
export function buildActionButtonsDiv(path: string): HTMLDivElement {
    const viewButton = buildActionButton(path, "view")
    const downloadButton = buildActionButton(path, "download")

    const buttonRowEl = document.createElement("div")
    buttonRowEl.classList.add("actions")

    buttonRowEl.appendChild(viewButton)
    buttonRowEl.appendChild(downloadButton)

    return buttonRowEl;
}

export function buildFullCardContainer(filename: string, path: string): HTMLDivElement {
    const mediaCard = buildMediaCard(filename)
    const buttons = buildActionButtonsDiv(path)

    const fullContainer = document.createElement("div")
    fullContainer.appendChild(mediaCard)
    fullContainer.appendChild(buttons)

    fullContainer.classList.add("card-container")

    // console.debug(mediaCard.getAttribute("data-time"))
    // console.debug(mediaCard.getAttribute("data-media-type"))
    // console.debug(mediaCard.getAttribute("data-record-type"))

    //Setting data-* attributes to outer card container for searching and filtering
    fullContainer.setAttribute("data-time", mediaCard.getAttribute("data-time")!)
    fullContainer.setAttribute("data-media-type", mediaCard.getAttribute("data-media-type")!)
    fullContainer.setAttribute("data-record-type", mediaCard.getAttribute("data-record-type")!)

    // console.debug(mediaCard.getAttribute("data-media-type"))

    if (mediaCard.getAttribute("data-media-type") === "video") {
        // console.debug("in video in buildFullCardContainer")
        fullContainer.setAttribute("data-duration-seconds", mediaCard.getAttribute("data-duration-seconds")!)
        mediaCard.removeAttribute("data-duration-seconds")
    }

    //Removing data-* from inner card since they aren't needed any more
    mediaCard.removeAttribute("data-time")
    mediaCard.removeAttribute("data-media-type")
    mediaCard.removeAttribute("data-record-type")

    return fullContainer
}
