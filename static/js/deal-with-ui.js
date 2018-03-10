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

    var input = $('#query_phrase');
    var newSearchBtn = $('#new_search_btn');
    var selectComponent = $('#intervalSelect');
    var intervalValue = Number(selectComponent.val());
    var searchBtn = $('#search-btn');
    deadline = new Date(Date.parse(new Date()) + intervalValue);
    var pullText = $('#pullInterval');
    pullText.text(selectComponent.find(":selected").text());
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
        deadline = new Date(Date.parse(new Date()) + intervalValue);
        initializeClock('clockdiv', deadline);
        socket.send(JSON.stringify({
            text: input.val(),
            user_name: "{{ user.get_username}}",
            last_tweet_id: last_tweet_id
        }));
    }, intervalValue);
    selectComponent.prop('disabled', true);
}



$('#query_phrase').on("keyup", disableSearchBtn);
$('#search-btn').click(sendMessage);


console.log($('#date-range-slider'));
// $('#date-range-slider').on('slidestop', onScrollChange);
$('#date-range-slider').on("ondragleave", function (e, ui) {
onScrollChange();
});

function onScrollChange(event, bla){
    console.log('changed');
}