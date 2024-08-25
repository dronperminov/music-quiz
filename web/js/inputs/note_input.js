function NoteInput(textarea, maxHeight = 300) {
    this.textarea = textarea
    this.maxHeight = maxHeight

    this.textarea.addEventListener("input", () => this.Resize())
    this.textarea.addEventListener("change", () => this.Resize())
    window.addEventListener("resize", () => this.Resize())

    this.Resize()
}

NoteInput.prototype.Resize = function() {
    this.textarea.style.height = "0px"
    this.textarea.style.height = `${Math.min(this.maxHeight, this.textarea.scrollHeight + 2)}px`
}
