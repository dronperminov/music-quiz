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

function GetYearsList(yearsSettings) {
    let years = []

    for (let [year, scale] of Object.entries(yearsSettings)) {
        let [startYear, endYear] = year.split("-")
        if (startYear !== "")
            startYear = +startYear

        if (endYear !== "")
            endYear = +endYear

        years.push({start_year: startYear, end_year: endYear, scale: scale})
    }

    return years
}

function GetYearsDict(yearsSettings) {
    let years = {}

    for (let year of yearsSettings)
        years[`${year.start_year}-${year.end_year}`] = year.scale

    return years
}

function GetQuestionSettings(yearsToList = false) {
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
        years: yearsToList ? GetYearsList(years) : years,
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

function GetArtistsGroupSettings() {
    let maxVariants = maxVariantsInput.GetValue()

    if (maxVariants === null)
        return null

    return {
        max_variants: maxVariants,
    }
}
