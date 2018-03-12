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
var average_polarity_list_pos_neg = [];
var tweets_per_pull_list = []; //list that contains number of tweets that came back from api
var negative_count_list = [];
var neutral_count_list = [];
var positive_count_list = [];


var calls_counter = 0;
var last_tweet_id;

function processTweets(data, single_search) {
    if (data) {
        if (data[0] && last_tweet_id !== data[0].id) {
            last_tweet_id = data[0].id;
            var positive_per_call = 0;
            var neutral_per_call = 0;
            var negative_per_call = 0;
            data.forEach(function (tweet) {
                total_tweets++;
                var user = tweet.user;
                var username = single_search ? user.name : tweet.username;
                var user_location = user.location;
                var content = tweet.text;
                var lat = tweet.lat;
                var lng = tweet.lng;
                var date = moment(new Date(tweet.created_at)).format('MMMM Do YYYY, h:mm:ss a');
                var polarity = tweet.polarity;
                var color = getColor(polarity);
                var user_profile_image = single_search ? user.profile_image_url_https : tweet.profile_image_url;
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
                if (lat && lng) {
                    // var lat, lng;
                    // lat = coordinates ? coordinates.coordinates[0] : place.bounding_box.coordinates[0][0][1];
                    // lng = coordinates ? coordinates.coordinates[1] : place.bounding_box.coordinates[0][0][0];
                    points.push(new google.maps.LatLng(lat, lng));
                    heatmap.setMap(map);
                    total_locations++;
                }

                appendToTimeline(inverted, color, polarity, user_profile_image, username, user_location, date, content);
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
            //might not be necessary.
            average_polarity_list_pos_neg.push((polarity_sum / (positive_tweets_count + negative_tweets_count)).toFixed(3));
            $('.average-stat-posneg').text((polarity_sum / (positive_tweets_count + negative_tweets_count)).toFixed(3));
            createLabelForNegNeuPosAll(calls_counter, negative_per_call, neutral_per_call, positive_per_call);
            createLabelsWithDate(calls_counter);
        }

        //last 3 minutes
        drawCharistPosVsNegLast3Minutes(negative_tweets_count, neutral_tweets_count, positive_tweets_count, total_tweets);
        var listOfCalls = createArrayOfInts(calls_counter + 1);
        drawChartistPolarityLast3Minutes(listOfCalls, average_polarity_list);
        drawChartistTweetsPerIterationLast3Minutes(listOfCalls, tweets_per_pull_list);
        //Timeline tweets per whole day
        drawChartJsTweetsAllDay(all_neg_neu_pos_labels, negative_count_list, neutral_count_list, positive_count_list);
        //Timeline tweets per whole day
        drawChartJsAveragePolarityAll(average_polarity_list);
        //Excluding neutral
        drawChartJsAveragePolarityPosNeg(average_polarity_list_pos_neg);
        // And for a doughnut chart
        drawChartJsDoughnutAll(negative_tweets_count, neutral_tweets_count, positive_tweets_count)
        drawChartJsTweetsPerPullAll(calls_counter, tweets_per_pull_list)
    }
}

function processSavedTweets(data) {
    if (data) {
        //save search id iterate till it changes

        //split data into sub arrays each array split by search id

        var current_search_id = data[0].search_id;

        var positive_per_call = 0;
        var neutral_per_call = 0;
        var negative_per_call = 0;
        data.forEach(function (tweet) {
            total_tweets++;
            var user = tweet.user;
            var username = tweet.username;
            // var user_location = user.location;
            var content = tweet.text;
            var lat = tweet.lat;
            var lng = tweet.lng;
            var date = moment(new Date(tweet.created_at)).format('MMMM Do YYYY, h:mm:ss a');
            var polarity = tweet.polarity;
            var color = getColor(polarity);
            var user_profile_image = tweet.profile_image_url;
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
            if (lat && lng) {
                points.push(new google.maps.LatLng(lat, lng));
                heatmap.setMap(map);
                total_locations++;
            }

            appendToTimeline(inverted, color, polarity, user_profile_image, username, "", date, content);
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
        //might not be necessary.
        average_polarity_list_pos_neg.push((polarity_sum / (positive_tweets_count + negative_tweets_count)).toFixed(3));
        $('.average-stat-posneg').text((polarity_sum / (positive_tweets_count + negative_tweets_count)).toFixed(3));
        createLabelForNegNeuPosAll(calls_counter, negative_per_call, neutral_per_call, positive_per_call);
        createLabelsWithDate(calls_counter);
    }

    //last 3 minutes
    drawCharistPosVsNegLast3Minutes(negative_tweets_count, neutral_tweets_count, positive_tweets_count, total_tweets);
    var listOfCalls = createArrayOfInts(calls_counter + 1);
    drawChartistPolarityLast3Minutes(listOfCalls, average_polarity_list);
    drawChartistTweetsPerIterationLast3Minutes(listOfCalls, tweets_per_pull_list);
    //Timeline tweets per whole day
    drawChartJsTweetsAllDay(all_neg_neu_pos_labels, negative_count_list, neutral_count_list, positive_count_list);
    //Timeline tweets per whole day
    drawChartJsAveragePolarityAll(average_polarity_list);
    //Excluding neutral
    drawChartJsAveragePolarityPosNeg(average_polarity_list_pos_neg);
    // And for a doughnut chart
    drawChartJsDoughnutAll(negative_tweets_count, neutral_tweets_count, positive_tweets_count)
    drawChartJsTweetsPerPullAll(calls_counter, tweets_per_pull_list)

}

function appendToTimeline(inverted, color, polarity, user_profile_image, username, user_location, date, content) {
    $(".timeline").append(
        '<li class =' + inverted + '> <div class=\"timeline-badge\" style=\"color:gray; background-color: ' + color + ';\"><i class=\"glyphicon glyphicon-check\">'
        + roundToTwoDecimal(polarity) + '</i></div> <div class=\"timeline-panel\"> ' +
        '<div class=\"timeline-heading\"><h4 class=\"timeline-title\">' +
        '<img src=\"' + user_profile_image + '\"alt=\"Thumbnail Image\" class=\"rounded-circle img-raised timeline-user-pic\">' +
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
}