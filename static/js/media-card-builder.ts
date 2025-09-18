import { formatDateFromCamToGB } from "./util";

/**
 *
 * @param date The date of the media in yyyymmdd format.
 * @param filename The filename of the media.
 */
function mediaCardBuilder(date: string, filename: string): HTMLElement {

    let mediaType: string = undefined; // image or video
    let recordType: string = undefined; // alert (a) or periodic (p)


    if (filename.slice(-3) === "jpg") {
        mediaType = "image"
    }
    else {
        //Assume it's a video otherwise. Saves checking for mp4 and 265
        mediaType =  "video"
    }

    if (filename[0].toLowerCase() === "a") {
        recordType = "alert"
    }
    else { // Assume periodic
        recordType = "periodic"
    }

    const card = document.createElement("div")
    card.classList.add("card")
    card.classList.add(recordType)
    card.classList.add(mediaType)


    const formattedDateEl = document.createElement("p")
    formattedDateEl.textContent = formatDateFromCamToGB(date)

    card.appendChild(formattedDateEl)

    return card
}

