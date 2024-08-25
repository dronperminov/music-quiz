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

    let startFromChorus = document.getElementById("start-from-chorus").checked
    let showSimpleArtistType = document.getElementById("show-simple-artist-type").checked

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

    let blackList = []

    let trackModificationSettings = GetTrackModificationSettings()
    if (trackModificationSettings === null)
        return null

    let repeatIncorrectProbability = repeatIncorrectProbabilityInput.GetValue()
    if (repeatIncorrectProbability === null)
        return null

    return {
        answer_time: answerTime,
        start_from_chorus: startFromChorus,
        show_simple_artist_type: showSimpleArtistType,
        genres: genres,
        years: years,
        languages: languages,
        artists_count: artistsCount,
        listen_count: listenCount,
        question_types: questionTypes,
        track_position: trackPosition,
        black_list: blackList,
        repeat_incorrect_probability: repeatIncorrectProbability / 100,
        track_modifications: trackModificationSettings
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
