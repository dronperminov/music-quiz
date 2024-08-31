function QuizTour(data, statuses) {
    this.quizTourId = data.quiz_tour_id
    this.quizTourType = data.quiz_tour_type
    this.name = data.name
    this.description = data.description
    this.questionIds = data.question_ids
    this.imageUrl = data.image_url
    this.createdAt = data.created_at
    this.createdBy = data.created_by
    this.tags = data.tags

    this.status = this.quizTourId in statuses ? statuses[this.quizTourId] : null
}

QuizTour.prototype.Build = function() {
    let quizTour = MakeElement("quiz-tour")

    let quizTourImage = MakeElement("quiz-tour-image", quizTour)
    let quizTourImageLink = MakeElement("", quizTourImage, {href: `/quiz-tours/${this.quizTourId}`}, "a")
    MakeElement("", quizTourImageLink, {src: this.imageUrl, loading: "lazy"}, "img")

    if (this.status !== null && this.status.lost == 0) {
        quizTour.classList.add("quiz-tour-completed")
        MakeElement("quiz-tour-completed-text", quizTourImage, {innerText: "Пройден"})
    }

    this.BuildStatus(quizTour, true)

    let quizTourName = MakeElement("quiz-tour-name", quizTour)
    MakeElement("", quizTourName, {href: `/quiz-tours/${this.quizTourId}`, innerText: this.name}, "a")

    if (this.quizTourType != "regular")
        MakeElement("quiz-tour-type", quizTour, {innerHTML: `<b>Механика</b>: ${this.QuizTourTypeToRus()}`})

    MakeElement("quiz-tour-description", quizTour, {innerText: this.description})
    MakeElement("quiz-tour-tags", quizTour, {innerHTML: `<b>Теги</b>: ${this.tags.map(tag => this.TagToRus(tag)).join(", ")}`})
    this.BuildQuestions(quizTour)

    MakeElement("quiz-tour-date", quizTour, {innerHTML: `${ParseDateTime(this.createdAt).date}`})

    return quizTour
}

QuizTour.prototype.BuildPage = function(blockId) {
    let quizTour = document.getElementById(blockId)

    let quizTourImage = MakeElement("quiz-tour-image", quizTour)
    MakeElement("", quizTourImage, {src: this.imageUrl, loading: "lazy"}, "img")

    MakeElement("quiz-tour-name", quizTour, {innerText: this.name}, "h1")
    MakeElement("quiz-tour-description", quizTour, {innerText: this.description})

    if (this.quizTourType != "regular")
        MakeElement("quiz-tour-type", quizTour, {innerHTML: `<b>Механика</b>: ${this.QuizTourTypeToRus()}`})

    MakeElement("quiz-tour-tags", quizTour, {innerHTML: `<b>Теги</b>: ${this.tags.map(tag => this.TagToRus(tag)).join(", ")}`})
}

QuizTour.prototype.QuizTourTypeToRus = function() {
    let type2rus = {
        "alphabet": "алфавит",
        "stairs": "лесенка",
        "letter": "на одну букву",
        "miracles_field": "поле чудес"
    }

    return type2rus[this.quizTourType]
}

QuizTour.prototype.TagToRus = function(tag) {
    let tag2rus = {
        "foreign": "зарубежное",
        "russian": "русское",

        "rock": "рок",
        "hip-hop": "рэп",

        "1990": "девяностые",
        "2000": "нулевые",
        "2010": "десятые",
        "modern": "современное",
        "2020": "2020-ые",

        "hits": "хиты",
        "unhackneyed": "незаезженное"
    }

    return tag2rus[tag]
}

QuizTour.prototype.IsStarted = function() {
    return this.status !== null && this.status.lost < this.questionIds.length
}

QuizTour.prototype.BuildStatus = function(quizTour) {
    if (!this.IsStarted())
        return

    let status = MakeElement("quiz-tour-status", quizTour)

    if (this.status.correct > 0)
        MakeElement("quiz-tour-status-bar quiz-tour-status-bar-correct", status, {style: `width: ${this.status.correct / this.questionIds.length * 100}%`})

    if (this.status.incorrect > 0)
        MakeElement("quiz-tour-status-bar quiz-tour-status-bar-incorrect", status, {style: `width: ${this.status.incorrect / this.questionIds.length * 100}%`})

    if (this.status.lost > 0)
        MakeElement("quiz-tour-status-bar quiz-tour-status-bar-lost", status, {style: `width: ${this.status.lost / this.questionIds.length * 100}%`})

    MakeElement("quiz-tour-time", quizTour, {innerHTML: `<b>время</b>: ${FormatTotalTime(this.status.time.total)}`})
}

QuizTour.prototype.BuildQuestions = function(quizTour) {
    let rating = this.IsStarted() ? `<span class="correct-color">${GetWordForm(this.status.correct, ['балл', 'балла', 'баллов'])}</span>, ` : ""
    let questions = GetWordForm(this.questionIds.length, ['вопрос', 'вопроса', 'вопросов'])
    MakeElement("quiz-tour-questions", quizTour, {innerHTML: `${rating}${questions}`})
}
