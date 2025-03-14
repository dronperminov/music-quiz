function GetQuizTourParams() {
    let name = nameInput.GetValue()
    if (name === null)
        return null

    let description = descriptionInput.GetValue()
    if (description === null)
        return null

    let questionsCount = questionsCountInput.GetValue()
    if (questionsCount === null)
        return null

    let years = document.getElementById("quiz-tour-years").value
    let genres = document.getElementById("quiz-tour-genres").value
    let language = document.getElementById("quiz-tour-language").value
    let positions = document.getElementById("quiz-tour-positions").value
    let mechanics = document.getElementById("quiz-tour-mechanics").value
    let imageDir = document.getElementById("quiz-tour-image-dir").value

    let listenCount = listenCountInput.GetValue()
    if (listenCount === null)
        return null

    return {
        name: name,
        description: description,
        questions_count: questionsCount,
        years: years,
        genres: genres,
        language: language,
        positions: positions,
        mechanics: mechanics,
        image_dir: imageDir,
        listen_count: listenCount
    }
}

function AddQuizTour() {
    let params = GetQuizTourParams()
    if (params === null)
        return

    if (!confirm(`Вы уверены, что хотите создать квиз "${params.name}" с этими параметрами?`))
        return

    SendRequest("/add-quiz-tour", params).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`<b>Ошибка</b>: не удалось создать мини-квиз<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
            return
        }

        ShowNotification(`Мини-квиз успешно добавлен`, "success-notification", 2000)
        nameInput.SetValue("")
        document.getElementById("quiz-tour-description").value = ""
    })
}
