function GetTrackModificationSettings() {
    let changePlaybackRate = document.getElementById("change-playback-rate").checked
    let probability = trackModificationsProbabilityInput.GetValue()

    if (probability === null)
        return null

    return {
        change_playback_rate: changePlaybackRate,
        probability: probability / 100
    }
}

function GetQuestionSettings() {
    let answerTime = answerTimeInput.GetValue()
    if (answerTime === null)
        return null

    let genres = genresInput.GetValue()
    if (genres === null)
        return null

    let years = yearsInput.GetValue()
    if (years === null)
        return null

    let languages = languagesInput.GetValue()
    if (languages === null)
        return null

    let artistsCount = artistsCountInput.GetValue()
    if (artistsCount === null)
        return null

    let listenCount = listenCountInput.GetValue()
    if (listenCount === null)
        return null

    let questionTypes = questionTypesInput.GetValue()
    if (questionTypes === null)
        return null

    let trackPosition = trackPositionInput.GetValue()
    if (trackPosition === null)
        return null

    let startFromChorus = document.getElementById("start-from-chorus").checked
    let blackList = []

    let trackModificationSettings = GetTrackModificationSettings()
    if (trackModificationSettings === null)
        return null

    let repeatIncorrectProbability = repeatIncorrectProbabilityInput.GetValue()
    if (repeatIncorrectProbability === null)
        return null

    return {
        answer_time: answerTime,
        genres: genres,
        years: years,
        languages: languages,
        artists_count: artistsCount,
        listen_count: listenCount,
        question_types: questionTypes,
        track_position: trackPosition,
        start_from_chorus: startFromChorus,
        black_list: blackList,
        track_modifications: trackModificationSettings,
        repeat_incorrect_probability: repeatIncorrectProbability / 100
    }
}

function UpdateMainSettings() {
    let settings = {
        show_progress: document.getElementById("show-progress").checked,
        autoplay: document.getElementById("autoplay").checked,
        show_knowledge_status: document.getElementById("show-knowledge-status").checked
    }

    SendRequest("/main_settings", settings).then(response => {
        if (response.status != SUCCESS_STATUS)
            ShowNotification(`<b>Ошибка</b>: не удалось обновить настройки<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
    })
}

function UpdateQuestionSettings() {
    let settings = GetQuestionSettings()
    if (settings === null)
        return

    let saveButton = document.getElementById("save-button")
    saveButton.setAttribute("disabled", "")

    SendRequest("/question_settings", settings).then(response => {
        saveButton.removeAttribute("disabled")

        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`<b>Ошибка</b>: не удалось обновить настройки вопросов<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
            return
        }

        saveButton.classList.add("hidden")
    })
}
