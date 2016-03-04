$( document ).ready(function() {
    var image_id = window.location.pathname.substr(1).split("/")[1];
    var preloaded = $("#preloaded-marker").val()
    if (image_id && preloaded != 0) {
        pollImage(image_id)
    }
});
