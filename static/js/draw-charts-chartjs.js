var time_labels = [
    '00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30',
    '06:00', '06:30', '07:00', '07:30',
    '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
    '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30',
    '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30', '23:59'];

//Timeline tweets per whole day
function drawChartJsTweetsAllDay() {
    var ctx = document.getElementById('neg-neu-pos-timeline').getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'bar',

        // The data for our dataset
        data: {
            labels: time_labels,
            datasets: [
                {
                    label: 'Negative',
                    data: [67.8, 12, 11],
                    backgroundColor: '#f44336'
                },
                {
                    label: 'Neutral',
                    data: [20.7, 42, 23],
                    backgroundColor: '#ffeb3b'
                },
                {
                    label: 'Positive',
                    data: [11.4, 23, 41],
                    backgroundColor: '#4caf50'
                }
            ]
        },

        // Configuration options go here
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    stacked: true,
                    time: {
                        format: "HH:mm",
                        unit: 'hour',
                        unitStepSize: 1,
                        displayFormats: {
                            'minute': 'HH:mm',
                            'hour': 'HH:mm',
                            min: '00:00',
                            max: '23:30'
                        },
                    }
                }],
                yAxes: [{stacked: true}]
            },
        }
    });

}
//Timeline tweets per whole day
function drawChartJsAveragePolarityAll() {
    var ctx2 = document.getElementById('all-average-polarity-timeline').getContext('2d');
    var chart = new Chart(ctx2, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: time_labels,
            datasets: [
                {
                    label: 'Average Sentiment',
                    data: [0.5, -0.1],
                    backgroundColor: 'transparent',
                    borderColor: '#2196f3'
                },
            ]
        },

        // Configuration options go here
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        format: "HH:mm",
                        unit: 'hour',
                        unitStepSize: 0.5,
                        displayFormats: {
                            'minute': 'HH:mm',
                            'hour': 'HH:mm',
                            min: '00:00',
                            max: '23:30'
                        },
                    }
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
    var myDoughnutChart = new Chart(ctx3, {
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
        var labels = [];
        for (var i = 1; i <= calls_counter; i++) {
            labels.push(i);
        }
        var ctx4 = document.getElementById('all-tweets-per-pull').getContext('2d');
        ctx4.clearRect(0, 0, ctx4.width, ctx4.height);

        var myBarChart = new Chart(ctx4, {
            type: 'bar',
            data: {
                labels: labels,
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
                    }]
                }
            }
        });
    }
}