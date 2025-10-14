/**
 * Converts a date from the cameras format (yymmdd or yyyymmdd) to the gb format (dd/mm/yyyy).
 * @param date The date to convert.
 * @returns The formatted date (dd/mm/yyyy).
 */
export function formatDateFromCamToGB(date: string): string {
    let year: string;
    let month: string;
    let day: string;

    let fulldate: string;

    if (date.length === 6)
    {
        year = date.slice(0,2)
        month = date.slice(2,4)
        day = date.slice(4,6)
        fulldate = `${day}/${month}/20${year}`; // Don't need to worry about the year starting with 20 for another 75 years.
    }
    else { // assume full yyyymmdd otherwise
        year = date.slice(0,4)
        month = date.slice(4,6)
        day = date.slice(6,8)
        fulldate = `${day}/${month}/${year}`
    }

    return fulldate
}

/**
 * Formats a date from GB format (dd/mm/yyyy) to ISO format (yyyy-mm-dd). Used for Date().
 * @param date The date to format.
 */
export function formatDateFromGBtoISO(date: string): string {
    const parts: string[] = date.split("/")

    const year = parts[2]
    const month = parts[1]
    const day = parts[0]

    return `${year}-${month}-${day}`
}

/**
 *
 * @param time The time in format of hh:mm:ss
 * @param isoDate the date in format of yyyy-mm-dd
 */
export function getUnixTimeFromTimeAndISODate(time: string, isoDate: string): number {
    const date = new Date(`${isoDate}T${time}`)
    const unixTime = Math.floor(date.getTime() / 1000)

    return unixTime;
}

/**
 * Converts a time object into a string of hh:mm:ss, or mm:ss if there is no hours.
 * @param time Can be a time object or a string. If it's a string it must be just the time, not the date as well.
 * @returns The time in a hh:mm:ss format, with 0 padding.
 */
export function formatTimeFromCamToUTC(time: Time | string): string {
    if (typeof time === "string") {
        if (time.length != 6) {
            throw RangeError("The time must be 6 characters long.")
        }
        const hours: string = time.slice(0, 2)
        const minutes : string = time.slice(2, 4)
        const seconds: string = time.slice(4, 6)
        return `${hours}:${minutes}:${seconds}`
    }

    let minutes: string = time.minutes.toString()

    if (minutes.length === 1) {
        minutes = "0" + minutes
    }

    let seconds: string = time.seconds.toString()

    if (seconds.length === 1) {
        seconds = "0" + seconds
    }

    if (time.hours === undefined || time.hours == null) { // Don't exclude == 0 because 00 is needed for time range if it starts after midnight and before 1am
        return `${minutes}:${seconds}`
    }

    let hours: string = time.hours.toString()

    if (hours.length === 1) {
        hours = "0" + hours
    }

    return `${hours}:${minutes}:${seconds}`
}

/**
 * Holds data shaped as time as numbers.
 */
export type Time = {
    hours: number;
    minutes: number;
    seconds: number;
}

/**
 * Holds two different Time objects.
 */
export type TimeRange = {
    startTime: Time;
    endTime: Time;
}

/**
 * Extracts the times (start and end) from a video file name.
 * SHOULD ONLY BE USED WITH A VIDEO FILE NAME.
 * @param videoFileName The file name of the video. Example: A250913_062357_062411.265 (doesn't include path)
 */
export function extractTimeRangeFromVideoFileName(videoFileName: string): TimeRange {

    // File name example: A250913_062357_062411.265
    // Date range is 062357_062411 part

    // Remove extension from end time
    const fileNameNoExt: string = videoFileName.split(".")[0]

    // Split the date and times
    const times: string[] = fileNameNoExt.split("_")

    // [1] and [2] is used instead of [0] and [1] because the date is in the [0] index.
    const startTime: Time = {
        hours: Number(times[1][0] + times[1][1]),
        minutes: Number(times[1][2] + times[1][3]),
        seconds: Number(times[1][4] + times[1][5]),
    }

    const endTime: Time = {
        hours: Number(times[2][0] + times[2][1]),
        minutes: Number(times[2][2] + times[2][3]),
        seconds: Number(times[2][4] + times[2][5]),
    };

    return { startTime, endTime }
}

