function getQueryParam(param) {
    location.search.substr(1)
        .split("&")
        .some(function(item) { // returns first occurence and stops
            return item.split("=")[0] == param && (param = item.split("=")[1])
        });
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

        // Populate the big blog and enable displaying it
        $("#full-result-value").text(JSON.stringify(data));
        $("#show-full-results").prop("disabled", false);
        $("#show-full-results").text("Show extended results");
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

function setupWebcam() {
    // Thanks https://github.com/jhuckaby/webcamjs
    $("#camera-container").hide();

    $("#snapshot").click(function() {
        $("#snapshot").prop("disabled", true);
        Webcam.snap( function(data_uri) {
            var upload_url = $("#image-upload-form").attr("action");
            Webcam.upload( data_uri, upload_url, function(code, text) {
                if (code == 200) {
                    window.location.replace(text);
                } else {
                    console.log(code);
                    console.log(text);
                    // Maybe try again?
                    $("#snapshot").prop("disabled", false);
                }
            } );
        });
    });

    $("#enable-camera").click(function(){
        if (!$("#enable-camera").attr("data-camera-attached")) {
            console.log("Initializing Webcam");
            $("#camera-container").slideDown(500, function(){
                Webcam.attach("#my_camera");
                $("#enable-camera").attr("data-camera-attached", true)
            });
        }
        return false;
    });
}

function setupJSONView() {
    $("#show-full-results").click(function(){
        var j = JSON.parse($("#full-result-value").text());
        $("#full-result-container").slideDown(
            500,
            function() {
                $("#full-result-container").JSONView(j);
            });
    })
}

$(document).ready(function() {
    setupWebcam();
    setupJSONView();
});