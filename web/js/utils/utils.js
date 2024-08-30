function SetAttributes(element, attributes) {
    if (attributes === null)
        return

    for (let [name, value] of Object.entries(attributes)) {
        if (name == "innerText")
            element.innerText = value
        else if (name == "innerHTML")
            element.innerHTML = value
        else
            element.setAttribute(name, value)
    }
}

function MakeElement(className, parent = null, attributes = null, tagName = "div") {
    let element = document.createElement(tagName)
    element.className = className

    SetAttributes(element, attributes)

    if (parent !== null)
        parent.appendChild(element)

    return element
}

function MakeCheckbox(parent, id, checked = false) {
    let label = MakeElement("switch-checkbox", parent, {for: id}, "label")
    let input = MakeElement("", label, {type: "checkbox", id: id}, "input")
    let span = MakeElement("switch-checkbox-slider", label, {}, "span")

    if (checked)
        input.setAttribute("checked", "")

    return input
}

function MakeDetails(parent, header, className = "details") {
    let details = MakeElement(className, parent)
    let detailsHeader = MakeElement("details-header", details)
    let detailsIcon = MakeElement("details-icon", detailsHeader, {}, "span")
    let detailsHeaderText = MakeElement("", detailsHeader, {innerText: header}, "span")

    detailsHeader.addEventListener("click", () => details.classList.toggle("details-open"))

    return MakeElement("details-content", details)
}

function GetWordForm(count, forms, onlyForm = false) {
    let index = 0

    if ([0, 5, 6, 7, 8, 9].indexOf(Math.abs(count) % 10) > -1 || [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20].indexOf(Math.abs(count) % 100) > -1)
        index = 2
    else if ([2, 3, 4].indexOf(Math.abs(count) % 10) > -1) 
        index = 1

    return onlyForm ? forms[index] : `${count} ${forms[index]}`
}

function Round(value, scale = 100) {
    return Math.round(value * scale) / scale
}

function FormatTime(time) {
    if (time < 10)
        return `${Round(time, 10)} ${GetWordForm(Math.floor(time * 10) % 10, ['секунда', 'секунды', 'секунд'], true)}`

    if (time < 60)
        return GetWordForm(Math.round(time), ['секунда', 'секунды', 'секунд'])

    let seconds = `${Math.floor(time) % 60}`.padStart(2, '0')
    let minutes = `${Math.floor(time / 60)}`.padStart(2, '0')
    return `${minutes}:${seconds}`
}

function ParseDateTime(datetime) {
    let match = (/^(?<year>\d\d\d\d)-(?<month>\d\d?)-(?<day>\d\d?)T(?<time>\d\d?:\d\d:\d\d?)(\.\d+)?$/g).exec(datetime)
    let groups = match.groups

    return {date: `${groups.day}.${groups.month}.${groups.year}`, time: groups.time}
}

function ClearSearchParams(url) {
    let keys = []

    for (let [key, value] of url.searchParams.entries())
        keys.push(key)

    for (let key of keys)
        url.searchParams.delete(key)
}
