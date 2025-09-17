

function videoCardBuilder(date: string, media_type: string, filename: string): HTMLElement {
    const card = document.createElement("div")
    card.classList.add("card")

    const formatted_date = document.createElement("p")
    formatted_date.textContent = format_date(date)


    return card
}

function format_date(date: string): string {
    const year: string = date.slice(0,4)
    const month: string = date.slice(4,6)
    const day: string = date.slice(6,8)

    return `${day}/${month}/${year}`;
}