function GetActivityParams() {
    return {}
}

function LoadActivity(response, block) {
    for (let activity of response.activity) {
        let user = response.username2user[activity.username]
        activity.avatar = user.avatar_url
        activity.full_name = user.full_name

        activity = new Activity(activity)
        block.appendChild(activity.Build())
    }

    return response.activity.length
}
