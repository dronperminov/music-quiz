function QuizTour(data) {
    this.quizTourId = data.quiz_tour_id
    this.quizTourType = data.quiz_tour_type
    this.name = data.name
    this.description = data.description
    this.questionIds = data.question_ids
    this.imageUrl = data.image_url
    this.createdAt = data.created_at
    this.createdBy = data.created_by
}

QuizTour.prototype.Build = function() {
    let quizTour = MakeElement("quiz-tour")

    let quizTourImage = MakeElement("quiz-tour-image", quizTour)
    let quizTourImageLink = MakeElement("", quizTourImage, {href: `/quiz-tours/${this.quizTourId}`}, "a")
    MakeElement("", quizTourImageLink, {src: this.imageUrl, loading: "lazy"}, "img")

    let quizTourName = MakeElement("quiz-tour-name", quizTour)
    MakeElement("", quizTourName, {href: `/quiz-tours/${this.quizTourId}`, innerText: this.name}, "a")

    MakeElement("quiz-tour-description", quizTour, {innerText: this.description})
    MakeElement("quiz-tour-questions", quizTour, {innerHTML: `${GetWordForm(this.questionIds.length, ['вопрос', 'вопроса', 'вопросов'])}`})
    MakeElement("quiz-tour-date", quizTour, {innerHTML: `${ParseDateTime(this.createdAt).date}`})

    return quizTour
}
