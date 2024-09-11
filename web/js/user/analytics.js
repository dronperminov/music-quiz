const key2color = {
    total: "#2f7bf0",
    correct: "#47b39c",
    incorrect: "#ec6b56",
    unknown: "#ffc154",

    questions: "#d82e6b",
    time: "#d82e6b"
}

function ToggleQuestionsChart() {
    if (Math.max(...questionsData.map(data => data.value)) == 0)
        return

    let chartBlock = document.getElementById("questions-chart-block")
    chartBlock.classList.toggle("analytics-chart-open")

    if (chartBlock.classList.contains("analytics-chart-open"))
        ShowQuestionsChart()
}

function ShowQuestionsChart() {
    if (Math.max(...questionsData.map(data => data.value)) == 0)
        return

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
    if (timesData.total.reduce((sum, value) => sum + value.count, 0) == 0)
        return

    let block = document.getElementById("times-chart-block")
    block.classList.toggle("analytics-chart-open")

    for (let key of ["total", "correct", "incorrect"]) {
        let label = document.getElementById(`times-${key}-label`)
        label.classList.remove("analytics-label-selected")
    }

    if (block.classList.contains("analytics-chart-open"))
        ShowTimesChart("total")
}

function ShowTimesChart(targetKey = null) {
    if (timesData.total.reduce((sum, value) => sum + value.count, 0) == 0)
        return

    let chartBlock = document.getElementById("times-chart-block")
    chartBlock.classList.add("analytics-chart-open")

    let oneScale = document.getElementById("times-scale").checked
    let maxTime = 0

    for (let key of ["total", "correct", "incorrect"]) {
        maxTime = Math.max(maxTime, ...timesData[key].map(data => data.count))

        if (targetKey === null && !document.getElementById(`times-${key}-chart`).classList.contains("hidden"))
            targetKey = key
    }

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
        chart.Plot(svg, timesData[key], "label", "count", oneScale ? maxTime : null)
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

function PlotPeriodBarChart(key, maxValue = null) {
    let svg = document.getElementById(`period-${key}-chart`)

    if (svg === null)
        return

    let chart = new BarChart({barColor: key2color[key], minRectWidth: 32, maxRectWidth: 38, bottomPadding: 25})
    chart.Plot(svg, periodData, "label", key, maxValue)
}

function PlotPeriodPlotChart(key) {
    let svg = document.getElementById(`period-${key}-chart`)

    if (svg === null)
        return

    let chart = new PlotChart({markerColor: key2color[key]})
    chart.Plot(svg, periodData, "label", key)
}

function TogglePeriodChart(key) {
    let block = document.getElementById(`period-${key}-block`)
    block.classList.toggle("analytics-chart-open")
}

function ToggleYearsChart() {
    if (yearsData.total.reduce((sum, value) => sum + value.count, 0) == 0)
        return

    let block = document.getElementById("years-chart-block")
    block.classList.toggle("analytics-chart-open")

    for (let key of ["total", "correct", "incorrect"]) {
        let label = document.getElementById(`years-${key}-label`)
        label.classList.remove("analytics-label-selected")
    }

    if (block.classList.contains("analytics-chart-open"))
        ShowYearsChart("total")
}

function ShowYearsChart(targetKey = null) {
    if (yearsData.total.reduce((sum, value) => sum + value.count, 0) == 0)
        return

    let chartBlock = document.getElementById("years-chart-block")
    chartBlock.classList.add("analytics-chart-open")

    let percentsBlock = document.getElementById("years-percents-block")
    percentsBlock.classList.add("hidden")

    for (let key of ["total", "correct", "incorrect"])
        if (targetKey === null && !document.getElementById(`years-${key}-chart`).classList.contains("hidden"))
            targetKey = key

    if (targetKey != "total")
        percentsBlock.classList.remove("hidden")

    let percents = document.getElementById("years-percents").checked

    if (percents) {
        yearsData.correctPercents = []
        yearsData.incorrectPercents = []

        for (let i = 0; i < yearsData.total.length; i++) {
            yearsData.correctPercents.push({label: yearsData.total[i].label, count: Math.round(yearsData.correct[i].count / Math.max(yearsData.total[i].count, 1) * 1000) / 10})
            yearsData.incorrectPercents.push({label: yearsData.total[i].label, count: Math.round(yearsData.incorrect[i].count / Math.max(yearsData.total[i].count, 1) * 1000) / 10})
        }
    }

    for (let key of ["total", "correct", "incorrect"]) {
        let svg = document.getElementById(`years-${key}-chart`)
        let label = document.getElementById(`years-${key}-label`)

        if (key != targetKey) {
            svg.classList.add("hidden")
            label.classList.remove("analytics-label-selected")
            continue
        }

        svg.classList.remove("hidden")
        label.classList.add("analytics-label-selected")

        let chart = new BarChart({barColor: key2color[key], minRectWidth: 48, maxRectWidth: 55, bottomPadding: 10, labelSize: 9})
        if (percents && key != "total")
            key += "Percents"

        chart.Plot(svg, yearsData[key], "label", "count")
    }

    let block = document.getElementById("years-block")
    block.scrollIntoView({behavior: "smooth"})
}
