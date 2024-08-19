function Player(trackId, audio) {
    this.audio = audio

    this.Build(trackId)
    this.InitEvents()
    this.InitMediaSessionHandlers()
    this.InitAudioParams()

    setInterval(() => this.UpdateLoop(), 10)
}

Player.prototype.Build = function(trackId) {
    this.block = document.getElementById(`player-${trackId}`)

    this.loadIcon = document.getElementById(`player-${trackId}-load`)
    this.playIcon = document.getElementById(`player-${trackId}-play`)
    this.pauseIcon = document.getElementById(`player-${trackId}-pause`)
    this.lyricsIcon = document.getElementById(`player-${trackId}-lyrics`)

    this.progress = this.BuildElement("player-progress", this.block)
    this.progressBar = this.BuildElement("player-progress-bar", this.progress)
    this.progressCurrent = this.BuildElement("player-progress-current", this.progressBar)
    this.time = this.BuildElement("player-time", this.block)

    this.lyricsUpdater = null

    if (document.getElementById(`lyrics-updater-${trackId}`) !== null) {
        this.lyricsUpdater = new LyricsUpdater(`lyrics-updater-${trackId}`, (seek) => this.Seek(seek))
    }
}

Player.prototype.InitEvents = function() {
    this.audio.addEventListener("pause", () => this.PauseEvent())
    this.audio.addEventListener("play", () => this.PlayEvent())
    this.audio.addEventListener("seeking", () => this.UpdateProgressBar())

    this.playIcon.addEventListener("click", () => this.Play())
    this.pauseIcon.addEventListener("click", () => this.Pause())

    this.progress.addEventListener("touchstart", (e) => this.ProgressMouseDown(this.PointToSeek(e)))
    this.progress.addEventListener("touchmove", (e) => this.ProgressMouseMove(this.PointToSeek(e)))
    this.progress.addEventListener("touchend", (e) => this.ProgressMouseUp())
    this.progress.addEventListener("touchleave", (e) => this.ProgressMouseUp())

    this.progress.addEventListener("mousedown", (e) => this.ProgressMouseDown(this.PointToSeek(e)))
    this.progress.addEventListener("mousemove", (e) => this.ProgressMouseMove(this.PointToSeek(e)))
    this.progress.addEventListener("mouseup", (e) => this.ProgressMouseUp())
    this.progress.addEventListener("mouseleave", (e) => this.ProgressMouseUp())
}

Player.prototype.InitMediaSessionHandlers = function() {
    if (!("mediaSession" in navigator))
        return

    navigator.mediaSession.setActionHandler("seekto", details => this.Seek(this.startTime + details.seekTime))
}

Player.prototype.InitAudioParams = function() {
    let seek = this.audio.hasAttribute("data-seek") ? +this.audio.getAttribute("data-seek") : 0
    let timecode = this.audio.hasAttribute("data-timecode") ? this.audio.getAttribute("data-timecode") : ""

    this.SetTimecode(timecode)
    this.Seek(seek)
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
    return this.audio.play()
}

Player.prototype.Pause = function() {
    return this.audio.pause()
}

Player.prototype.Seek = function(seek) {
    this.audio.currentTime = Math.max(this.startTime, Math.min(this.endTime - this.startTime, seek))
}

Player.prototype.SetTimecode = function(timecode = "") {
    [this.startTime, this.endTime] = this.ParseTimecode(timecode)
    this.UpdateProgressBar()
}

Player.prototype.ParseTimecode = function(timecode) {
    if (timecode === "")
        return [0, this.audio.duration]

    let timestamps = timecode.split(",")

    if (timestamps.length == 1)
        return [+timecode, this.audio.duration]

    return [+timestamps[0], +timestamps[1]]
}

Player.prototype.PointToSeek = function(e) {
    let x = e.touches ? e.touches[0].clientX - this.progress.offsetLeft : e.offsetX
    let part = Math.max(0, Math.min(1, x / this.progressBar.clientWidth))
    return this.startTime + part * (this.endTime - this.startTime)
}

Player.prototype.UpdateProgressBar = function() {
    if (this.audio.currentTime >= this.endTime || this.audio.ended)
        this.audio.currentTime = this.startTime

    let currentTime = Math.max(this.audio.currentTime - this.startTime, 0)
    let duration = Math.max(this.endTime - this.startTime, 0.01)

    if (this.lyricsUpdater !== null)
        this.lyricsUpdater.Update(this.audio.currentTime)

    this.progressCurrent.style.width = `${currentTime / duration * 100}%`
    this.time.innerText = `${this.TimeToString(currentTime)} / ${this.TimeToString(duration)}`

    if ("mediaSession" in navigator)
        navigator.mediaSession.setPositionState({duration: duration, playbackRate: this.audio.playbackRate, position: currentTime})
}

Player.prototype.ProgressMouseDown = function(seek) {
    this.paused = this.audio.paused
    this.pressed = true

    this.Seek(seek)
    this.audio.pause()
}

Player.prototype.ProgressMouseMove = function(seek) {
    if (this.pressed)
        this.Seek(seek)
}

Player.prototype.ProgressMouseUp = function() {
    if (!this.pressed)
        return

    this.pressed = false

    if (!this.paused)
        this.audio.play()
}

Player.prototype.PlayEvent = function() {
    this.playIcon.classList.add("hidden")
    this.pauseIcon.classList.remove("hidden")
    this.loadIcon.classList.add("hidden")

    if ("mediaSession" in navigator)
        navigator.mediaSession.playbackState = "playing"
}

Player.prototype.PauseEvent = function() {
    this.playIcon.classList.remove("hidden")
    this.pauseIcon.classList.add("hidden")
    this.loadIcon.classList.add("hidden")

    if ("mediaSession" in navigator)
        navigator.mediaSession.playbackState = "paused"
}
