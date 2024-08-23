function Metadata(metadata, createText, updateText) {
    this.createdAt = metadata.created_at
    this.createdBy = metadata.created_by
    this.updatedAt = metadata.updated_at
    this.updatedBy = metadata.updated_by
    this.createText = createText
    this.updateText = updateText
}

Metadata.prototype.BuildInfo = function(parent) {
    let created = ParseDateTime(this.createdAt)
    MakeElement("info-line", parent, {innerHTML: `<b>${this.createText}:</b> ${created.date} в ${created.time} пользователем @${this.createdBy}`})

    if (this.createdAt == this.updatedAt)
        return

    let updated = ParseDateTime(this.updatedAt)
    MakeElement("info-line", parent, {innerHTML: `<b>Обновлён:</b> ${updated.date} в ${updated.time} пользователем @${this.updatedBy}`})
}
