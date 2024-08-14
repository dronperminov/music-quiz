function Search(blockId = "search", onSearch, onClear) {
    this.block = document.getElementById(blockId)
    this.onSearch = onSearch
    this.onClear = onClear

    this.clear = this.block.getElementsByClassName("search-clear")[0]
    this.clear.addEventListener("click", () => this.ClearQuery())

    this.query = this.block.getElementsByClassName("search-query")[0]
    this.queryInput = this.query.children[0]
    this.queryInput.addEventListener("keydown", (e) => this.QueryKeyDown(e))
    this.queryInput.addEventListener("input", (e) => this.QueryInput(e))
    this.queryInput.addEventListener("focus", (e) => this.QueryFocus())
    this.queryInput.addEventListener("focusout", (e) => this.QueryFocusOut())

    this.filters = this.block.getElementsByClassName("search-filters")[0]
    this.filters.addEventListener("click", (e) => this.ToggleFiltersPopup())
    this.filtersPopup = this.block.getElementsByClassName("search-filters-popup")[0]
}

Search.prototype.GetQuery = function() {
    return this.queryInput.value.trim()
}

Search.prototype.ClearQuery = function() {
    this.queryInput.value = ""
    this.block.classList.add("search-query-empty")
    this.onClear()
}

Search.prototype.QueryKeyDown = function(e) {
    if (e.key != "Enter")
        return

    e.preventDefault()
    this.block.classList.remove("search-focus")
    this.queryInput.blur()

    this.onSearch()
}

Search.prototype.QueryInput = function(e) {
    let query = this.GetQuery()

    if (query.length == 0) {
        this.block.classList.add("search-query-empty")
    }
    else {
        this.block.classList.remove("search-query-empty")
    }
}

Search.prototype.QueryFocus = function() {
    this.block.classList.add("search-focus")
    this.filtersPopup.classList.remove("search-filters-popup-open")
    this.filters.classList.remove("search-filters-open")
}

Search.prototype.QueryFocusOut = function() {
    this.block.classList.remove("search-focus")
}

Search.prototype.ToggleFiltersPopup = function() {
    console.log("!")
    this.filtersPopup.classList.toggle("search-filters-popup-open")
    this.filters.classList.toggle("search-filters-open")
}