/**
 * Time duration is for holding the amount of time between two times. Same shape as Time.
 */
export type TimeDuration = Time

/**
 * Calculates the time range of two given times.
 * @param timeRange A TimeRange object with the start and end times.
 * @return A TimeDuration object with the time difference. Numbers do not have `0` padding (leading zeros).
 */
export function calculateDuration(timeRange: TimeRange): TimeDuration {

     // Start Time
    const st: Time = timeRange.startTime

    // End Time
    const et: Time = timeRange.endTime

    // Actual date doesn't matter, as long as they are the same in each
    const startDate: Date = new Date(`2025-01-01T${padTime(st.hours)}:${padTime(st.minutes)}:${padTime(st.seconds)}`)
    const endDate: Date = new Date(`2025-01-01T${padTime(et.hours)}:${padTime(et.minutes)}:${padTime(et.seconds)}`)

    const diffInMilliseconds: number = endDate.getTime() - startDate.getTime()

    // Calculate hours by dividing total milliseconds by ms in one hour
    const hours = Math.floor(diffInMilliseconds / (1000 * 60 * 60));

    // Calculate remaining minutes after removing whole hours
    const minutes = Math.floor((diffInMilliseconds % (1000 * 60 * 60)) / (1000 * 60));

    // Calculate remaining seconds after removing whole minutes
    const seconds = Math.floor((diffInMilliseconds % (1000 * 60)) / 1000);


    return { hours: hours, minutes: minutes, seconds: seconds }
}

/**
 * Converts a time duration to just seconds.
 * @param timeDuration A TimeDuration object that holds the time
 */
export function convertDurationToSeconds(timeDuration: TimeDuration): number {
    const hoursToSecs = timeDuration.hours * 3600 //should be 0 but used anyway.
    const minsToSecs = timeDuration.minutes * 60
    return hoursToSecs + minsToSecs + timeDuration.seconds
}

/**
 * Extracts the date from a file name. Filename can be either video or image since both start with AYYMMDD_
 * @param filename The name of the file, should be in a format of AYYMMDD_... where A can be anything, YYMMDD is the date format, and the _... doesn't matter.
 * @returns a date from the filename in the format of YYMMDD assuming that's the format the filename came with.
 */
export function extractDateFromFilename(filename: string) {
    return filename.substring(1, 7)
}

/**
 * Returns the time from the filename of an image.
 * @param filename The filename of the file to get the date of.
 */
export function extractTimeFromImageFileName(filename: string): string {
    return filename.substring(7, 13) // Image names have 00 at the end, e.g. A25091715443100.jpg, so substring is easier than removing extension and date.
}

/**
 * Pad a time so that it will always start with 0 if it is a single digit0
 * @param time The number to pad.
 */
export function padTime(time: number): string {
    return time.toString().padStart(2, '0');
}

/**
 * Extracts the filename from a path of media from the camera, excluding extension.
 * @param path The path to extract the filename from
 * @returns The filename excluding the extension. e.g. 20250923/record001/A250923_150431_150445.265 turns into A250923_150431_150445
 */
export function extract_filename_from_path_excluding_extension(path: string): string {
    const parts: string[] = path.split("/")
    const filenameExt: string[] = parts[parts.length - 1].split(".")
    const filename: string = filenameExt[0]
    return filename
}

/**
 * Extracts the filename from a path of media from the camera, including extension.
 * @param path The path to extract the filename from
 * @returns The filename including the extension. e.g. 20250923/record001/A250923_150431_150445.265 turns into A250923_150431_150445.265
 */
export function extract_filename_from_path(path: string): string {
    const parts: string[] = path.split("/")
    return parts[parts.length - 1]
}
