function PlayerCollection() {
    this.players = []
}

PlayerCollection.prototype.Add = function(trackId, audio) {
    let player = new Player(trackId, audio)
    this.players.push(player)
    return player
}

PlayerCollection.prototype.Pause = function(audio) {
    for (let player of this.players)
        if (player.audio !== audio)
            player.Pause()
}

PlayerCollection.prototype.GetPlayer = function() {
    if (this.players.length == 0)
        return null

    return this.players[this.players.length - 1]
}
