
function drawCharistPosVsNegLast3Minutes(negative_tweets_count, neutral_tweets_count, positive_tweets_count, total_tweets){
    new Chartist.Pie('.pos-vs-neg-chart-last3', {
        series: [last18records(negative_tweets_count), last18records(neutral_tweets_count), last18records(positive_tweets_count)]
    }, {
        donut: true,
        donutWidth: 60,
        donutSolid: true,
        startAngle: 270,
        total: total_tweets * 2,
        showLabel: true
    });
}
function drawChartistPolarityLast3Minutes(listOfCalls, average_polarity_list) {
    //last 3 minutes polarity
    new Chartist.Line('.polarity-per-pull-last3', {
        labels: last18records(listOfCalls),
        series: [last18records(average_polarity_list)]

    }, {
        low: -1,
        high: 1,
        fullWidth: true,
        chartPadding: {right: 40}
    });
}


        //how many tweets for each iteration
function drawChartistTweetsPerIterationLast3Minutes(listOfCalls, tweets_per_pull_list) {

    new Chartist.Line('.tweets-per-pull-last3', {
        labels: last18records(listOfCalls),
        series: [last18records(tweets_per_pull_list)]

    }, {
        fullWidth: true,
        chartPadding: {right: 40}
    });
}