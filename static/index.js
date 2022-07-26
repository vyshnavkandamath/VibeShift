
$(document).ready(function(){
    console.log("document ready")
    $("buttonclick").click(function(){
        submitLocation();
    });

});



let locationInfo;

function submitLocation() {
    console.log("submitted info");
    locationInfo =  document.getElementById("userInput").value; 

}


    

    // $.ajax({

    //     url: 'http://api.weatherapi.com/v1/current.json',
    //     type: 'GET',
    //     data: {
    //         'q': 20841
    //     },
    //     headers: {
    //         "key": "TBD Weather API key value"
    //     },
    //     dataType: 'json',
    //     success: function (data) {
    //         alert('Data: ' + JSON.stringify(data));
    //     },
    //     error: function (request, error) {
    //         alert("Request: " + JSON.stringify(request));
    //     }

    // });





