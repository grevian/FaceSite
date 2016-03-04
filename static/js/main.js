function getQueryParam(param) {
    location.search.substr(1)
        .split("&")
        .some(function(item) { // returns first occurence and stops
            return item.split("=")[0] == param && (param = item.split("=")[1])
        })
    return param
}

function pollComplete(data, image_id) {
    console.log(data);
    // If still building, wait 3 seconds then try again
    if (data["status"] == "pending") {
        console.log("Still Building, Polling Again");
        setTimeout(function() { pollImage(image_id); }, 3000);
    }
    // If completed, Display the data
    else if (data["responses"]) {
        console.log("Analysis Complete");
        $("#datablock").show();

        // The emotional details
        $("#anger-rating").text(data.responses[0].faceAnnotations[0].angerLikelihood);
        $("#joy-rating").text(data.responses[0].faceAnnotations[0].joyLikelihood);
        $("#sorrow-rating").text(data.responses[0].faceAnnotations[0].sorrowLikelihood);
        $("#surprise-rating").text(data.responses[0].faceAnnotations[0].surpriseLikelihood);

        // Hat factor
        $("#hat-rating").text(data.responses[0].faceAnnotations[0].headwearLikelihood);

        // Confidence of detection
        $("#confidence-rating").text(data.responses[0].faceAnnotations[0].detectionConfidence);

        // Do you suck at photos?
        $("#blurred-rating").text(data.responses[0].faceAnnotations[0].blurredLikelihood);
        $("#underexposed-rating").text(data.responses[0].faceAnnotations[0].underExposedLikelihood);

    }
}

function pollImage(image_id) {
    var pollPath = '/api/poll/' + image_id;
    $.get(pollPath, function( data ){
        pollComplete(data, image_id);
    }, "json").fail(
        function() {

        }
    );
}
