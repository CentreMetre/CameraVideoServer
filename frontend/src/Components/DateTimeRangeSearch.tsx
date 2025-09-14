import { useState } from "react";
import "./DateTimeRangeSearch.css"

function DateTimeRangeSearch() {
    const now: Date = new Date()
    const month: string = now.getMonth().toString().length === 2 ? now.getMonth().toString() : "0" + now.getMonth().toString()
    
    const [startFullDay, setStartFullDay] = useState(false) 
    const [endFullDay, setEndFullDay] = useState(false);

    return (
        <div className="grid">
            <div>
                <label htmlFor="start-date-time">
                    Choose a start date and time to search for:<br />
                </label>

                <input
                    type={startFullDay ? "date" : "datetime-local"}
                    id="start-date-time"
                    name="start-date-time"
                    // value={`${now.getFullYear()}-${month}-${now.getDate()}T${now.getHours()}:${now.getMinutes()}`}
                />
            </div>


            <div>
                <label htmlFor="end-date-time">
                    Choose an end date and time to search for:<br />
                </label>

                <input
                    type={endFullDay ? "date" : "datetime-local"}
                    id="end-date-time"
                    name="end-date-time"
                    // value="2018-06-12T19:30"
                    />
            </div>

            <div>
                <label htmlFor="start-day-full">
                    Search from the start of the day?<br />
                </label>

                <input
                    type="checkbox"
                    id="start-day-full"
                    name="start-day-full"
                    checked={startFullDay}
                    onChange={(e) => setStartFullDay(e.target.checked)}
                />
            </div>

            <div>
                <label htmlFor="end-day-full">
                    Search until the end of the day?<br />
                </label>

                <input
                    type="checkbox"
                    id="end-day-full"
                    name="end-day-full"
                    checked={endFullDay}
                    onChange={(e) => setEndFullDay(e.target.checked)}
                />
            </div>

        </div>
    )
}

export default DateTimeRangeSearch;