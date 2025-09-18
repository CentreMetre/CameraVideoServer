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
 * Holds data shaped as time as numbers.
 */
export type Time = {
    hours: number;
    minutes: number;
    seconds: number;
}


export type TimeRange = {
    startTime: Time;
    endTime: Time;
}

export function extractTimeRangeFromVideoFileName(videoFileName: string): TimeRange {
    // File name example: A250913_062357_062411.265
    // Date range is 062357_062411 part

    // Remove extension from end time
    const fileNameNoExt: string = videoFileName.split(".")[0]

    // Split the date and times
    const times: string[] = fileNameNoExt.split("_")



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
    // // 3600 secs in 1 hour
    // // 60 secs in 1 min
    //
    // Start Time
    const st: Time = timeRange.startTime

    // End Time
    const et: Time = timeRange.endTime

    // // These are absolute times, e.g. 09:05:23
    // const startInSeconds = st.hours * 3600 + st.minutes * 60 + st.seconds
    // const endInSeconds = et.hours * 3600 + et.minutes * 60 + et.seconds
    //
    // // Should be less than 3600, but will assume more than an hour can exist, I don't know full capabilities of camera.
    // const deltaInSeconds: number = endInSeconds - startInSeconds

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