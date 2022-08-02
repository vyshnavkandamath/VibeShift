function loadData() {
    let inputData;

    $(document).ready(function () {
        inputData = sessionStorage.getItem('locationInput')
        $.ajax({

            url: '/playlistInfo',
            type: 'POST',
            data: {
                'location': inputData,
            },
            headers: {
                "key": "Weather API secret key value"
            },
            dataType: 'json',
            success: function (data) {
                // alert('Data: ' + JSON.stringify(data));
                console.log(data);

            },
            error: function (request, error) {
                // alert("Request: " + JSON.stringify(request));
                alert('Did not input value correctly, try again' + request.responseJSON.message());
            }

        });

        $.ajax({

            url: '/playlistInfo',
            type: 'GET',
            headers: {
                "key": "Weather API secret key value"
            },
            dataType: 'json',
            success: function (data) {
                // alert('Data: ' + JSON.stringify(data));
                console.log(data);
                let obj = JSON.parse(JSON.stringify(data));
                console.log(obj);
                let playlistName = obj['name'];
                console.log(playlistName);
                let playlistImage = obj.images[0].url;
                console.log(playlistImage);

                document.getElementById('PlaylistName').innerHTML = playlistName;
                document.getElementById('PlaylistImage').src = playlistImage;
            },
            error: function (request, error) {
                alert("Request: " + JSON.stringify(request));
            }

        });




    })

}
