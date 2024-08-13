function Player(playerId, audio) {
    this.block = document.getElementById(playerId)
    this.audio = audio

    this.Build(playerId)
    this.InitEvents()

    setInterval(() => this.UpdateLoop(), 10)
}

Player.prototype.Build = function(playerId) {
    this.loadIcon = document.getElementById(`${playerId}-load`)
    this.playIcon = document.getElementById(`${playerId}-play`)
    this.pauseIcon = document.getElementById(`${playerId}-pause`)

    this.loadIcon.classList.add("hidden")
    this.pauseIcon.classList.remove("hidden")

    this.progress = this.BuildElement("player-progress", this.block)
    this.progressBar = this.BuildElement("player-progress-bar", this.progress)
    this.progressCurrent = this.BuildElement("player-progress-current", this.progressBar)
    this.time = this.BuildElement("player-time", this.block)
}

Player.prototype.InitEvents = function() {
    this.audio.addEventListener("pause", () => {
        this.playIcon.classList.remove("hidden")
        this.pauseIcon.classList.add("hidden")
    })

    this.audio.addEventListener("play", () => {
        this.playIcon.classList.add("hidden")
        this.pauseIcon.classList.remove("hidden")
    })

    this.playIcon.addEventListener("click", () => this.Play())
    this.pauseIcon.addEventListener("click", () => this.Pause())

    this.progress.addEventListener("touchstart", (e) => this.ProgressMouseDown(this.GetPoint(e)))
    this.progress.addEventListener("touchmove", (e) => this.ProgressMouseMove(this.GetPoint(e)))
    this.progress.addEventListener("touchend", (e) => this.ProgressMouseUp())
    this.progress.addEventListener("touchleave", (e) => this.ProgressMouseUp())

    this.progress.addEventListener("mousedown", (e) => this.ProgressMouseDown(this.GetPoint(e)))
    this.progress.addEventListener("mousemove", (e) => this.ProgressMouseMove(this.GetPoint(e)))
    this.progress.addEventListener("mouseup", (e) => this.ProgressMouseUp())
    this.progress.addEventListener("mouseleave", (e) => this.ProgressMouseUp())
}

Player.prototype.BuildElement = function(className, parent) {
    let element = document.createElement("div")
    element.className = className
    parent.appendChild(element)
    return element
}

Player.prototype.UpdateLoop = function() {
    if (!this.audio.paused)
        this.UpdateProgressBar()
}

Player.prototype.TimeToString = function(time) {
    let seconds = `${Math.floor(time) % 60}`.padStart(2, '0')
    let minutes = `${Math.floor(time / 60)}`.padStart(2, '0')
    return `${minutes}:${seconds}`
}

Player.prototype.Play = function() {
    this.audio.play()
}

Player.prototype.Pause = function() {
    this.audio.pause()
}

Player.prototype.GetPoint = function(e) {
    if (e.touches)
        return e.touches[0].clientX - this.progress.offsetLeft

    return e.offsetX
}

Player.prototype.UpdateProgressBar = function() {
    let currentTime = Math.max(this.audio.currentTime, 0)
    let duration = Math.max(this.audio.duration, 0.01)

    this.progressCurrent.style.width = `${currentTime / duration * 100}%`
    this.time.innerText = `${this.TimeToString(currentTime)} / ${this.TimeToString(duration)}`
}

Player.prototype.ProgressMouseDown = function(x) {
    this.paused = this.audio.paused
    this.pressed = true

    let part = Math.max(0, Math.min(1, x / this.progressBar.clientWidth))
    this.audio.currentTime = part * this.audio.duration
    this.audio.pause()

    this.UpdateProgressBar()
}

Player.prototype.ProgressMouseMove = function(x) {
    if (!this.pressed)
        return

    let part = Math.max(0, Math.min(1, x / this.progressBar.clientWidth))
    this.audio.currentTime = part * this.audio.duration
    this.UpdateProgressBar()
}

Player.prototype.ProgressMouseUp = function() {
    if (!this.pressed)
        return

    this.pressed = false

    if (!this.paused)
        this.audio.play()
}
