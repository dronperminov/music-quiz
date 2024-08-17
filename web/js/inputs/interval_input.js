function IntervalInput(blockId, value = null) {
    this.block = document.getElementById(blockId)
    this.error = document.getElementById(`${blockId}-error`)
    this.scale2number = {"": 1, "K": 1000, "M": 1000000}

    let inputs = this.block.getElementsByTagName("input")
    this.minInput = inputs[0]
    this.maxInput = inputs[1]

    this.minInput.addEventListener("input", () => this.ClearErrorInput(this.minInput))
    this.maxInput.addEventListener("input", () => this.ClearErrorInput(this.maxInput))

    this.SetValue(value)
}

IntervalInput.prototype.ClearErrorInput = function(input) {
    input.classList.remove("input-error")
    this.error.innerText = ""
}

IntervalInput.prototype.GetInputValue = function(input, message) {
    let value = input.value

    if (value === "")
        return ""

    if (value.match(/^\d+(\.\d*)?$/) !== null)
        return +value

    let match = (/^(?<number>\d+(\.\d*)?)(?<scale>[kKкКmMмМ])$/).exec(value)
    if (match !== null) {
        let number = +match.groups.number
        let scale = match.groups.scale.replace(/[кk]/gi, "K").replace(/[мm]/gi, "M")

        if (number < 1) {
            number *= 1000
            scale = scale == "K" ? "" : "K"
        }

        input.value = `${number}${scale}`
        return number * this.scale2number[scale]
    }

    input.focus()
    input.classList.add("input-error")

    throw new Error(message)
}

IntervalInput.prototype.PrettifyInputValue = function(value) {
    if (value.match(/^\d+[kKкКmMмМ]$/g))
        return value

    if (value.match(/^\d+000000$/g))
        return `${value.substr(0, value.length - 6)}M`

    if (value.match(/^\d+000$/g))
        return `${value.substr(0, value.length - 3)}K`

    return value
}

IntervalInput.prototype.SwapValues = function(min, max) {
    if (min === "" || max === "" || min <= max)
        return [min, max]

    let value = this.minInput.value
    this.minInput.value = this.maxInput.value
    this.maxInput.value = value
    return [max, min]
}

IntervalInput.prototype.GetValue = function() {
    this.ClearErrorInput(this.minInput)
    this.ClearErrorInput(this.maxInput)

    try {
        let min = this.GetInputValue(this.minInput, "Начальное значение задано некорректно")
        let max = this.GetInputValue(this.maxInput, "Конечное значение задано некорректно")

        return this.SwapValues(min, max)
    }
    catch (error) {
        this.error.innerText = error.message
        return null
    }
}

IntervalInput.prototype.SetValue = function(value) {
    if (value === null)
        return

    this.minInput.value = this.PrettifyInputValue(value[0].toString())
    this.maxInput.value = this.PrettifyInputValue(value[1].toString())
}

IntervalInput.prototype.Clear = function() {
    this.minInput.value = ""
    this.maxInput.value = ""
}
