function UpdateMainSettings() {
    let settings = {
        show_progress: document.getElementById("show-progress").checked,
        autoplay: document.getElementById("autoplay").checked,
        show_knowledge_status: document.getElementById("show-knowledge-status").checked
    }

    SendRequest("/main_settings", settings).then(response => {
        if (response.status != SUCCESS_STATUS)
            ShowNotification(`<b>Ошибка</b>: не удалось обновить настройки<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
        else
            ShowNotification(`Настройки успешно обновлены`, "success-notification", 1000)
    })
}

function UpdateQuestionSettings() {
    let settings = GetQuestionSettings()
    if (settings === null)
        return

    SendRequest("/question_settings", settings).then(response => {
        if (response.status != SUCCESS_STATUS)
            ShowNotification(`<b>Ошибка</b>: не удалось обновить настройки вопросов<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
        else
            ShowNotification(`Настройки вопросов успешно обновлены`, "success-notification", 1000)
    })
}

function UpdateArtistsGroupSettings() {
    let settings = GetArtistsGroupSettings()
    if (settings === null)
        return

    SendRequest("/artists_group_settings", settings).then(response => {
        if (response.status != SUCCESS_STATUS)
            ShowNotification(`<b>Ошибка</b>: не удалось обновить настройки групп<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
        else
            ShowNotification(`Настройки групп успешно обновлены`, "success-notification", 1000)
    })
}
