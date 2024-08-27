function ArtistsGroup(data, tracksCount) {
    this.groupId = data.group_id
    this.name = data.name
    this.description = data.description
    this.artistIds = data.artist_ids
    this.imageUrl = data.image_url
    this.metadata = new Metadata(data.metadata, "Создана", "Обновлена")
    this.tracksCount = tracksCount
}

ArtistsGroup.prototype.Build = function(groupId2scale) {
    let group = MakeElement("artists-group")
    let groupImage = MakeElement("artists-group-image", group)
    let groupImageLink = MakeElement("", groupImage, {href: `/artists-groups/${this.groupId}`}, "a")
    let groupImageImg = MakeElement("", groupImageLink, {src: this.imageUrl, loading: "lazy"}, "img")

    let groupData = MakeElement("artists-group-data", group)
    let groupName = MakeElement("artists-group-name", groupData)

    if (groupId2scale !== null && this.groupId in groupId2scale) {
        let scale = groupId2scale[this.groupId]
        let circle = MakeElement("circle", groupName, {style: `background-color: hsl(${scale.scale * 120}, 70%, 50%)`})
        let correct = GetWordForm(scale.correct, ['корректный', 'корректных', 'корректных'])
        let incorrect = GetWordForm(scale.incorrect, ['некорректный', 'некорректных', 'некорректных'])
        circle.addEventListener("click", () => ShowNotification(`<b>${this.name}</b>: ${correct} и ${incorrect}`, 'info-notification', 3000))
    }

    let groupNameLink = MakeElement("", groupName, {href: `/artists-groups/${this.groupId}`, innerText: this.name}, "a")

    let groupDescription = MakeElement("artists-group-description", groupData, {innerText: this.description})
    let groupStats = MakeElement("artists-group-stats", groupData, {innerHTML: this.GetStats()})
    let groupLink = MakeElement("gradient-link", groupData, {href: `/group-question/${this.groupId}`, innerText: "К вопросам!"}, "a")

    let groupMenu = MakeElement("artists-group-menu", group)
    let verticalHam = MakeElement("vertical-ham", groupMenu, {innerHTML: "<div></div><div></div><div></div>"})
    verticalHam.addEventListener("click", () => infos.Show(`artists-group-${this.groupId}`))

    return group
}

ArtistsGroup.prototype.BuildInfo = function(artistId2name) {
    let info = MakeElement("info")
    info.setAttribute("id", `info-artists-group-${this.groupId}`)

    let closeIcon = MakeElement("close-icon", info, {title: "Закрыть"})
    let infoImage = MakeElement("info-image", info)
    let img = MakeElement("", infoImage, {src: this.imageUrl, loading: "lazy"}, "img")

    MakeElement("info-header-line", info, {innerHTML: this.name})

    if (this.description.length > 0)
        MakeElement("info-description-line", info, {innerHTML: this.description})

    if (this.artistIds.length > 0) {
        let artists = this.artistIds.map(artistId => `<li><a class="link" href="/artists/${artistId}">${artistId2name[artistId]}</a></li>`).join("")
        MakeElement("info-line", info, {innerHTML: `<p><b>Исполнители:</b></p><ul>${artists}</ul>`})
    }

    MakeElement("info-line", info, {innerHTML: `<b>Количество треков:</b> ${this.tracksCount}`})

    this.metadata.BuildInfo(info)

    this.BuildAdmin(info)
    return info
}

ArtistsGroup.prototype.BuildAdmin = function(block) {
    let adminBlock = MakeElement("admin-buttons admin-block", block)

    let historyButton = MakeElement("basic-button gradient-button", adminBlock, {innerText: "История изменений"}, "button")
    historyButton.addEventListener("click", () => ShowHistory(`/artists-group-history/${this.groupId}`))

    let removeButton = MakeElement("basic-button red-button", adminBlock, {innerText: "Удалить группу"}, "button")
    removeButton.addEventListener("click", () => this.Remove([removeButton]))
}

ArtistsGroup.prototype.GetStats = function() {
    let artists = GetWordForm(this.artistIds.length, ['исполнитель', 'исполнителя', 'исполнителей'])
    let tracks = GetWordForm(this.tracksCount, ['трек', 'трека', 'треков'])
    return [artists, tracks].join(", ")
}

ArtistsGroup.prototype.Remove = function(buttons) {
    if (!confirm(`Вы уверены, что хотите удалить группу "${this.name}"?`))
        return

    for (let button of buttons)
        button.setAttribute("disabled", "")

    SendRequest("/remove-artists-group", {group_id: this.groupId}).then(response => {
        if (response.status != SUCCESS_STATUS) {
            for (let button of buttons)
                button.removeAttribute("disabled")

            ShowNotification(`Не удалось удалить группу "${this.name}".<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
            return
        }

        location.reload()
    })
}
