function PlotQuestionsChart() {
    let svg = document.getElementById("questions-chart")
    let chart = new Chart()
    chart.Plot(svg, questionsData)
}

function ToggleChart(blockId) {
    let block = document.getElementById(blockId)
    block.classList.toggle("analytics-chart-open")
}

function ShowTimesChart(targetKey) {
    for (let key of ["total", "correct", "incorrect"]) {
        let svg = document.getElementById(`times-${key}-chart`)

        if (key != targetKey) {
            svg.classList.add("hidden")
            continue
        }

        svg.classList.remove("hidden")
        let chart = new BarChart({barColor: key2color[key], minRectWidth: 32, maxRectWidth: 45, bottomPadding: 12})
        chart.Plot(svg, timesData[key], "label", "count")
    }
}

function ToggleTable(blockId) {
    let block = document.getElementById(blockId)
    block.classList.toggle("hidden")

    if (!block.classList.contains("hidden"))
        block.scrollIntoView({behavior: "smooth"})
}
