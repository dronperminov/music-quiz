function BuildArtistEditAction(action, parent) {
    let diffBlock = MakeElement("action-diff", parent, {}, "ul")

    for (let [key, diff] of Object.entries(action.diff)) {
        MakeElement("action-diff-row", diffBlock, {innerHTML: `<b>${key}</b>: <span class="error-color"><s>${JSON.stringify(diff.prev)}</s></span> &rarr; <span class="success-color">${JSON.stringify(diff.new)}</span>`}, "li")
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
