function ShowTrackInfo(trackId) {
    for (let trackInfo of document.getElementsByClassName("track-info"))
        trackInfo.classList.remove("track-info-open")

    let trackInfoPopup = document.getElementById("track-info-popup")
    trackInfoPopup.classList.add('track-info-popup-open')

    let trackInfo = document.getElementById(`track-info-${trackId}`)
    trackInfo.classList.add('track-info-open')
    trackInfo.scrollTop = 0
}

function CloseTrackInfo() {
    let body = document.getElementsByTagName("body")[0]
    body.classList.remove("no-overflow")

    let trackInfoPopup = document.getElementById("track-info-popup")
    trackInfoPopup.classList.remove('track-info-popup-open')

    for (trackInfo of document.getElementsByClassName("track-info-open"))
        trackInfo.classList.remove('track-info-open')
}

function InitSwipeHandlers() {
    for (let block of document.getElementsByClassName("track-info")) {
        let handler = new SwipeHandler(block, CloseTrackInfo, SWIPE_HANDLER_DOWN)
    }
}
