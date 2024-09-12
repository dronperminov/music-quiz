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

function GetActionDiffLyrics(diff) {
    let html = []

    if (diff.prev === null)
        return `<b>текст песни</b>: <s class="error-color">null</s> &rarr; <span class="success-color">${JSON.stringify(diff.new)}</span></li>`

    if (diff.new === null)
        return `<b>текст песни</b>: <s class="error-color">${JSON.stringify(diff.prev)}</s> &rarr; <span class="success-color">null</span></li>`

    let prevLines = JSON.stringify(diff.prev.lines, null, 1).replace("\n", "")
    let newLines = JSON.stringify(diff.new.lines, null, 1).replace("\n", "")
    if (prevLines != newLines)
        html.push(`<li><b>строки</b>: <s class="error-color">${prevLines}</s> &rarr; <span class="success-color">${newLines}</span></li>`)

    let prevChorus = JSON.stringify(diff.prev.chorus, null, 1).replace("\n", "")
    let newChorus = JSON.stringify(diff.new.chorus, null, 1).replace("\n", "")
    if (prevChorus != newChorus)
        html.push(`<li><b>припев</b>: <s class="error-color">${prevChorus}</s> &rarr; <span class="success-color">${newChorus}</span></li>`)

    if (diff.prev.lrc != diff.new.lrc)
        html.push(`<li><b>синхронный</b>: <s class="error-color">${diff.prev.lrc}</s> &rarr; <span class="success-color">${diff.new.lrc}</span></li>`)

    if (diff.prev.validated != diff.new.validated)
        html.push(`<li><b>проверен</b>: <s class="error-color">${diff.prev.validated}</s> &rarr; <span class="success-color">${diff.new.validated}</span></li>`)

    return `<b>текст песни</b>: <ul class="action-diff">${html.join(", ")}</li>`
}

function GetActionDiffKeyValue(key, value) {
    if (key == "artist_type")
        return new ArtistType(value).ToRus()

    if (key == "genres")
        return value.map(genre => new Genre(genre).ToRus()).join(", ")

    if (key == "language")
        return new Language(value).ToRus()

    return JSON.stringify(value, null, 1).replace("\n", "")
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
        "language": "язык",

        "artist_ids": "исполнители"
    }

    if (key == "tracks")
        return GetActionDiffTracks(diff)

    if (key == "lyrics")
        return GetActionDiffLyrics(diff)

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
        "remove_track": '<b class="error-color">Удалён</b> трек',

        "edit_artists_group": "<b>Обновлена</b> группа похожих исполнителей",
        "add_artists_group": '<b class="success-color">Добавлена</b> группа похожих исполнителей',
        "remove_artists_group": '<b class="error-color">Удалена</b> группа похожих исполнителей',
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
            objectId = ` <a class="link" href="/tracks/${action.track.track_id}">${action.track.track_id}</a>`
        else if (action.name == "edit_track")
            objectId = ` <a class="link" href="/tracks/${action.track_id}">${action.track_id}</a>`
        else if (action.name == "remove_track")
            objectId = ` ${action.track_id}`
        else if (action.name == "add_artists_group")
            objectId = ` ${action.group.group_id}`
        else if (action.name == "edit_artists_group" || action.name == "remove_artists_group")
            objectId = ` ${action.group_id}`

        MakeElement("action-header", actionBlock, {innerHTML: `${action2title[action.name]}${objectId} @${action.username} ${date} в ${time}`})

        if (action.name == "edit_artist" || action.name == "edit_track" || action.name == "edit_artists_group") {
            BuildEditAction(action, actionBlock)
        }
    }
}

function ShowHistory(url, params = null) {
    let info = document.getElementById("info-history")

    if (info === null) {
        info = MakeElement("info", null, {id: "info-history"})

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
