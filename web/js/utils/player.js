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

const PLAYER_NOTE_ICON = `<svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M21.6189 12.099L20.9989 11.889L19.3289 11.339C18.7489 11.149 18.1589 11.219 17.7089 11.539C17.2689 11.869 17.0089 12.399 17.0089 13.019V17.809C16.6089 17.589 16.1589 17.449 15.6689 17.449C14.1289 17.449 12.8789 18.709 12.8789 20.249C12.8789 20.509 12.9189 20.759 12.9789 20.999C13.3089 22.189 14.3889 23.049 15.6689 23.049C17.1989 23.049 18.4389 21.829 18.4689 20.309V15.699C18.4889 15.699 18.4989 15.709 18.5189 15.719L20.7989 16.479C20.8389 16.489 20.8889 16.509 20.9289 16.509C21.1089 16.559 21.2689 16.579 21.4389 16.579C21.7989 16.579 22.1389 16.479 22.4189 16.269C22.8689 15.949 23.1189 15.419 23.1189 14.799V14.199C23.1189 13.289 22.4789 12.389 21.6189 12.099ZM15.6689 21.589C15.2089 21.589 14.8089 21.359 14.5689 20.999C14.4189 20.789 14.3389 20.529 14.3389 20.249C14.3389 19.519 14.9389 18.919 15.6689 18.919C16.4089 18.919 17.0089 19.519 17.0089 20.249C17.0089 20.479 16.9489 20.689 16.8489 20.869C16.6289 21.299 16.1789 21.589 15.6689 21.589Z"/>
    <path d="M23.1189 14.199V14.799C23.1189 15.419 22.8689 15.949 22.4189 16.269C22.1389 16.479 21.7989 16.579 21.4389 16.579C21.2689 16.579 21.1089 16.559 20.9289 16.509C20.8889 16.509 20.8389 16.489 20.7989 16.479L18.5189 15.719C18.4989 15.709 18.4889 15.699 18.4689 15.699V20.309C18.4389 21.829 17.1989 23.049 15.6689 23.049C14.3889 23.049 13.3089 22.189 12.9789 20.999C12.9189 20.759 12.8789 20.509 12.8789 20.249C12.8789 18.709 14.1289 17.449 15.6689 17.449C16.1589 17.449 16.6089 17.589 17.0089 17.809V13.019C17.0089 12.399 17.2689 11.869 17.7089 11.539C18.1589 11.219 18.7489 11.149 19.3289 11.339L20.9989 11.889L21.6189 12.099C22.4789 12.389 23.1189 13.289 23.1189 14.199Z"/>
    <path d="M21 7.52V9.62C21 9.96 20.67 10.2 20.34 10.09L19.8 9.91C18.75 9.58 17.68 9.72 16.81 10.34C15.98 10.96 15.51 11.94 15.51 13.02V15.47C15.51 15.74 15.3 15.96 15.03 16C12.97 16.31 11.38 18.1 11.38 20.25C11.38 20.3 11.38 20.35 11.38 20.4C11.39 20.71 11.16 21 10.84 21H7.52C4.07 21 2 18.94 2 15.48V7.52C2 4.06 4.07 2 7.52 2H15.48C18.93 2 21 4.06 21 7.52Z"/>
</svg>`

const TRACK_LOAD_ICON = `
<svg width="1.25em" height="1.25em" viewBox="0 0 7.1 7.1" xmlns="http://www.w3.org/2000/svg">
    <path d="M5.495,2.573 L1.501,0.142 C0.832,-0.265 0,0.25 0,1.069 L0,5.931 C0,6.751 0.832,7.264 1.501,6.858 L5.495,4.428 C6.168,4.018 6.168,2.983 5.495,2.573" />
</svg>
`

const TRACK_PLAY_ICON = `<svg width="1.25em" height="1.25em" viewBox="0 0 7.1 7.1" xmlns="http://www.w3.org/2000/svg">
    <path d="M5.495,2.573 L1.501,0.142 C0.832,-0.265 0,0.25 0,1.069 L0,5.931 C0,6.751 0.832,7.264 1.501,6.858 L5.495,4.428 C6.168,4.018 6.168,2.983 5.495,2.573" />
</svg>
`

const TRACK_PAUSE_ICON = `<svg width="1.25em" height="1.25em" viewBox="-0.7 -0.05 8.1 8.1" xmlns="http://www.w3.org/2000/svg">
    <path d="M1,0 C0.448,0 0,0.448 0,1 L0,7 C0,7.552 0.448,8 1,8 C1.552,8 2,7.552 2,7 L2,1 C2,0.448 1.552,0 1,0 M6,1 L6,7 C6,7.552 5.552,8 5,8 C4.448,8 4,7.552 4,7 L4,1 C4,0.448 4.448,0 5,0 C5.552,0 6,0.448 6,1" />
</svg>
`

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
    this.noteIcon = this.BuildElement(`player-icon${this.audio.hasAttribute("data-note-seek") ? "" : " hidden"}`, this.icons, PLAYER_NOTE_ICON)

    this.progress = this.BuildElement("player-progress", this.block)
    this.progressBar = this.BuildElement("player-progress-bar", this.progress)
    this.progressCurrent = this.BuildElement("player-progress-current", this.progressBar)
    this.time = this.BuildElement("player-time", this.block)

    this.lyricsUpdater = null

    if (document.getElementById(`lyrics-updater-${trackId}`) !== null) {
        this.lyricsUpdater = new LyricsUpdater(`lyrics-updater-${trackId}`, (seek) => this.Seek(seek))
        this.lyricsIcon.classList.remove("hidden")

        if (this.lyricsUpdater.lrc && this.lyricsUpdater.HaveChorus())
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
    this.noteIcon.addEventListener("click", () => this.SeekToNote())

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
    if (this.audio.hasAttribute("data-note-seek"))
        this.noteIcon.classList.remove("hidden")
    else
        this.noteIcon.classList.add("hidden")

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
    if (this.lyricsUpdater === null || !this.lyricsUpdater.lrc)
        return

    let time = this.lyricsUpdater.GetChorusTime(this.audio.currentTime)
    this.Seek(time)
}

Player.prototype.SeekToNote = function() {
    let time = +this.audio.getAttribute("data-note-seek")
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

Player.prototype.Reset = function() {
    this.SetTimecode("")
    this.SetPlaybackRate(1)
    this.ShowIcons()
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
