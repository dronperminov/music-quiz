function ToggleTracksChart() {
    let chartBlock = document.getElementById("tracks-chart-block")
    chartBlock.classList.toggle("analytics-chart-open")

    if (chartBlock.classList.contains("analytics-chart-open"))
        ShowTracksChart()
}

function ShowTracksChart() {
    let chartBlock = document.getElementById("tracks-chart-block")
    chartBlock.classList.add("analytics-chart-open")

    let svg = document.getElementById("tracks-chart")
    let chart = new Chart()
    chart.Plot(svg, tracksData)

    let block = document.getElementById("tracks-block")
    block.scrollIntoView({behavior: "smooth"})
}
