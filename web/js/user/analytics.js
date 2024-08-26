function PlotQuestionsChart() {
    let svg = document.getElementById("questions-chart")
    let chart = new Chart()
    chart.Plot(svg, questionsData)
}

function ToggleChart(blockId) {
    let block = document.getElementById(blockId)
    block.classList.toggle("analytics-chart-open")
}

function ShowChart(blockId) {
    let block = document.getElementById(blockId)
    block.classList.add("analytics-chart-open")
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
    let block = document.getElementById(blockId)

    if (block === null)
        return

    block.classList.toggle("hidden")

    if (!block.classList.contains("hidden"))
        block.scrollIntoView({behavior: "smooth"})
}

function PlotGenresChart() {
    let svg = document.getElementById("genres-chart")
    let radar = new RadarChart({labelSize: 10})
    radar.Plot(svg, genresData)
}
