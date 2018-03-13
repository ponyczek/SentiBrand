var all_neg_neu_pos_labels = [];
var all_date_labels = [];

function createLabelForNegNeuPosAll(calls_counter, negative_per_call, neutral_per_call, positive_per_call, date) {
    if (calls_counter > 0) {
        var d = date ? date : new Date();
        var pull_date = moment(d).format('MMMM Do YYYY, h:mm:ss a');
        var pull_tweets_total = negative_per_call + neutral_per_call + positive_per_call;
        var total_str = "Pulled " + pull_tweets_total + " tweets at " + pull_date;
        all_neg_neu_pos_labels.push(total_str);
    }
}

function createLabelsWithDate(calls_counter) {
    if (calls_counter > 0) {
        var pull_date = moment(new Date()).format('MMMM Do YYYY, h:mm:ss a');
        var total_str = "Result taken from: " + pull_date;
        all_date_labels.push(total_str);
    }
}

function createLabelsWithHistoricDates(calls_counter, date) {
    if (calls_counter > 0) {
        var pull_date = moment(date).format('MMMM Do YYYY, h:mm:ss a');
        var total_str = "Result taken from: " + pull_date;
        all_date_labels.push(total_str);
    }
}

//Timeline tweets per whole day
function drawChartJsTweetsAllDay(all_neg_neu_pos_labels, negative_count_list, neutral_count_list, positive_count_list) {
    var ctx = document.getElementById('neg-neu-pos-timeline').getContext('2d');
    if (window.chart && window.chart !== null) {
        window.chart.destroy();
    }
    window.chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'bar',

        // The data for our dataset
        data: {
            labels: all_neg_neu_pos_labels,
            datasets: [
                {
                    label: 'Negative',
                    data: negative_count_list,
                    backgroundColor: '#f44336'
                },
                {
                    label: 'Neutral',
                    data: neutral_count_list,
                    backgroundColor: '#ffeb3b'
                },
                {
                    label: 'Positive',
                    data: positive_count_list,
                    backgroundColor: '#4caf50'
                }
            ]
        },

        // Configuration options go here
        options: {
            animation: {
                duration: 0
            },
            scales: {
                xAxes: [{
                    display: false,
                    stacked: true,

                }],
                yAxes: [{
                    stacked: true,
                    ticks: {
                        max: 100,
                        min: 0
                    }
                }]
            },
        },
    });

}

//Timeline tweets per whole day
function drawChartJsAveragePolarityAll(average_polarity_list) {
    var ctx2 = document.getElementById('all-average-polarity-timeline').getContext('2d');
    if (window.averageListChart && window.averageListChart !== null) {
        window.averageListChart.destroy();
    }
    window.averageListChart = new Chart(ctx2, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: all_date_labels,
            datasets: [
                {
                    label: 'Average Sentiment',
                    data: average_polarity_list,
                    backgroundColor: 'transparent',
                    borderColor: '#2196f3'
                },
            ]
        },

        // Configuration options go here
        options: {
            scales: {
                xAxes: [{
                    display: false,
                }],
                yAxes: [{
                    ticks: {
                        max: 1,
                        min: -1
                    }
                }]

            },
        }
    });
}

function drawChartJsAveragePolarityPosNeg(average_polarity_list_pos_neg) {
    var averagePosNegChart = document.getElementById('posneg-average-polarity-timeline').getContext('2d');
    if (window.averageListChartPosNeg && window.averageListChartPosNeg !== null) {
        window.averageListChartPosNeg.destroy();
    }
    window.averageListChartPosNeg = new Chart(averagePosNegChart, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: all_date_labels,
            datasets: [
                {
                    label: 'Average Sentiment Excl. Neutral',
                    data: average_polarity_list_pos_neg,
                    backgroundColor: 'transparent',
                    borderColor: '#2196f3'
                },
            ]
        },

        // Configuration options go here
        options: {
            scales: {
                xAxes: [{
                    display: false,
                }],
                yAxes: [{
                    ticks: {
                        max: 1,
                        min: -1
                    }
                }]

            },
        }
    });
}

function drawChartJsDoughnutAll(negative_tweets_count, neutral_tweets_count, positive_tweets_count) {
// And for a doughnut chart
    var ctx3 = document.getElementById('all-neg-neu-pos').getContext('2d');
    if (window.myDoughnutChart && window.myDoughnutChart !== null) {
        window.myDoughnutChart.destroy();
    }
    window.myDoughnutChart = new Chart(ctx3, {
        type: 'doughnut',
        data: {
            labels: [
                "Negative",
                "Neutral",
                "Positive",
            ],
            datasets: [
                {
                    data: [negative_tweets_count, neutral_tweets_count, positive_tweets_count],
                    backgroundColor: [
                        "#f44336",
                        "#ffeb3b",
                        "#4caf50",
                    ],
                    borderColor: '#888',

                }]
        },
        options: {}
    });
}

function drawChartJsTweetsPerPullAll(calls_counter, tweets_per_pull_list) {

    if (calls_counter > 0) {

        var ctx4 = document.getElementById('all-tweets-per-pull').getContext('2d');
        ctx4.clearRect(0, 0, ctx4.width, ctx4.height);
        if (window.tweetsPerPullChart && window.tweetsPerPullChart !== null) {
            window.tweetsPerPullChart.destroy();
        }
        window.tweetsPerPullChart = new Chart(ctx4, {
            type: 'bar',
            data: {
                labels: all_date_labels,
                datasets: [
                    {
                        label: "Number of tweets per pull",
                        backgroundColor: '#2196f3',
                        borderColor: '#2196f3',
                        data: tweets_per_pull_list
                    }
                ]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            max: 100,
                            beginAtZero: true,
                        }
                    }],
                    xAxes:[ {
                        display: false,
                    }]
                }
            }
        });
    }
}