import {
    calculateDuration, extractDateFromFilename, extractTimeFromImageFileName,
    extractTimeRangeFromVideoFileName,
    formatDateFromCamToGB,
    formatTimeFromCamToUTC,
    Time, TimeDuration,
    TimeRange
} from "./util";

/**
 *
 * @param filename The filename of the media.
 */
function mediaCardBuilder(filename: string): HTMLElement {

    // CREATING DATA TO FILL HTML WITH //

    if (filename.slice(-3) === "jpg") {
        return buildVideoCard(filename)
    }
    else {
        //Assume it's a video otherwise. Saves checking for mp4 and 265
        buildImageCard(filename)
    }
}

function buildVideoCard(filename: string): HTMLElement {

    // CREATING DATA TO FILL HTML WITH //

    const date: string = extractDateFromFilename(filename)

    const mediaType: string = "video"
    let recordType: string = undefined;

    if (filename[0].toLowerCase() === "a") {
        recordType = "alert"
    }
    else { // Assume periodic
        recordType = "periodic"
    }

    const timeRange: TimeRange = extractTimeRangeFromVideoFileName(filename)

    const videoDuration: TimeDuration = calculateDuration(timeRange)

    const startTime: string = formatTimeFromCamToUTC(timeRange.startTime)
    const endTime: string = formatTimeFromCamToUTC(timeRange.endTime)

    const timeRangeString: string = `${startTime} - ${endTime}`

    // CREATING HTML //

    const card = document.createElement("div")
    card.classList.add("card")
    card.classList.add("grid-container") // used to have it be a grid for easier management.
    card.classList.add(recordType)
    card.classList.add(mediaType)

    // FIRST ROW //
    const dateEl = document.createElement("p")
    dateEl.classList.add("time")
    dateEl.textContent = date;

    const timeRangeEl = document.createElement("p")
    timeRangeEl.textContent = timeRangeString

    // SECOND ROW //
    const mediaTypeEl = document.createElement("p")
    mediaTypeEl.textContent = mediaType

    const recordTypeEl = document.createElement("p")
    recordTypeEl.textContent = recordType

    const videoDurationEl = document.createElement("p")
    videoDurationEl.textContent = videoDuration.hours === 0 ? `${videoDuration.minutes}m ${videoDuration.seconds}s` :
        `${videoDuration.hours}h ${videoDuration.minutes}m ${videoDuration.seconds}s`

    // THIRD ROW
    const filenameEl = document.createElement("p")
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

    // CREATING DATA TO FILL HTML WITH //

    const date: string = extractDateFromFilename(filename)

    const time: string = extractTimeFromImageFileName(filename)

    const mediaType: string = "image"
    let recordType: string = undefined;

    if (filename[0].toLowerCase() === "a") {
        recordType = "alert"
    }
    else { // Assume periodic
        recordType = "periodic"
    }

    // CREATING HTML //
    const card = document.createElement("div")
    card.classList.add("card")
    card.classList.add("grid-container") // used to have it be a grid for easier management.
    card.classList.add(recordType)
    card.classList.add(mediaType)

    // FIRST ROW
    const dateEl = document.createElement("p")
    dateEl.classList.add("time")
    dateEl.textContent = date;

    const timeEl = document.createElement("p")
    timeEl.textContent = time

    // SECOND ROW //
    const mediaTypeEl = document.createElement("p")
    mediaTypeEl.textContent = mediaType

    const recordTypeEl = document.createElement("p")
    recordTypeEl.textContent = recordType

    // THIRD ROW
    const filenameEl = document.createElement("p")
    filenameEl.textContent = filename;

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