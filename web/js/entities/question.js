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

    this.BuildQuestionLines(parent)
    this.BuildAudio(parent, params)
    this.BuildTrack(parent, params)
    this.BuildTrackModifications(parent)
    this.BuildShowAnswerButton(parent)
    this.BuildAnswerBlock(parent, params)

    parent.classList.remove("hidden")
}

Question.prototype.BuildQuestionLines = function(parent) {
    if (!this.question.lines)
        return

    let lines = MakeElement("question-lines", parent)

    for (let line of this.question.lines)
        MakeElement("question-line", lines, {innerText: line})
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

    if (this.question.answer_seek)
        audio.setAttribute("data-answer-seek", this.question.answer_seek)

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
        artistsBlock.appendChild(artist.Build(params.artist_id2scale))
        infos.Add(artist.BuildInfo())
    }

    infos.Add(this.track.BuildInfo(artists))
}

Question.prototype.BuildLyrics = function(parent, params) {
    if (params.track.lyrics === null)
        return

    let block = MakeElement("hidden", parent, {id: `lyrics-updater-${this.trackId}`, "data-lrc": params.track.lyrics.lrc})
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

Question.prototype.ShowAnswer = function(correct = null, answerTime = null) {
    if (answerTime !== null)
        this.answerTime = answerTime
    else if (this.answerTime !== null)
        this.answerTime = (performance.now() - this.answerTime) / 1000

    if (this.answerTime !== null) {
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

    this.ResetPlayer()
    this.UpdateAnswerButtons(correct)
}

Question.prototype.UpdateAnswerButtons = function(correct = null) {
    if (correct === null)
        return

    let buttons = {
        "true": document.getElementById("answer-button-correct"),
        "false": document.getElementById("answer-button-incorrect")
    }

    for (let [value, button] of Object.entries(buttons)) {
        button.setAttribute("disabled", "")
        if (value !== `${correct}`)
            button.classList.add("hidden")
    }
}

Question.prototype.ResetPlayer = function() {
    let player = players.GetPlayer()

    if (player !== null) {
        player.Reset()

        if (this.question.answer_seek)
            player.Seek(this.question.answer_seek)
        return
    }

    setTimeout(() => this.ResetPlayer(), 1000)
}
