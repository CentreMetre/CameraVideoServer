import {
    calculateDuration,
    extractDateFromFilename,
    extractTimeFromImageFileName,
    extractTimeRangeFromVideoFileName, formatDateFromCamToGB,
    formatTimeFromCamToUTC,
    TimeDuration,
    TimeRange
} from "./util.js";

/**
 *
 * @param filename The filename of the media.
 */
export function buildMediaCard(filename: string): HTMLElement {

    console.debug(filename)

    if (filename.slice(-3).toLowerCase() === "jpg") {
        return buildImageCard(filename)
    }
    else {
        //Assume it's a video otherwise. Saves checking for mp4 and 265
        return buildVideoCard(filename)
    }
}

function buildVideoCard(filename: string): HTMLElement {

    console.debug("In buildVideoCard for " + filename)

    // CREATING DATA TO FILL HTML WITH //

    let date: string = extractDateFromFilename(filename)
    date = formatDateFromCamToGB(date)

    const mediaType: string = "video"
    const mediaTypeCapital: string = "Video"
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

    console.debug("In buildImageCard for " + filename)

    // CREATING DATA TO FILL HTML WITH //

    let  date: string = extractDateFromFilename(filename)
    date = formatDateFromCamToGB(date)

    let time: string = extractTimeFromImageFileName(filename)
    time = formatTimeFromCamToUTC(time)

    const mediaType: string = "image"
    const mediaTypeCapital: string = "Image"
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

    // FIRST ROW
    const dateEl = document.createElement("p")
    dateEl.classList.add("date")
    dateEl.textContent = date;

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