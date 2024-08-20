const PLAYER_LYRICS_ICON = `<svg width="1em" height="1em" viewBox="2 2 52 52" xmlns="http://www.w3.org/2000/svg">
    <path d="M 29.7460 51.8359 C 33.2147 51.8359 38.4647 49.2344 38.4647 42.3437 L 38.4647 20.8984 C 38.4647 19.7265 38.6522 19.5156 39.7069 19.3047 L 50.8868 16.8437 C 51.7072 16.6563 52.2462 16 52.2462 15.1797 L 52.2462 6.3437 C 52.2462 5.0312 51.1912 4.1641 49.9024 4.4453 L 37.4803 7.1406 C 35.8632 7.4922 34.9960 8.3359 34.9960 9.7422 L 35.1366 35.8047 C 35.1366 36.8828 34.6444 37.5859 33.6835 37.7734 L 29.9569 38.5703 C 25.1757 39.5547 22.9491 42.0156 22.9491 45.6015 C 22.9491 49.2578 25.7850 51.8359 29.7460 51.8359 Z M 5.3476 16.3750 L 26.3007 16.3750 C 27.1913 16.3750 27.8944 15.6484 27.8944 14.7812 C 27.8944 13.9141 27.1913 13.2109 26.3007 13.2109 L 5.3476 13.2109 C 4.4803 13.2109 3.7538 13.9141 3.7538 14.7812 C 3.7538 15.6484 4.4803 16.3750 5.3476 16.3750 Z M 5.3476 24.7187 L 26.3007 24.7187 C 27.2147 24.7187 27.8944 23.9922 27.8944 23.1016 C 27.8944 22.2344 27.1913 21.5547 26.3007 21.5547 L 5.3476 21.5547 C 4.4803 21.5547 3.7538 22.2344 3.7538 23.1016 C 3.7538 23.9922 4.4569 24.7187 5.3476 24.7187 Z M 5.3476 33.0625 L 26.3007 33.0625 C 27.2147 33.0625 27.8944 32.3594 27.8944 31.4687 C 27.8944 30.6016 27.1913 29.8984 26.3007 29.8984 L 5.3476 29.8984 C 4.4803 29.8984 3.7538 30.6016 3.7538 31.4687 C 3.7538 32.3594 4.4569 33.0625 5.3476 33.0625 Z"/>
</svg>`

const PLAYER_CHORUS_ICON = `<svg width="1.2em" height="1.2em" viewBox="0 0 960 960" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M592.448 676.492C634.941 548.274 689.177 423.607 727.239 294.235C728.897 287.334 727.228 283.457 719.294 281.709C622.855 263.12 528.089 232.324 430.221 223.091C412.095 330.54 388.216 436.331 364.157 542.468C342.362 615.971 322.161 723.719 232.862 739.576C190.558 745.804 155.44 716.767 152.031 674.155C152.533 607.712 208.223 541.795 268.736 557.322C280.026 560.837 290.903 565.663 303.375 570.441C336.499 451.986 358.667 329.019 380.87 207.933C389.514 157.034 449.275 172.417 485.656 177.892C570.069 196.051 654.789 213.267 738.464 234.573C793.265 244.735 779.161 306.258 766.581 344.77C746.661 402.504 724.432 459.439 703.634 516.878C673.232 600.523 646.883 685.763 608.832 766.403C604.543 775.907 597.859 784.555 591.205 792.726C542.974 856.995 435.247 818.887 436.935 738.333C437.239 664.774 537.81 635.657 592.448 676.492Z"/>
    <path d="M244.133 336.717C183.459 315.681 130.397 277.565 73.4054 248.431C55.0164 240.143 32.9644 221.844 45.3274 201.97C66.4504 167.334 119.569 221.201 145.805 231.568C179.352 250.51 213.21 268.898 246.923 287.545C275.45 298.178 278.166 331.889 244.133 336.717Z"/>
    <path d="M893.98 789.714C884.23 790.14 876.882 784.225 869.75 777.696C835.749 747.334 803.345 715.063 767.845 686.469C742.571 667.029 768.21 630.183 794.86 647.096C806.708 654.656 817.962 663.347 828.625 672.53C854.747 695.027 880.397 718.071 906.192 740.946C913.271 747.224 918.797 754.394 919.122 764.482C919.605 779.528 909.744 789.783 893.98 789.714Z"/>
    <path d="M156.159 437.789C166.397 438.604 173.732 443.039 177.686 452.15C195.01 489.63 100.57 506.205 76.3195 518.167C39.9925 530.781 25.4185 480.842 59.1055 469.926C91.4955 459.405 123.357 446.976 156.159 437.789Z"/>
    <path d="M663.886 862.332C661.623 846.805 659.199 831.299 657.138 815.746C651.167 782.464 697.609 771.173 705.725 803.149C710.787 826.396 715.423 849.801 718.683 873.356C721.483 917.168 660.632 918.73 662.42 862.532C662.909 862.465 663.398 862.398 663.886 862.332Z"/>
    <path d="M284.652 53.2666C293.13 53.4646 301.274 58.8846 305.761 68.2136C316.457 90.4536 326.824 112.883 336.371 135.635C341.913 148.841 337.21 161.024 326.409 166.555C315.934 171.919 302.829 169.144 296.017 157.219C282.987 134.409 270.509 111.138 259.934 87.1196C252.511 70.2576 265.059 53.1136 284.652 53.2666Z"/>
    <path d="M878.829 441.892C918.731 439.594 923.612 487.993 887.996 494.212C873.8 496.284 859.501 497.891 845.19 498.899C811.628 502.359 804.822 454.609 837.832 448.599C852.903 445.409 868.264 443.576 878.829 441.892Z"/>
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
    this.chorusIcon = this.BuildElement("player-icon hidden", this.icons, PLAYER_CHORUS_ICON)

    this.progress = this.BuildElement("player-progress", this.block)
    this.progressBar = this.BuildElement("player-progress-bar", this.progress)
    this.progressCurrent = this.BuildElement("player-progress-current", this.progressBar)
    this.time = this.BuildElement("player-time", this.block)

    this.lyricsUpdater = null

    if (document.getElementById(`lyrics-updater-${trackId}`) !== null) {
        this.lyricsUpdater = new LyricsUpdater(`lyrics-updater-${trackId}`, (seek) => this.Seek(seek))
        this.lyricsIcon.classList.remove("hidden")

        if (this.lyricsUpdater.HaveChorus())
            this.chorusIcon.classList.remove("hidden")

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
    this.chorusIcon.addEventListener("click", () => this.SeekToChorus())

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
    let playbackRate = this.audio.hasAttribute("data-playback-rate") ? +this.audio.getAttribute("data-playback-rate") : 1

    this.SetTimecode(timecode)
    this.SetPlaybackRate(playbackRate)
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

Player.prototype.SetPlaybackRate = function(playbackRate) {
    this.audio.playbackRate = Math.max(0.25, Math.min(4, playbackRate))
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

Player.prototype.SeekToChorus = function() {
    if (this.lyricsUpdater === null)
        return

    let time = this.lyricsUpdater.GetChorusTime(this.audio.currentTime)
    this.Seek(time)
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
