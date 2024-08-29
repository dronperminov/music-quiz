function QuizTour(data, statuses) {
    this.quizTourId = data.quiz_tour_id
    this.quizTourType = data.quiz_tour_type
    this.name = data.name
    this.description = data.description
    this.questionIds = data.question_ids
    this.imageUrl = data.image_url
    this.createdAt = data.created_at
    this.createdBy = data.created_by

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

    this.BuildStatus(quizTour)

    let quizTourName = MakeElement("quiz-tour-name", quizTour)
    MakeElement("", quizTourName, {href: `/quiz-tours/${this.quizTourId}`, innerText: this.name}, "a")

    if (this.quizTourType != "regular")
        MakeElement("quiz-tour-type", quizTour, {innerHTML: `<b>Механика</b>: ${this.QuizTourTypeToRus()}`})

    MakeElement("quiz-tour-description", quizTour, {innerText: this.description})
    MakeElement("quiz-tour-questions", quizTour, {innerHTML: `${GetWordForm(this.questionIds.length, ['вопрос', 'вопроса', 'вопросов'])}`})
    MakeElement("quiz-tour-date", quizTour, {innerHTML: `${ParseDateTime(this.createdAt).date}`})

    return quizTour
}

QuizTour.prototype.QuizTourTypeToRus = function() {
    let type2rus = {
        "alphabet": "алфавит",
        "stairs": "лесенка"
    }

    return type2rus[this.quizTourType]
}

QuizTour.prototype.BuildStatus = function(quizTour) {
    if (this.status === null || this.status.lost == this.questionIds.length)
        return

    let status = MakeElement("quiz-tour-status", quizTour)

    if (this.status.correct > 0)
        MakeElement("quiz-tour-status-bar quiz-tour-status-bar-correct", status, {style: `width: ${this.status.correct / this.questionIds.length * 100}%`})

    if (this.status.incorrect > 0)
        MakeElement("quiz-tour-status-bar quiz-tour-status-bar-incorrect", status, {style: `width: ${this.status.incorrect / this.questionIds.length * 100}%`})

    if (this.status.lost > 0)
        MakeElement("quiz-tour-status-bar quiz-tour-status-bar-lost", status, {style: `width: ${this.status.lost / this.questionIds.length * 100}%`})
}
