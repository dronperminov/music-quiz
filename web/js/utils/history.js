function GetActionDiffTracks(diff) {
    let prevValue = Object.fromEntries(diff.prev.map(value => [value.track_id, value.position]))
    let newValue = Object.fromEntries(diff.new.map(value => [value.track_id, value.position]))
    let html = []

    for (let [key, value] of Object.entries(prevValue)) {
        if (key in newValue && newValue[key] == value)
            continue

        if (key in newValue)
            html.push(`${key}: <s class="error-color">${value}</s> &rarr; <span class="success-color">${newValue[key]}</span>`)
        else
            html.push(`<s class="error-color">${key}: ${value}</s>`)
    }

    for (let [key, value] of Object.entries(newValue)) {
        if (key in prevValue)
            continue

        html.push(`<span class="success-color">${key}: ${value}</span>`)
    }

    return html.join(", ")
}

function GetActionDiffKeyValue(key, value) {
    if (key == "artist_type")
        return new ArtistType(value).ToRus()

    if (key == "genres")
        return value.map(genre => new Genre(genre).ToRus()).join(", ")

    if (key == "language")
        return new Language(value).ToRus()

    if (key == "tracks") {
        let tracks = value.map(track => `${track.track_id}: ${track.position}`).join(", ")
        return `{${tracks}}`
    }

    return JSON.stringify(value)
}

function GetActionDiff(key, diff) {
    let key2name = {
        "genres": "жанры",

        "name": "имя",
        "description": "описание",
        "tracks_count": "количество треков",
        "image_urls": "изображения",
        "artist_type": "форма записи",
        "listen_count": "количество прослушиваний",
        "tracks": "треки",

        "title": "название",
        "artists": "исполнители",
        "year": "год выхода",
        "lyrics": "текст песни",
        "duration": "длительность",
        "downloaded": "трек скачан",
        "image_url": "обложка",
        "language": "язык"
    }

    if (key == "tracks")
        return GetActionDiffTracks(diff)

    let prevValue = `<span class="error-color"><s>${GetActionDiffKeyValue(key, diff.prev)}</s></span>`
    let newValue = `<span class="success-color">${GetActionDiffKeyValue(key, diff.new)}</span>`
    return `<b>${key2name[key]}</b>: ${prevValue} &rarr; ${newValue}`
}

function BuildArtistEditAction(action, parent) {
    let diffBlock = MakeElement("action-diff", parent, {}, "ul")

    for (let [key, diff] of Object.entries(action.diff)) {
        MakeElement("action-diff-row", diffBlock, {innerHTML: GetActionDiff(key, diff)}, "li")
    }
}

function BuildHistory(parent, history) {
    let historyBlock = MakeElement("history", parent)

    let action2title = {
        "edit_artist": "Обновлён",
        "add_artist": "Добавлен",
        "edit_track": "Обновлён",
        "add_track": "Добавлен",
    }

    for (let action of history) {
        let actionBlock = MakeElement("action", historyBlock)
        let {date, time} = ParseDateTime(action.timestamp)

        MakeElement("action-header", actionBlock, {innerText: `${action2title[action.name]} @${action.username} ${date} в ${time}`})

        if (action.name == "edit_artist" || action.name == "edit_track") {
            BuildArtistEditAction(action, actionBlock)
        }
    }
}

function ShowHistory(url) {
    let info = document.getElementById("info-history")

    if (info === null) {
        let body = document.getElementsByTagName("body")[0]
        info = MakeElement("info", body, {id: "info-history"})

        MakeElement("close-icon", info, {title: "Закрыть"})
        MakeElement("info-header-line", info, {innerText: "История изменений"})
        MakeElement("info-content", info)
        infos.Add(info)
    }

    SendRequest(url).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось получить историю изменений<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
            return
        }

        info.children[info.children.length - 1].innerHTML = ""
        BuildHistory(info.children[info.children.length - 1], response.history)
        infos.Show(`history`)
    })
}
