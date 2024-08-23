function ArtistsGroup(data) {
    this.groupId = data.group_id
    this.name = data.name
    this.description = data.description
    this.artistIds = data.artist_ids
    this.imageUrl = data.image_url
    this.metadata = new Metadata(data.metadata, "Создана", "Обновлена")
}

ArtistsGroup.prototype.Build = function() {
    let group = MakeElement("artists-group")
    let groupImage = MakeElement("artists-group-image", group)
    let groupImageLink = MakeElement("", groupImage, {href: `/artists-groups/${this.groupId}`}, "a")
    let groupImageImg = MakeElement("", groupImageLink, {src: this.imageUrl, loading: "lazy"}, "img")

    let groupData = MakeElement("artists-group-data", group)
    let groupName = MakeElement("artists-group-name", groupData)
    let groupNameLink = MakeElement("", groupName, {href: `/artists-groups/${this.groupId}`, innerText: this.name}, "a")

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
