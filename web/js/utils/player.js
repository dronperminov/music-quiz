const PLAYER_LYRICS_ICON = `<svg width="1em" height="1em" viewBox="2 2 52 52" xmlns="http://www.w3.org/2000/svg">
    <path d="M 29.7460 51.8359 C 33.2147 51.8359 38.4647 49.2344 38.4647 42.3437 L 38.4647 20.8984 C 38.4647 19.7265 38.6522 19.5156 39.7069 19.3047 L 50.8868 16.8437 C 51.7072 16.6563 52.2462 16 52.2462 15.1797 L 52.2462 6.3437 C 52.2462 5.0312 51.1912 4.1641 49.9024 4.4453 L 37.4803 7.1406 C 35.8632 7.4922 34.9960 8.3359 34.9960 9.7422 L 35.1366 35.8047 C 35.1366 36.8828 34.6444 37.5859 33.6835 37.7734 L 29.9569 38.5703 C 25.1757 39.5547 22.9491 42.0156 22.9491 45.6015 C 22.9491 49.2578 25.7850 51.8359 29.7460 51.8359 Z M 5.3476 16.3750 L 26.3007 16.3750 C 27.1913 16.3750 27.8944 15.6484 27.8944 14.7812 C 27.8944 13.9141 27.1913 13.2109 26.3007 13.2109 L 5.3476 13.2109 C 4.4803 13.2109 3.7538 13.9141 3.7538 14.7812 C 3.7538 15.6484 4.4803 16.3750 5.3476 16.3750 Z M 5.3476 24.7187 L 26.3007 24.7187 C 27.2147 24.7187 27.8944 23.9922 27.8944 23.1016 C 27.8944 22.2344 27.1913 21.5547 26.3007 21.5547 L 5.3476 21.5547 C 4.4803 21.5547 3.7538 22.2344 3.7538 23.1016 C 3.7538 23.9922 4.4569 24.7187 5.3476 24.7187 Z M 5.3476 33.0625 L 26.3007 33.0625 C 27.2147 33.0625 27.8944 32.3594 27.8944 31.4687 C 27.8944 30.6016 27.1913 29.8984 26.3007 29.8984 L 5.3476 29.8984 C 4.4803 29.8984 3.7538 30.6016 3.7538 31.4687 C 3.7538 32.3594 4.4569 33.0625 5.3476 33.0625 Z"/>
</svg>`

function Player(trackId, audio, config) {
    this.audio = audio

    this.Build(trackId, config)
    this.InitEvents()
    this.InitMediaSessionHandlers()
    this.InitAudioParams()

    setInterval(() => this.UpdateLoop(), 10)
}

Player.prototype.Build = function(trackId, config) {
    this.block = document.getElementById(`player-${trackId}`)

    this.loadIcon = document.getElementById(`player-${trackId}-load`)
    this.playIcon = document.getElementById(`player-${trackId}-play`)
    this.pauseIcon = document.getElementById(`player-${trackId}-pause`)

    this.icons = this.BuildElement(`player-icons${config.withIcons ? "" : " hidden"}`, this.block)
    this.lyricsIcon = this.BuildElement("player-icon hidden", this.icons, PLAYER_LYRICS_ICON)

    this.progress = this.BuildElement("player-progress", this.block)
    this.progressBar = this.BuildElement("player-progress-bar", this.progress)
    this.progressCurrent = this.BuildElement("player-progress-current", this.progressBar)
    this.time = this.BuildElement("player-time", this.block)

    this.lyricsUpdater = null

    if (document.getElementById(`lyrics-updater-${trackId}`) !== null) {
        this.lyricsUpdater = new LyricsUpdater(`lyrics-updater-${trackId}`, (seek) => this.Seek(seek))
        this.lyricsIcon.classList.remove("hidden")

        if (this.lyricsUpdater.IsOpen())
            this.lyricsIcon.classList.add("player-icon-pressed")
        else
            this.lyricsIcon.classList.remove("player-icon-pressed")
    }
}

Player.prototype.InitEvents = function() {
    this.audio.addEventListener("pause", () => this.PauseEvent())
    this.audio.addEventListener("play", () => this.PlayEvent())
    this.audio.addEventListener("seeking", () => this.UpdateProgressBar())

    this.playIcon.addEventListener("click", () => this.Play())
    this.pauseIcon.addEventListener("click", () => this.Pause())
    this.lyricsIcon.addEventListener("click", () => this.ToggleLyrics())

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

Player.prototype.BuildElement = function(className, parent, innerHTML = "") {
    let element = document.createElement("div")
    element.className = className

    if (innerHTML !== "")
        element.innerHTML = innerHTML

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

Player.prototype.ToggleLyrics = function() {
    if (this.lyricsUpdater === null)
        return

    this.lyricsIcon.classList.toggle("player-icon-pressed")

    if (this.lyricsIcon.classList.contains("player-icon-pressed"))
        this.lyricsUpdater.Open()
    else
        this.lyricsUpdater.Close()
}

Player.prototype.ShowIcons = function() {
    this.icons.classList.remove("hidden")
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
