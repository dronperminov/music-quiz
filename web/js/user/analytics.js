const key2color = {
    total: "#2f7bf0",
    correct: "#47b39c",
    incorrect: "#ec6b56",
    unknown: "#ffc154"
}

function ToggleQuestionsChart() {
    let chartBlock = document.getElementById("questions-chart-block")
    chartBlock.classList.toggle("analytics-chart-open")

    if (chartBlock.classList.contains("analytics-chart-open"))
        ShowQuestionsChart()
}

function ShowQuestionsChart() {
    let chartBlock = document.getElementById("questions-chart-block")
    chartBlock.classList.add("analytics-chart-open")

    let svg = document.getElementById("questions-chart")
    let chart = new Chart()
    chart.Plot(svg, questionsData)

    let block = document.getElementById("questions-block")
    block.scrollIntoView({behavior: "smooth"})
}

function ToggleTotalTimeChart() {
    let block = document.getElementById("total-time-block")
    block.classList.toggle("analytics-chart-open")

    let smallBar = document.getElementById("total-time-small-bar")
    smallBar.classList.toggle("analytics-bar-small")
}

function ToggleTimesChart() {
    let block = document.getElementById("times-chart-block")
    block.classList.toggle("analytics-chart-open")

    for (let key of ["total", "correct", "incorrect"]) {
        let label = document.getElementById(`times-${key}-label`)
        label.classList.remove("analytics-label-selected")
    }

    if (block.classList.contains("analytics-chart-open"))
        ShowTimesChart("total")
}

function ShowTimesChart(targetKey) {
    let chartBlock = document.getElementById("times-chart-block")
    chartBlock.classList.add("analytics-chart-open")

    for (let key of ["total", "correct", "incorrect"]) {
        let svg = document.getElementById(`times-${key}-chart`)
        let label = document.getElementById(`times-${key}-label`)

        if (key != targetKey) {
            svg.classList.add("hidden")
            label.classList.remove("analytics-label-selected")
            continue
        }

        svg.classList.remove("hidden")
        label.classList.add("analytics-label-selected")

        let chart = new BarChart({barColor: key2color[key], minRectWidth: 32, maxRectWidth: 45, bottomPadding: 12})
        chart.Plot(svg, timesData[key], "label", "count")
    }

    let block = document.getElementById("times-block")
    block.scrollIntoView({behavior: "smooth"})
}

function ToggleTable(blockId) {
    let table = document.getElementById(`${blockId}-table`)

    if (table === null)
        return

    table.classList.toggle("hidden")

    if (!table.classList.contains("hidden")) {
        let block = document.getElementById(`${blockId}-block`)
        block.scrollIntoView({behavior: "smooth"})
    }
}

function PlotGenresChart() {
    let svg = document.getElementById("genres-chart")

    if (svg === null)
        return

    let radar = new RadarChart({labelSize: 10})
    radar.Plot(svg, genresData)
}
