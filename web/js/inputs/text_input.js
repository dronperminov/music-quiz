function TextInput(inputId, pattern, errorMessage, value = null, onChange = null) {
    this.input = document.getElementById(inputId)
    this.error = document.getElementById(`${inputId}-error`)
    this.input.addEventListener("input", () => this.Input())

    if (onChange !== null)
        this.input.addEventListener("change", () => onChange())

    this.pattern = pattern
    this.errorMessage = errorMessage

    this.SetValue(value)
}

TextInput.prototype.SetValue = function(value) {
    if (value !== null)
        this.input.value = value
}

TextInput.prototype.GetValue = function() {
    let value = this.input.value.trim()
    this.input.value = value

    if (value.match(this.pattern) === null) {
        this.input.classList.add("error-input")
        this.input.focus()
        this.error.innerText = this.errorMessage
        this.input.scrollIntoView({behavior: 'smooth'})
        return null
    }

    return value
}

TextInput.prototype.Input = function() {
    this.input.classList.remove("error-input")
    this.error.innerText = ""
}
