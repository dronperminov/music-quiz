function Language(value) {
    this.value = value
    this.options = {
        "unknown": "неизвестен",
        "russian": "русский",
        "foreign": "зарубежный"
    }
}

Language.prototype.ToRus = function() {
    return this.options[this.value]
}

Language.prototype.IsUnknown = function() {
    return this.value == "unknown"
}

Language.prototype.Build = function(parent) {
    let label = MakeElement("", parent, {innerHTML: `<b>Язык:</b> `}, "span")
    let select = MakeElement("text-select", parent, {}, "select")

    for (let [value, name] of Object.entries(this.options)) {
        if (!this.IsUnknown() && value == "unknown")
            continue

        let option = MakeElement("", select, {innerText: name, value: value}, "option")

        if (this.value == value)
            option.setAttribute("selected", "")
    }

    let html = document.getElementsByTagName("html")[0]
    if (!html.hasAttribute("data-user-role") || html.getAttribute("data-user-role") != "admin") {
        select.classList.add("text-select-disabled")
        return
    }

    select.addEventListener("click", () => {
        select.classList.remove("text-select")
        select.classList.add("basic-select")
    })

    label.addEventListener("click", () => {
        select.value = this.value
        select.classList.remove("basic-select")
        select.classList.add("text-select")
    })

    return select
}
