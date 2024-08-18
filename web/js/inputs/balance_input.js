function BalanceInput(blockId, errorMessage, value, onChange = null) {
    this.block = document.getElementById(blockId)
    this.error = document.getElementById(`${blockId}-error`)
    this.errorMessage = errorMessage

    this.options = {}
    for (let track of this.block.getElementsByClassName("balance-input-option-track")) {
        let input = track.getElementsByTagName("input")[0]
        let name = input.getAttribute("data-name")
        let value = document.getElementById(`${input.getAttribute("id")}-value`)
        this.options[name] = {input: input, value: value}

        input.addEventListener("input", () => this.UpdateValue(input, value))

        if (onChange !== null)
            input.addEventListener("change", () => onChange())
    }

    this.SetValue(value)
}

BalanceInput.prototype.SetValue = function(value) {
    for (let option of Object.values(this.options)) {
        option.input.value = 50
        option.value.innerText = "50"
    }

    if (value === null)
        return

    let maxValue = 0
    let minValue = Infinity

    for (let optionValue of Object.values(value)) {
        maxValue = Math.max(maxValue, optionValue)
        minValue = Math.min(minValue, optionValue)
    }

    if (maxValue == 0)
        maxValue = 1
    else if (minValue == maxValue)
        maxValue *= 2

    for (let [name, option] of Object.entries(this.options)) {
        let optionValue = name in value ? Math.round(value[name] / maxValue * 1000) / 10 : 0
        option.input.value = optionValue
        option.value.innerText = `${optionValue}`
    }
}

BalanceInput.prototype.GetValue = function() {
    let value = {}
    let sum = 0

    for (let [name, option] of Object.entries(this.options)) {
        let optionValue = +option.input.value
        value[name] = optionValue
        sum += optionValue
    }

    if (sum == 0) {
        this.error.innerText = this.errorMessage
        this.block.scrollIntoView({behavior: 'smooth'})
        return null
    }

    for (let [name, nameValue] of Object.entries(value))
        value[name] = nameValue / sum

    return value
}

BalanceInput.prototype.Clear = function() {
    this.SetValue(null)
}

BalanceInput.prototype.UpdateValue = function(input, value) {
    value.innerText = input.value
    this.error.innerText = ""
}
