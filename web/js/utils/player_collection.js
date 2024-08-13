function PlayerCollection() {
    this.players = []
}

PlayerCollection.prototype.Add = function(trackId, audio, play = true) {
    let player = new Player(`player-${trackId}`, audio)
    this.players.push(player)

    if (play)
        player.Play()
}

PlayerCollection.prototype.Pause = function(audio) {
    for (let player of this.players)
        if (player.audio !== audio)
            player.Pause()
}
