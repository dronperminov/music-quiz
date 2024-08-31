function BuildTopPlayers(players, topCount = 10) {
    let topPlayers = document.getElementById("top-players")

    if (players.length == 0)
        topPlayers.innerHTML = "Нет квизов, удовлетворяющих заданным параметрам"

    for (let i = 0; i < players.length && i < topCount; i++) {
        let user = players[i][0]

        let topPlayer = MakeElement("top-player", topPlayers)

        MakeElement("top-player-place", topPlayer, {innerText: i + 1})

        let image = MakeElement("top-player-image", topPlayer)
        let link = MakeElement("", image, {href: `/analytics?username=${user.username}`}, "a")
        MakeElement("", link, {src: user.avatar_url}, "img")

        let name = MakeElement("top-player-name", topPlayer, {innerText: user.full_name})
        MakeElement("top-player-tours-count", name, {innerText: GetWordForm(players[i][2], ['мини-квиз', 'мини-квиза', 'мини-квизов'])})

        let rating = MakeElement("top-player-rating", topPlayer)
        MakeElement("", rating, {src: "/images/rating.svg"}, "img")
        MakeElement("", rating, {innerText: players[i][1]}, "span")
    }
}

function ShowTopPlayers() {
    let loader = document.getElementById("loader")
    loader.classList.remove("hidden")

    let tags = tagsInput.GetValue()
    tagsInput.Disable()

    let topPlayers = document.getElementById("top-players")
    topPlayers.innerHTML = ""

    SendRequest("/get-top-players", {tags: tags}).then(response => {
        tagsInput.Enable()
        loader.classList.add("hidden")

        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось получить данные об игроках<br><b>Причина:</b> ${response.message}`, "error-notification", 3500)
            return
        }

        BuildTopPlayers(response.players)
    })
}
