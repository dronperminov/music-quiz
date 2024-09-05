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
    this.historyBlock = document.getElementById("session-history")
    this.historyActionsBlock = document.getElementById("session-history-actions")
    this.username2avatar = {}

    this.disconnectButton = document.getElementById("disconnect-button")

    this.reactionBlock = document.getElementById("reactions")
    this.reactions = ["poo", "heart", "angry", "crying", "happy", "monkey"]
}

MultiPlayer.prototype.Connect = function(sessionId, username) {
    this.sessionId = sessionId
    this.username = username
    this.ws = new WebSocket(this.GetWebsockerUrl(sessionId))

    this.ws.addEventListener("open", () => this.Open())
    this.ws.addEventListener("message", (e) => this.HandleMessage(JSON.parse(e.data)))
    this.ws.addEventListener("close", () => this.Close())
}

MultiPlayer.prototype.Open = function() {
    console.log(`Connected to the session ${this.sessionId}`)
    ShowNotification(`Connected to the session ${this.sessionId}`, "success-notification", 1500)

    this.managerBlock.classList.add("hidden")
    this.historyBlock.classList.remove("hidden")
    this.historyActionsBlock.innerHTML = ""
    this.reactionBlock.classList.remove("hidden")
    this.disconnectButton.classList.remove("hidden")
    localStorage.setItem("sessionId", this.sessionId)
}

MultiPlayer.prototype.Close = function() {
    this.ws = null

    if (this.sessionId === null) {
        console.log("Disconnected from the session")
        ShowNotification("Disconnected from the session", "success-notification", 1500)
        return
    }

    console.log(`Disconnected from the session ${this.sessionId}, try to reconnct`)
    ShowNotification(`Disconnected from the session ${this.sessionId}, try to reconnct`, "error-notification", 1500)
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
    this.disconnectButton.classList.add("hidden")
    this.sessionInfo.classList.add("hidden")
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

MultiPlayer.prototype.HandleMessage = function(session) {
    console.log(session.players, session.action)

    this.UpdateSessionInfo(session)

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

    if (session.question !== null && this.question == null)
        this.InitQuestion(session)
}

MultiPlayer.prototype.UpdateSessionInfo = function(session) {
    if (session.players.length > 0)
        this.sessionInfo.classList.remove("hidden")
    else
        this.sessionInfo.classList.add("hidden")

    this.ShowConnectedUsers(session)
    this.AppendHistory(session)
}

MultiPlayer.prototype.ShowConnectedUsers = function(session) {
    this.usersCountSpan.innerText = session.players.length
    this.usersBlock.innerHTML = ""

    for (let user of session.players)
        this.BuildConnectedUser(user, session.answers)
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
    if (["connect", "disconnect", "answer", ...this.reactions].indexOf(session.action) == -1)
        return

    let date = new Date()
    let hours = `${date.getHours()}`.padStart(2, '0')
    let minutes = `${date.getMinutes()}`.padStart(2, '0')
    let seconds = `${date.getSeconds()}`.padStart(2, '0')

    let text = null

    if (session.action == "connect") {
        text = `@${session.username} подключился`
    }
    else if (session.action == "disconnect") {
        text = `@${session.username} отключился`
    }
    else if (session.action == "answer") {
        let correct = session.answers[session.username].correct ? '<span class="correct">знаю</span>' : '<span class="incorrect">не знаю</span>'
        let time = FormatTime(session.answers[session.username].answer_time)
        text = `@${session.username} ответил ${correct} (${time})`
    }
    else if (this.reactions.indexOf(session.action) > -1) {
        text = `@${session.username} отправил <img class="reaction" src="/images/reactions/${session.action}.svg">`

        if (session.username != this.username)
            ShowNotification(`@${session.username} отправил <img class="reaction" src="/images/reactions/${session.action}.svg">`, "info-notification", 1800)
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
