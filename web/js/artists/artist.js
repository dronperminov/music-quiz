function ShowTrackNotification(trackId, correct, incorrect) {
    let title = document.getElementById(`track-${trackId}`).getElementsByClassName("track-title")[0].innerText.trim()
    let correctText = GetWordForm(correct, ['корректный', 'корректных', 'корректных'])
    let incorrectText = GetWordForm(incorrect, ['некорректный', 'некорректных', 'некорректных'])
    ShowNotification(`<b>${title}</b>: ${correctText} и ${incorrectText}`, 'info-notification', 3000)
}
