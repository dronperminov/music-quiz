function Note(note) {
    this.text = note.text
    this.artistId = note.artist_id
    this.trackId2seek = note.track_id2seek
}

Note.prototype.Build = function(artist, params) {
    let note = MakeElement("artist")
    let artistImage = MakeElement("artist-image", note)
    let artistImageLink = MakeElement("", artistImage, {href: `/artists/${this.artistId}`}, "a")
    MakeElement("", artistImageLink, {src: artist.imageUrls[0], loading: "lazy"}, "img")

    let artistInfo = MakeElement("artist-data", note)

    let artistName = MakeElement("artist-name", artistInfo)
    artist.BuildScale(artistName, params.artist_id2scale)
    MakeElement("", artistName, {href: `/artists/${this.artistId}`, innerText: artist.name}, "a")

    let tracksCount = GetWordForm(Object.keys(this.trackId2seek).length, ["трек", "трека", "треков"])
    let artistNote = MakeElement("artist-note", artistInfo, {innerText: `${this.text} (${tracksCount})`})
    artistNote.addEventListener("click", () => {
        let tracks = document.getElementById(`artist-${this.artistId}-tracks`)
        tracks.classList.toggle("artist-tracks-open")
    })

    let artistMenu = MakeElement("artist-menu", note)
    let verticalHam = MakeElement("vertical-ham", artistMenu, {innerHTML: "<div></div><div></div><div></div>"})
    verticalHam.addEventListener("click", () => infos.Show(`artist-${this.artistId}`))

    return note
}

Note.prototype.BuildTracks = function(artist, params) {
    let tracks = MakeElement("artist-tracks", null, {id: `artist-${this.artistId}-tracks`})

    for (let [trackId, seek] of Object.entries(this.trackId2seek)) {
        let track = new Track(params.track_id2track[`${trackId}`])
        infos.Add(track.BuildInfo())

        console.log(params)
        this.BuildAudio(track, seek, tracks, params)
        this.BuildTrack(track, tracks, params)
    }

    return tracks
}

Note.prototype.BuildAudio = function(track, seek, parent, params) {
    let audio = MakeElement("", parent, {}, "audio")

    audio.setAttribute("id", `audio-${track.trackId}`)
    audio.setAttribute("data-track-id", track.trackId)
    audio.setAttribute("preload", "metadata")

    if (track.downloaded)
        audio.setAttribute("data-src", `https://music.dronperminov.ru/tracks/${track.trackId}.mp3`)
    else
        audio.setAttribute("data-yandex-id", track.source.yandex_id)

    audio.setAttribute("data-seek", seek)
    audio.setAttribute("data-note-seek", seek)
}

Note.prototype.BuildTrack = function(track, parent, params) {
    let trackBlock = MakeElement("track", parent, {id: `track-${track.trackId}`})
    let trackMain = MakeElement("track-main", trackBlock)

    let trackImage = MakeElement("track-image", trackMain)
    let image = MakeElement("", trackImage, {id: "track-image", src: track.imageUrl}, "img")
    image.addEventListener("click", () => PlayPauseTrack(track.trackId))
    if (track.lyrics)
        MakeElement("track-image-lyrics", trackImage, {innerText: "T"})

    let div = MakeElement("", trackMain)
    this.BuildTrackTitle(track, div, params)
    this.BuildTrackArtists(track, div, params)
    this.BuildTrackControls(track, trackMain, params)
    this.BuildTrackMenu(track.trackId, trackMain)

    let player = MakeElement("player", trackBlock, {id: `player-${track.trackId}`})

    this.BuildLyrics(track, trackBlock)
}

Note.prototype.BuildTrackTitle = function(track, parent, params) {
    let trackTitle = MakeElement("track-title", parent)
    let scale = `${track.trackId}` in params.track_id2scale ? params.track_id2scale[`${track.trackId}`] : null

    if (scale !== null) {
        let circle = MakeElement("circle", trackTitle, {id: "track-circle", style: `background-color: hsl(${scale.scale * 120}, 70%, 50%)`}, "span")
        circle.addEventListener("click", () => ShowTrackNotification(track.trackId, scale.correct, scale.incorrect))
    }

    MakeElement("", trackTitle, {id: "track-title", innerText: track.title}, "span")
}

Note.prototype.BuildTrackArtists = function(track, parent, params) {
    let trackArtists = MakeElement("track-artists", parent, {id: "track-artists"})
    
    for (let i = 0; i < track.artists.length; i++) {
        if (i > 0)
            MakeElement("", trackArtists, {innerText: ", "}, "span")

        MakeElement("link", trackArtists, {innerText: params.artist_id2artist[`${track.artists[i]}`].name}, "a")
    }

    MakeElement("", trackArtists, {innerText: " ("}, "span")
    MakeElement("link", trackArtists, {id: "track-year", target: "_blank", innerText: track.year}, "a")
    MakeElement("", trackArtists, {innerText: ")"}, "span")
}

Note.prototype.BuildTrackControls = function(track, parent, params) {
    let controls = MakeElement("track-controls", parent)

    let loader = MakeElement("loader hidden", controls, {"id": `loader-${track.trackId}`})
    MakeElement("", loader, {src: "/images/loader.svg"}, "img")

    let loadIcon = MakeElement("", controls, {innerHTML: TRACK_LOAD_ICON, id: `player-${track.trackId}-load`})
    let playIcon = MakeElement("hidden", controls, {innerHTML: TRACK_PLAY_ICON, id: `player-${track.trackId}-play`})
    let pauseIcon = MakeElement("hidden", controls, {innerHTML: TRACK_PAUSE_ICON, id: `player-${track.trackId}-pause`})

    loadIcon.addEventListener("click", () => PlayTrack(track.trackId))
}

Note.prototype.BuildTrackMenu = function(trackId, parent) {
    let trackMenu = MakeElement("track-menu", parent)
    let ham = MakeElement("vertical-ham", trackMenu, {id: "track-menu"})
    ham.addEventListener("click", () => infos.Show(`track-${trackId}`))

    MakeElement("", ham)
    MakeElement("", ham)
    MakeElement("", ham)
}

Note.prototype.BuildLyrics = function(track, parent) {
    if (track.lyrics === null)
        return

    let block = MakeElement("hidden", parent, {id: `lyrics-updater-${track.trackId}`, "data-lrc": track.lyrics.lrc})
    let updater = MakeElement("lyrics-updater", block)
    let lines = MakeElement("lyrics-lines", updater)
    let indices = track.GetChorusIndices()

    for (let i = 0; i < track.lyrics.lines.length; i++) {
        let line = MakeElement("lyrics-line", lines, {innerText: track.lyrics.lines[i].text, "data-time": track.lyrics.lines[i].time})

        if (i in indices)
            line.classList.add("lyrics-line-chorus")

        let index1 = i in indices ? indices[i] : -1
        let index2 = (i + 1) in indices ? indices[i + 1] : -1
        if (index1 != index2)
            MakeElement("", lines, null, "br")
    }
}
