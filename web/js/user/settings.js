function UpdateMainSettings() {
    let data = {
        show_progress: document.getElementById("show-progress").checked,
        autoplay: document.getElementById("autoplay").checked
    }

    SendRequest("/settings_main", data).then(response => {
        if (response.status != SUCCESS_STATUS)
            ShowNotification(`<b>Ошибка</b>: не удалось обновить настройки<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
    })
}
