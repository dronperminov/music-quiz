function MultiPlayer() {
    this.ws = null
    this.sessionId = null
    this.username = null

    this.question = null
    this.pageHeaderBlock = document.getElementById("page-header")
    this.questionBlock = document.getElementById("question")
    this.managerBlock = document.getElementById("multi-player-manager")

    this.sessionInfo = document.getElementById("session-info")
    this.usersCountSpan = document.getElementById("connected-users-count")
    this.usersBlock = document.getElementById("connected-users")
    this.statisticsBlock = document.getElementById("session-statistics")
    this.statisticsItems = document.getElementById("session-statistics-items")
    this.historyBlock = document.getElementById("session-history")
    this.historyActionsBlock = document.getElementById("session-history-actions")
    this.username2avatar = {}

    this.connectionBlock = document.getElementById("connection-block")
    this.removeSessionButton = document.getElementById("remove-session-button")

    this.reactionBlock = document.getElementById("reactions")
    this.reactions = ["poo", "heart", "angry", "crying", "happy", "monkey", "party-popper", "clapping"]
}

MultiPlayer.prototype.Connect = function(sessionId, username) {
    this.sessionId = sessionId
    this.username = username

    this.ws = new WebSocket(this.GetWebsockerUrl(sessionId))
    this.ws.onopen = () => this.Open()
    this.ws.onmessage = (e) => this.HandleMessage(e.data)
    this.ws.onclose = () => this.Close()
    this.ws.onerror = (error) => this.HandleError(error)
}

MultiPlayer.prototype.Open = function() {
    this.managerBlock.classList.add("hidden")
    this.historyBlock.classList.remove("hidden")
    this.historyActionsBlock.innerHTML = ""
    this.statisticsBlock.classList.remove("hidden")
    this.reactionBlock.classList.remove("hidden")
    this.connectionBlock.classList.remove("hidden")
    document.querySelector("body").classList.add("hidden-menu")

    localStorage.setItem("sessionId", this.sessionId)

    ShowNotification(`Подключение к сессии ${this.sessionId} установлено<br>Меню будет скрыто на время игры`, "success-notification", 2500)
}

MultiPlayer.prototype.Close = function() {
    this.ws = null

    if (this.sessionId === null) {
        ShowNotification("Подключение к сессии разорвано", "success-notification", 1500)
        return
    }

    ShowNotification(`Подключение к сессии ${this.sessionId} неожиданно разорвано, пробую переподключиться`, "error-notification", 1500)
    setTimeout(() => this.Connect(this.sessionId, this.username), 1000)
}

MultiPlayer.prototype.Disconnect = function() {
    if (this.ws === null)
        return

    this.sessionId = null
    this.username = null
    this.ws.close()

    this.managerBlock.classList.remove("hidden")
    this.historyBlock.classList.add("hidden")
    this.reactionBlock.classList.add("hidden")
    this.connectionBlock.classList.add("hidden")
    this.sessionInfo.classList.add("hidden")
    document.querySelector("body").classList.remove("hidden-menu")
    this.ClearQuestion()

    localStorage.removeItem("sessionId")
}

MultiPlayer.prototype.GetWebsockerUrl = function(sessionId) {
    let protocol = location.protocol == "https:" ? "wss" : "ws"
    let host = window.location.host

    return `${protocol}://${host}/ws/${sessionId}`
}

MultiPlayer.prototype.IsAllAnswered = function(session) {
    for (let player of session.players)
        if (!(player.username in session.answers))
            return false

    return true
}

MultiPlayer.prototype.HandleMessage = function(message) {
    if (message === "ping") {
        this.ws.send("pong")
        return
    }

    let session = JSON.parse(message)
    this.UpdateSessionInfo(session)

    if (session.action == "remove") {
        this.Disconnect()
        return
    }

    if (session.action == "disconnect" && session.username == session.created_by) {
        this.Disconnect()
        return
    }

    if (session.players.length < 2) {
        this.ClearQuestion()
        return
    }

    if (session.question === null || this.IsAllAnswered(session)) {
        this.ClearQuestion()
        Start()
    }

    if (session.question !== null && (this.question == null || session.question.track_id != this.question.trackId))
        this.InitQuestion(session)
}

MultiPlayer.prototype.HandleError = function(error) {
    ShowNotification(`Произошла ошибка вебсокета: ${error}`, "error-notification", 2000)
}

MultiPlayer.prototype.UpdateSessionInfo = function(session) {
    if (session.players.length > 0)
        this.sessionInfo.classList.remove("hidden")
    else
        this.sessionInfo.classList.add("hidden")

    this.ShowConnectedUsers(session)
    this.ShowStatistics(session)
    this.AppendHistory(session)
}

