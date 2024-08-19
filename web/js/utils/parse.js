function ParseArtist(button, artistId) {
    button.setAttribute("disabled", "")

    SendRequest("/parse-artist", {artist_id: artistId}).then(response => {
        button.removeAttribute("disabled")

        if (response.status != SUCCESS_STATUS)
            ShowNotification(`Не удалось распарсить исполнителя<br>${response.message}`, "error-notification")
        else
            ShowNotification(`Исполнитель успешно обновлён.<ul><li>треки: ${response.tracks}</li><li>исполнители: ${response.artists}</li></ul>`, "success-notification")
    })
}
