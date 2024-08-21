function Genre(value) {
    this.value = value
}

Genre.prototype.ToRus = function() {
    return {
        "rock": "рок",
        "hip-hop": "хип-хоп",
        "pop": "поп",
        "electro": "электронная",
        "disco": "диско",
        "jazz-soul": "джаз / соул"
    }[this.value]
}
