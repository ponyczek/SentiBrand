function setStatistics(tweets_no, locations_no) {
    $('.tweets-stat').text(tweets_no);
    $('.locations-stat').text(locations_no);
    $('.average-stat').text(countAverage());
}

function disableSearchBtn() {
    if ($('#query_phrase').val().length > 0) {
        $('#search-btn').prop("disabled", false);
    } else {
        $('#search-btn').prop("disabled", true);
    }
}


function setTopTweet(data, tag) {
    var path = " .most-tweet .timeline-panel .timeline-heading ";
    $(tag + path + ".timeline-title .polarity-stat").text(roundToTwoDecimal(data.polarity));
    $(tag + path + ".timeline-title .stat-author").text(data.user.name);
    $(tag + path + " .stat-pic").prop('src', data.user.profile_image_url_https);
    $(tag + path + " .stat-date").text(data.created_at);
    $(tag + " .most-tweet .timeline-panel .stat-content").text(data.text);
}

function sendMessage() {

    $('.statistics-holder').show();
    deadline = new Date(Date.parse(new Date()) + 10 * 1000);
    initializeClock('clockdiv', deadline);

    var input = $('#query_phrase');
    var newSearchBtn = $('#new_search_btn');
    var searchBtn = $('#search-btn');
    initializeClock('clockdiv', deadline);

    input.prop('disabled', 'disabled');
    searchBtn.prop('disabled', 'disabled');

    newSearchBtn.removeClass('btn-default');
    newSearchBtn.addClass('btn-primary');
    newSearchBtn.prop('disabled', false);

    clearInterval(getDataInterval);

    socket.send(JSON.stringify({
        text: input.val(),
        user_name: "{{ user.get_username}}"
    }));

    var getDataInterval = setInterval(function () {
        deadline = new Date(Date.parse(new Date()) + 10 * 1000);
        initializeClock('clockdiv', deadline);
        socket.send(JSON.stringify({
            text: input.val(),
            user_name: "{{ user.get_username}}",
            last_tweet_id: last_tweet_id
        }));
    }, 10000);
}

$('#query_phrase').on("keyup", disableSearchBtn);
$('#search-btn').click(sendMessage);
