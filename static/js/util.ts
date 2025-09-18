/**
 * Converts a date from the cameras format (yyyymmdd) to the gb format (dd/mm/yyyy).
 * @param date The date to convert.
 * @returns The formatted date (dd/mm/yyyy).
 */
export function formatDateFromCamToGB(date: string): string {
    const year: string = date.slice(0,4)
    const month: string = date.slice(4,6)
    const day: string = date.slice(6,8)

    return `${day}/${month}/${year}`;
}

/**
 * Converts a time object into a string of hh:mm:ss, or mm:ss if there is no hours.
 * @param time
 */
export function formatTimeFromCamToUTC(time: Time): string {
    let minutes: string = time.minutes.toString()

    if (minutes.length === 1) {
        minutes = "0" + minutes
    }

    let seconds: string = time.seconds.toString()

    if (seconds.length === 1) {
        seconds = "0" + seconds
    }

    if (time.hours === undefined || time.hours === 0 || time.hours == null) {
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
    const startDate: Date = new Date(`2025-01-01T${st.hours}:${st.minutes}:${st.seconds}`)
    const endDate: Date = new Date(`2025-01-01T${et.hours}:${et.minutes}:${et.seconds}`)

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
 * Extracts the date from a file name. Filename can be either video or image since both start with AYYMMDD_
 * @param filename The name of the file, should be in a format of AYYMMDD_... where A can be anything, YYMMDD is the date format, and the _... doesn't matter.
 * Returns a date from the filename in the format of YYMMDD assuming that's the format the filename came with.
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