function BuildTopPlayers(players, topCount = 10) {
    let topPlayers = document.getElementById("top-players")
    topPlayers.innerHTML = ""

    if (players.length == 0)
        topPlayers.innerHTML = "Нет квизов, удовлетворяющих заданным параметрам"

    for (let i = 0; i < players.length && i < topCount; i++) {
        let user = players[i][0]

        let topPlayer = MakeElement("top-player", topPlayers)

        MakeElement("top-player-place", topPlayer, {innerText: i + 1})

        let image = MakeElement("top-player-image", topPlayer)
        let link = MakeElement("", image, {href: `/analytics?username=${user.username}`}, "a")
        MakeElement("", link, {src: user.avatar_url}, "img")

        MakeElement("top-player-name", topPlayer, {innerText: user.full_name})

        let rating = MakeElement("top-player-rating", topPlayer)
        MakeElement("", rating, {src: "/images/rating.svg"}, "img")
        MakeElement("", rating, {innerText: players[i][1]}, "span")
    }
}

function ShowTopPlayers() {
    let tags = tagsInput.GetValue()
    tagsInput.Disable()

    SendRequest("/get-top-players", {tags: tags}).then(response => {
        tagsInput.Enable()

        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось получить данные об игроках<br><b>Причина:</b> ${response.message}`, "error-notification", 3500)
            return
        }

        BuildTopPlayers(response.players)
    })
}
