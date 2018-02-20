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
        drawCharistPosVsNegLast3Minutes(negative_tweets_count, neutral_tweets_count, positive_tweets_count, total_tweets);
        var listOfCalls = createArrayOfInts(calls_counter + 1);
        drawChartistPolarityLast3Minutes(listOfCalls, average_polarity_list);
        drawChartistTweetsPerIterationLast3Minutes(listOfCalls, tweets_per_pull_list);

        var time_labels = [
            '00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30',
            '06:00', '06:30', '07:00', '07:30',
            '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
            '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30',
            '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30', '23:59'];

        //Timeline tweets per whole day
        drawChartJsTweetsAllDay();

        //Timeline tweets per whole day
        drawChartJsAveragePolarityAll();

        // And for a doughnut chart
        drawChartJsDoughnutAll(negative_tweets_count, neutral_tweets_count, positive_tweets_count)


        drawChartJsTweetsPerPullAll(calls_counter, tweets_per_pull_list)


    }

}