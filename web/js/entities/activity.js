function Activity(data) {
    this.username = data.username
    this.fullname = data.full_name
    this.avatarUrl = data.avatar
    this.timestamp = ParseDateTime(data.timestamp)
    this.groupId = data.group_id
}

Activity.prototype.Build = function() {
    let activity = MakeElement("activity")

    let activityAvatar = MakeElement("activity-avatar", activity)
    let activityAvatarLink = MakeElement("", activityAvatar, {href: `/analytics?username=${this.username}`}, "a")
    let activityAvatarImg = MakeElement("", activityAvatarLink, {src: this.avatarUrl, loading: "lazy"}, "img")

    let activityInfo = MakeElement("activity-info", activity)
    let activityTimestamp = MakeElement("activity-timestamp", activityInfo, {innerText: `${this.timestamp.date} в ${this.timestamp.time}`})

    let link = `<a class="link" href="/analytics?username=${this.username}">@${this.username}</a>`
    let groupLink = this.groupId ? ` в <a class="link" href="artists-groups/${this.groupId}">группе</a>` : ""
    let activityAction = MakeElement("activity-action", activityInfo, {innerHTML: `${link} ответил на вопрос${groupLink}`})

    return activity
}