MultiPlayer.prototype.ShowConnectedUsers = function(session) {
    this.usersCountSpan.innerText = session.players.length
    this.usersBlock.innerHTML = ""

    if (session.created_by == this.username)
        this.removeSessionButton.classList.remove("hidden")
    else
        this.removeSessionButton.classList.add("hidden")

    for (let user of session.players)
        this.BuildConnectedUser(user, session.answers)
}

MultiPlayer.prototype.ShowStatistics = function(session) {
    this.statisticsItems.innerHTML = ""

    for (let [username, answers] of Object.entries(session.statistics))
        this.BuildUserStatistics(username, answers)

    if (this.statisticsItems.children.length > 0)
        this.statisticsBlock.classList.remove("hidden")
    else
        this.statisticsBlock.classList.add("hidden")
}

MultiPlayer.prototype.BuildConnectedUser = function(user, answers) {
    this.username2avatar[user.username] = user.avatar_url

    let block = MakeElement("connected-user", this.usersBlock)
    MakeElement("", block, {src: user.avatar_url}, "img")

    if (!(user.username in answers))
        return

    if (answers[user.username].correct)
        block.classList.add("answered-correct-user")
    else
        block.classList.add("answered-incorrect-user")
}

MultiPlayer.prototype.BuildUserStatistics = function(username, answers) {
    if (answers.length == 0 || !(username in this.username2avatar))
        return

    let correct = 0
    let incorrect = 0
    let time = 0

    for (let answer of answers) {
        if (answer.correct)
            correct += 1
        else
            incorrect += 1

        time += answer.answer_time
    }

    let meanTime = FormatTime(time / answers.length)
    let correctText = `<span class="correct-color">${GetWordForm(correct, ['верный', 'верных', 'верных'])}</span>`
    let incorrectText = `<span class="incorrect-color">${GetWordForm(incorrect, ['неверный', 'неверных', 'неверных'])}</span>`

    let block = MakeElement("session-statistics-item", this.statisticsItems)
    MakeElement("", block, {src: this.username2avatar[username]}, "img")
    MakeElement("", block, {innerHTML: `@${username}: ${correctText}, ${incorrectText} (${meanTime})`})
}

MultiPlayer.prototype.InitQuestion = function(session) {
    this.ClearQuestion()

    this.pageHeaderBlock.classList.add("hidden")
    this.question = new Question(session.question, (correct, answerTime) => SendMultiplayerAnswer(correct, answerTime))
    this.question.Build(this.questionBlock, session)
    this.reactionBlock.classList.remove("hidden")

    if (this.username in session.answers) {
        this.question.answerTime = session.answers[this.username].answer_time
        this.question.ShowAnswer(session.answers[this.username].correct)
    }

    PlayTrack(this.question.trackId)
}

MultiPlayer.prototype.ClearQuestion = function() {
    this.pageHeaderBlock.classList.remove("hidden")
    this.reactionBlock.classList.add("hidden")
    this.questionBlock.innerHTML = ""
    this.question = null

    players.Clear()
    infos.Clear()
}

MultiPlayer.prototype.AppendHistory = function(session) {
    if (["connect", "disconnect", "remove", "answer", ...this.reactions].indexOf(session.action) == -1)
        return

    let date = new Date()
    let hours = `${date.getHours()}`.padStart(2, '0')
    let minutes = `${date.getMinutes()}`.padStart(2, '0')
    let seconds = `${date.getSeconds()}`.padStart(2, '0')

    let text = null

    if (session.action == "connect") {
        text = `@${session.username} подключился`

        if (session.username != this.username)
            ShowNotification(text, "info-notification", 1500)
    }
    else if (session.action == "disconnect") {
        text = `@${session.username} отключился`

        if (session.username != this.username)
            ShowNotification(text, "info-notification", 1500)
    }
    else if (session.action == "remove" && session.username == session.created_by) {
        text = `@${session.username} удалил сессию`
        ShowNotification(`@${session.username} удалил сессию`, "error-notification", 4000)
    }
    else if (session.action == "answer") {
        let correct = session.answers[session.username].correct ? '<span class="correct">знаю</span>' : '<span class="incorrect">не знаю</span>'
        let time = FormatTime(session.answers[session.username].answer_time)
        text = `@${session.username} ответил ${correct} (${time})`

        if (session.username != this.username)
            ShowNotification(text, "info-notification", 1500)
    }
    else if (this.reactions.indexOf(session.action) > -1) {
        text = `@${session.username} отправил <img class="reaction" src="/images/reactions/${session.action}.svg">`
        ShowNotification(text, "info-notification", 1800)
    }

    let action = MakeElement("session-history-action", null)
    let user = MakeElement("session-history-action-user", action)
    MakeElement("", user, {src: this.username2avatar[session.username]}, "img")
    MakeElement("", action, {innerHTML: `${hours}:${minutes}:${seconds}: ${text}`})

    this.historyActionsBlock.prepend(action)
}

MultiPlayer.prototype.SendReaction = function(reaction) {
    this.ws.send(reaction)
}
