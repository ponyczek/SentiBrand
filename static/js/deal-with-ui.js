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
    $(tag + path + " .stat-pic").prop('src', data.profile_image_url? data.profile_image_url : data.user.profile_image_url);
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

function getSearchIds(search_records, start, end) {
    var search_ids = [];
    search_records.forEach(function (search_record) {
        if ((search_record.created_at * 1000) >= start && (search_record.created_at * 1000) <= end) {
            search_ids.push(search_record.search_id);
        }
    });
    return search_ids;
}


$('#date-range-slider').on("slideStop", function (e) {
    var start = e.value[0];
    var end = e.value[1];
    search_ids = getSearchIds(search_records, start, end);
    $('.statistics-holder').show();
    $.ajax({
        url: window.location.href + 'analysis',
        type: 'GET',
        data: {search_ids: JSON.stringify(search_ids)},
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            processSavedTweets(response.tweets);
            $('#dates-header').text('Data collected between: \n' +
                moment(e.value[0]).format("DD/MM/YYYY HH:mm") + " and " +
                moment(e.value[1]).format("DD/MM/YYYY HH:mm"));
        },
        error: function () {
            alert("error");
        }
    });
});

$(function () {
    $("#datepicker").datepicker({
        autoclose: true,
    }).datepicker('setDate', new Date()).datepicker().on("changeDate", function (e) {
        //call to api;
        var sel_day_start = Date.parse(e.date);
        var end_of_day = 86400000 - 1;
        var sel_day_end = sel_day_start + end_of_day;
        var search_ids_for_query = getSearchIds(search_records, sel_day_start, sel_day_end);

        $.ajax({
            url: window.location.href + 'analysis',
            type: 'GET',
            data: {search_ids: JSON.stringify(search_ids_for_query)},
            contentType: 'application/json; charset=utf-8',
            success: function (response) {
                if (response.tweets.length) {
                    $('.statistics-holder').show();
                    processSavedTweets(response.tweets);
                    $('#dates-header').text('Showing data collected on ' +
                        moment(e.date).format("DD/MM/YYYY"));
                }
                else {
                    $('#myModal').modal('show');
                }
            },
            error: function () {
                alert("error");
            }
        });
    });
});


