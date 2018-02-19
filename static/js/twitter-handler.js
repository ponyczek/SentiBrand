var total_tweets = null;
var total_locations = null;
var highest_polarity = -2;
var lowest_polarity = 2;
var polarity_sum = 0;
var most_positive_tweet = {};
var most_negative_tweet = {};
var positive_tweets_count = 0;
var neutral_tweets_count = 0;
var negative_tweets_count = 0;

var average_polarity_list = [];
var tweets_per_pull_list = []; //list that contains number of tweets that came back from api
var negative_count_list = [];
var neutral_count_list = [];
var positive_count_list = [];


var calls_counter = 0;
var last_tweet_id;

function processTweets(event) {
    var data = JSON.parse(event.data);
    if (data) {
        if (data[0] && last_tweet_id !== data[0].id) {
            last_tweet_id = data[0].id;
            var positive_per_call = 0;
            var neutral_per_call = 0;
            var negative_per_call = 0;
            data.forEach(function (tweet) {
                total_tweets++;
                //console.log(tweet.user.name);
                var user = tweet.user;
                var username = user.name;
                var user_location = user.location;
                var content = tweet.text;
                var coordinates = tweet.geolocation;
                var place = tweet.place;
                var date = moment(new Date(tweet.created_at)).format('MMMM Do YYYY, h:mm:ss a');
                var polarity = tweet.polarity;
                var color = getColor(polarity);
                polarity_sum += polarity;

                if (polarity > 0) {
                    positive_tweets_count++;
                    positive_per_call++;
                } else if (polarity < 0) {
                    negative_tweets_count++;
                    negative_per_call++;
                } else {
                    neutral_tweets_count++;
                    neutral_per_call++;
                }

                if (polarity >= highest_polarity) {
                    most_positive_tweet = tweet;
                    highest_polarity = polarity;
                }

                if (polarity <= lowest_polarity) {
                    most_negative_tweet = tweet;
                    lowest_polarity = polarity;
                }


                //should be negative left positive right ?
                var inverted = polarity >= 0 ? "timeline-inverted" : "";
                if (coordinates || place) {
                    var lat, lng;
                    lat = coordinates ? coordinates.coordinates[0] : place.bounding_box.coordinates[0][0][1];
                    lng = coordinates ? coordinates.coordinates[1] : place.bounding_box.coordinates[0][0][0];
                    points.push(new google.maps.LatLng(lat, lng));
                    heatmap.setMap(map);
                    total_locations++;
                }

                "<div class='col-sm-2'><img src='" + user.profile_image_url_https + "'alt='Thumbnail Image' class='rounded-circle img-raised'> </div>"

                $(".timeline").append(
                    '<li class =' + inverted + '> <div class=\"timeline-badge\" style=\"color:gray; background-color: ' + color + ';\"><i class=\"glyphicon glyphicon-check\">'
                    + roundToTwoDecimal(polarity) + '</i></div> <div class=\"timeline-panel\"> ' +
                    '<div class=\"timeline-heading\"><h4 class=\"timeline-title\">' +
                    '<img src=\"' + user.profile_image_url_https + '\"alt=\"Thumbnail Image\" class=\"rounded-circle img-raised timeline-user-pic\">' +
                    '<span class =\"title-username\">' + username + '</span></h4>' +
                    '<p> <small class=\"text-muted\"><i class=\"glyphicon glyphicon-time\">' +
                    '</i>' +
                    (user_location ? 'Assigned user location: ' + user_location + ',  ' : '') + date + " " + '</small> </p> </div> <div class=\"timeline-body\"> ' +
                    '<p>' + content +
                    '</p> ' +
                    '</div> ' +
                    '</div> ' +
                    '</li>'
                );

                setStatistics(total_tweets, total_locations);
                setTopTweet(most_positive_tweet, ".positive-tweet");
                setTopTweet(most_negative_tweet, ".negative-tweet");

            });
            calls_counter++;
            positive_count_list.push(positive_per_call);
            neutral_count_list.push(neutral_per_call);
            negative_count_list.push(negative_per_call);
            tweets_per_pull_list.push(positive_per_call + neutral_per_call + negative_per_call);
            average_polarity_list.push(countAverage());
        }


        //last 3 minutes

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


        var listOfCalls = createArrayOfInts(calls_counter + 1);

        //how polarity
        new Chartist.Line('.polarity-per-pull-last3', {
            labels: last18records(listOfCalls),
            series: [last18records(average_polarity_list)]

        }, {
            low: -1,
            high: 1,
            fullWidth: true,
            chartPadding: {right: 40}
        });

        //how many tweets for each iteration
        new Chartist.Line('.tweets-per-pull-last3', {
            labels: last18records(listOfCalls),
            series: [last18records(tweets_per_pull_list)]

        }, {
            fullWidth: true,
            chartPadding: {right: 40}
        });

        new Chartist.Line('.count-over-time-last3', {
            labels: last18records(listOfCalls),
            series: [
                last18records(negative_count_list),
                last18records(neutral_count_list),
                last18records(positive_count_list)
            ]
        }, {
            fullWidth: true,
            chartPadding: {
                right: 40
            }
        });


        var time_labels = [
            '00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30',
            '06:00', '06:30', '07:00', '07:30',
            '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
            '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30',
            '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30', '23:59'];

        //Timeline tweets per whole day
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

        //Timeline tweets per whole day
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

}