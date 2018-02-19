//Get appropriate color for the polarity
var colours = [
    "#FF0000",
    "#FF1100",
    "#FF3400",
    "#FF4600",
    "#FF6900",
    "#FF7B00",
    "#FF9E00",
    "#FFAF00",
    "#FFD300",
    "#FFE400",
    "#F7FF00",
    "#FFFF00",
    "#E5FF00",
    "#C2FF00",
    "#B0FF00",
    "#8DFF00",
    "#7CFF00",
    "#58FF00",
    "#47FF00",
    "#24FF00",
    "#12FF00",
];

function getColor(polarity) {
    var roundedVal = Math.round(polarity * 10);
    var positionOfYellow = 10;
    if (roundedVal === 0) {
        return colours[positionOfYellow];
    }
    else if (roundedVal < 0) {
        return colours[positionOfYellow + (roundedVal)];
    }
    else {
        return colours[positionOfYellow + roundedVal];
    }
}

function roundToTwoDecimal(polarity) {
    return Math.round(polarity * 100) / 100;
}

function countAverage() {
    return (polarity_sum / total_tweets).toFixed(2);
}

function createArrayOfInts(howMany, step) {
    var arr = [];
    if (howMany > 1) {
        var incr = step ? step : 1;
        for (var i = incr; i < howMany * incr; i += incr) {
            arr.push(i);
        }
    } else {
        arr.push(1);
    }
    return arr;
}

function correctNoOfLabels(counter) {
    if (counter <= 18) {
        return createArrayOfInts(18);
    }
    //display 1h
    else if (counter <= 360) {
        return createArrayOfInts(20, 3); // 1 step = 3
    }
    else if (counter <= 8640) {
        return createArrayOfInts(24); //display 1 day. 1 step 1h
    }
    else if (counter <= (8640 * 7)) {
        return createArrayOfInts(7);
    }
}

function last18records(arr) {
    if (arr.length > 18) {
        return arr.slice(arr.length - 18);
    }
    else {
        return arr;
    }
}

function last18records(arr) {
    if (arr.length > 18) {
        return arr.slice(arr.length - 18);
    }
    else {
        return arr;
    }
}