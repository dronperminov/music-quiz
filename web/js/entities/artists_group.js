function ArtistsGroup(data) {
    this.groupId = data.group_id
    this.name = data.name
    this.description = data.description
    this.artistIds = data.artist_ids
    this.imageUrl = data.image_url
    this.metadata = new Metadata(data.metadata, "Создана", "Обновлена")
}

ArtistsGroup.prototype.Build = function(groupId2scale) {
    let group = MakeElement("artists-group")
    let groupImage = MakeElement("artists-group-image", group)
    let groupImageLink = MakeElement("", groupImage, {href: `/group-question/${this.groupId}`}, "a")
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

    let groupNameLink = MakeElement("", groupName, {href: `/group-question/${this.groupId}`, innerText: this.name}, "a")

    let groupDescription = MakeElement("artists-group-description", groupData, {innerText: this.description})
    let groupStats = MakeElement("artists-group-stats", groupData, {innerHTML: GetWordForm(this.artistIds.length, ['исполнитель', 'исполнителя', 'исполнителей'])})

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
        MakeElement("info-description-line", info, {innerHTML: `<p><b>Исполнители:</b></p><ul>${artists}</ul>`})
    }

    this.metadata.BuildInfo(info)

    return info
}
