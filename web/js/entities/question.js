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

function Question(question, onAnswer) {
    this.question = question
    this.trackId = question.track_id
    this.onAnswer = onAnswer
}

Question.prototype.Build = function(parent, params) {
    this.track = new Track(params.track)
    this.artists = params.track.artists.map(artistId => params.artist_id2artist[artistId])
    this.answerTime = null

    MakeElement("question-title", parent, {innerHTML: this.question.title})
    this.BuildAudio(parent, params)
    this.BuildTrack(parent, params)
    this.BuildTrackModifications(parent)
    this.BuildShowAnswerButton(parent)
    this.BuildAnswerBlock(parent, params)

    parent.classList.remove("hidden")
}

Question.prototype.BuildAudio = function(parent, params) {
    let audio = MakeElement("", parent, {}, "audio")

    audio.setAttribute("id", `audio-${this.trackId}`)
    audio.setAttribute("data-track-id", this.trackId)
    audio.setAttribute("preload", "metadata")

    if (params.track.downloaded)
        audio.setAttribute("data-src", `https://music.dronperminov.ru/tracks/${this.trackId}.mp3`)
    else
        audio.setAttribute("data-yandex-id", params.track.source.yandex_id)

    audio.setAttribute("data-seek", this.question.question_seek)
    audio.setAttribute("data-playback-rate", this.question.track_modifications.playback_rate)

    if (this.question.question_timecode)
        audio.setAttribute("data-timecode", this.question.question_timecode)

    if (params.note && this.trackId in note.track_id2seek)
        audio.setAttribute("data-note-seek", params.note.track_id2seek[this.trackId])

    audio.addEventListener("play", () => this.InitQuestion())
}

Question.prototype.BuildTrack = function(parent, params) {
    let track = MakeElement("track track-question track-unknown", parent, {id: `track-${this.trackId}`})
    let trackMain = MakeElement("track-main", track)

    let trackImage = MakeElement("track-image", trackMain)
    let image = MakeElement("", trackImage, {id: "track-image", src: "/images/tracks/default.png"}, "img")
    image.addEventListener("click", () => PlayPauseTrack(this.trackId))

    let div = MakeElement("", trackMain)
    this.BuildTrackTitle(div, params)
    this.BuildTrackArtists(div, params)
    this.BuildTrackControls(track, params)
    this.BuildTrackMenu(track)

    let player = MakeElement("player", track, {id: `player-${this.trackId}`})
}

Question.prototype.BuildTrackTitle = function(parent, params) {
    let trackTitle = MakeElement("track-title", parent)

    if (this.trackId in params.track_id2scale) {
        let circle = MakeElement("circle hidden", trackTitle, {id: "track-circle", style: `background-color: hsl(${params.track_id2scale[this.trackId].scale * 120}, 70%, 50%)`}, "span")
        circle.addEventListener("click", () => ShowTrackNotification(this.trackId, params.track_id2scale[this.trackId].correct, params.track_id2scale[this.trackId].incorrect))
    }

    MakeElement("", trackTitle, {id: "track-title", innerText: "НЕИЗВЕСТЕН"}, "span")
}

Question.prototype.BuildTrackArtists = function(parent, params) {
    let trackArtists = MakeElement("track-artists", parent, {id: "track-artists"})
    
    for (let i = 0; i < params.track.artists.length; i++) {
        if (i > 0)
            MakeElement("", trackArtists, {innerText: ", "}, "span")

        MakeElement("link", trackArtists, {id: `link-artist-${params.track.artists[i]}`, innerText: "unknown"}, "a")
    }

    MakeElement("", trackArtists, {innerText: " ("}, "span")
    MakeElement("link", trackArtists, {id: "track-year", target: "_blank", innerText: "?"}, "a")
    MakeElement("", trackArtists, {innerText: ")"}, "span")
}

Question.prototype.BuildTrackControls = function(parent, params) {
    let controls = MakeElement("track-controls", parent)

    let loader = MakeElement("loader hidden", controls, {"id": `loader-${this.trackId}`})
    MakeElement("", loader, {src: "/images/loader.svg"}, "img")

    let loadIcon = MakeElement("", controls, {innerHTML: TRACK_LOAD_ICON, id: `player-${this.trackId}-load`})
    let playIcon = MakeElement("hidden", controls, {innerHTML: TRACK_PLAY_ICON, id: `player-${this.trackId}-play`})
    let pauseIcon = MakeElement("hidden", controls, {innerHTML: TRACK_PAUSE_ICON, id: `player-${this.trackId}-pause`})

    loadIcon.addEventListener("click", () => PlayTrack(this.trackId))
}

Question.prototype.BuildTrackMenu = function(parent) {
    let trackMenu = MakeElement("track-menu", parent)
    let ham = MakeElement("vertical-ham", trackMenu, {id: "track-menu", disabled: ""})
    ham.addEventListener("click", () => infos.Show(`track-${this.trackId}`))

    MakeElement("", ham)
    MakeElement("", ham)
    MakeElement("", ham)
}

