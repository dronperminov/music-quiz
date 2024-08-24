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

    return `<b>треки</b>: ${html.join(", ")}`
}

function GetActionDiffKeyValue(key, value) {
    if (key == "artist_type")
        return new ArtistType(value).ToRus()

    if (key == "genres")
        return value.map(genre => new Genre(genre).ToRus()).join(", ")

    if (key == "language")
        return new Language(value).ToRus()


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

function BuildEditAction(action, parent) {
    let diffBlock = MakeElement("action-diff", parent, {}, "ul")

    for (let [key, diff] of Object.entries(action.diff))
        MakeElement("action-diff-row", diffBlock, {innerHTML: GetActionDiff(key, diff)}, "li")
}

function BuildHistory(parent, history) {
    let historyBlock = MakeElement("history", parent)

    let action2title = {
        "edit_artist": "<b>Обновлён</b> исполнитель",
        "add_artist": '<b class="success-color">Добавлен</b> исполнитель',
        "remove_artist": '<b class="error-color">Удалён</b> исполнитель',
        "edit_track": "<b>Обновлён</b> трек",
        "add_track": '<b class="success-color">Добавлен</b> трек',
        "remove_track": '<b class="error-color">Удалён</b> трек'
    }

    for (let action of history) {
        let actionBlock = MakeElement("action", historyBlock)
        let {date, time} = ParseDateTime(action.timestamp)
        let objectId = ""

        if (action.name == "add_artist")
            objectId = ` <a class="link" href="/artists/${action.artist.artist_id}">${action.artist.artist_id}</a>`
        else if (action.name == "edit_artist")
            objectId = ` <a class="link" href="/artists/${action.artist_id}">${action.artist_id}</a>`
        else if (action.name == "remove_artist")
            objectId = ` ${action.artist_id}`
        else if (action.name == "add_track")
            objectId = ` ${action.track.track_id}`
        else if (action.name == "edit_track" || action.name == "remove_track")
            objectId = ` ${action.track_id}`

        MakeElement("action-header", actionBlock, {innerHTML: `${action2title[action.name]}${objectId} @${action.username} ${date} в ${time}`})

        if (action.name == "edit_artist" || action.name == "edit_track") {
            BuildEditAction(action, actionBlock)
        }
    }
}

function ShowHistory(url, params = null) {
    let info = document.getElementById("info-history")

    if (info === null) {
        let body = document.getElementsByTagName("body")[0]
        info = MakeElement("info", body, {id: "info-history"})

        MakeElement("close-icon", info, {title: "Закрыть"})
        MakeElement("info-header-line", info, {innerText: "История изменений"})
        MakeElement("info-content", info)
        infos.Add(info)
    }

    SendRequest(url, params).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось получить историю изменений<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
            return
        }

        info.children[info.children.length - 1].innerHTML = ""
        BuildHistory(info.children[info.children.length - 1], response.history)
        infos.Show(`history`)
    })
}