Question.prototype.BuildTrackModifications = function(parent) {
    let playbackRate = this.question.track_modifications.playback_rate

    if (playbackRate == 1)
        return
    
    MakeElement("track-modifications", parent, {id: "track-modifications", innerHTML: `Внимание, <b>скорость трека изменена</b>: ${Math.round(playbackRate * 100) / 100}x`})
}

Question.prototype.BuildShowAnswerButton = function(parent) {
    let button = MakeElement("basic-button gradient-button hidden", parent, {id: "show-answer", innerText: "Показать ответ"}, "button")
    button.addEventListener("click", () => this.ShowAnswer())
}

Question.prototype.BuildAnswerBlock = function(parent, params) {
    let block = MakeElement("answer-block hidden", parent, {id: "answer"})
    MakeElement("answer", block, {innerHTML: `<b>Ответ:</b> ${this.question.answer}`})
    MakeElement("description hidden", block, {innerHTML: `<b>Время ответа:</b> <span id="answer-time"></span>`})

    let buttons = MakeElement("answer-buttons", block)
    let answerCorrectButton = MakeElement("basic-button green-button", buttons, {id: "answer-button-correct", innerText: "Знаю"})
    let answerIncorrectButton = MakeElement("basic-button red-button", buttons, {id: "answer-button-incorrect", innerText: "Не знаю"})

    answerCorrectButton.addEventListener("click", () => this.onAnswer(true, this.answerTime))
    answerIncorrectButton.addEventListener("click", () => this.onAnswer(false, this.answerTime))

    this.BuildAnswerInfo(block, params)
    this.BuildLyrics(block, params)
}

Question.prototype.BuildAnswerInfo = function(parent, params) {
    MakeElement("", parent, {innerText: `Исполнител${params.track.artists.length > 1 ? "и" : "ь"}:`}, "h3")

    infos.Clear()
    let artistsBlock = MakeElement("", parent, {id: "artists"})

    for (let artist of this.artists) {
        artist = new Artist(artist)
        artistsBlock.appendChild(artist.Build(artistId2scale))
        infos.Add(artist.BuildInfo())
    }

    infos.Add(this.track.BuildInfo(artists))
}

Question.prototype.BuildLyrics = function(parent, params) {
    if (params.track.lyrics === null)
        return

    let block = MakeElement("", parent, {id: `lyrics-updater-${this.trackId}`, "data-lrc": params.track.lyrics.lrc})
    MakeElement("", block, {innerText: "Текст"}, "h3")

    let updater = MakeElement("lyrics-updater", block)
    let lines = MakeElement("lyrics-lines", updater)
    let indices = this.track.GetChorusIndices()

    for (let i = 0; i < params.track.lyrics.lines.length; i++) {
        let line = MakeElement("lyrics-line", lines, {innerText: params.track.lyrics.lines[i].text, "data-time": params.track.lyrics.lines[i].time})

        if (i in indices)
            line.classList.add("lyrics-line-chorus")

        let index1 = i in indices ? indices[i] : -1
        let index2 = (i + 1) in indices ? indices[i + 1] : -1
        if (index1 != index2)
            MakeElement("", lines, null, "br")
    }
}

Question.prototype.InitQuestion = function() {
    if (this.answerTime !== null)
        return

    let showAnswerButton = document.getElementById("show-answer")
    showAnswerButton.classList.remove("hidden")
    this.answerTime = performance.now()
}

Question.prototype.ShowAnswer = function(correct = null) {
    console.log(correct)
    if (this.answerTime !== null) {
        this.answerTime = (performance.now() - this.answerTime) / 1000
        let answerTimeSpan = document.getElementById("answer-time")
        answerTimeSpan.innerText = FormatTime(this.answerTime)
        answerTimeSpan.parentNode.classList.remove("hidden")
    }

    this.track.ReplaceUnknown(this.artists)

    let trackModifications = document.getElementById("track-modifications")
    if (trackModifications !== null)
        trackModifications.classList.add("hidden")

    let showAnswerButton = document.getElementById("show-answer")
    showAnswerButton.classList.add("hidden")

    let answerBlock = document.getElementById("answer")
    answerBlock.classList.remove("hidden")

    if (correct !== null) {
        document.getElementById("answer-button-correct").setAttribute("disabled", "")
        document.getElementById("answer-button-incorrect").setAttribute("disabled", "")
    }

    let audio = document.getElementById(`audio-${this.trackId}`)
    audio.addEventListener("play", () => {
        let player = players.GetPlayer()

        if (player === null)
            return

        player.SetTimecode("")
        player.SetPlaybackRate(1)
        player.ShowIcons()
    })
}

//     {% if artist_id2note %}
//     <div class="notes">
//         <h3>Личные заметки:</h3>

//         {% for artist_id in track.artists %}
//         {% if artist_id in artist_id2note %}
//         <div class="note"><b>{{artist_id2artist[artist_id].name}}</b>: {{artist_id2note[artist_id].text}}</div>
//         {% endif %}
//         {% endfor %}
//     </div>
//     {% endif %}
// </div>
