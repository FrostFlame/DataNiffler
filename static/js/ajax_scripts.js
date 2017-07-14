$(document).ready(function () {

    $('#clickID').click(function () {
        $.ajax({
            url: "someURLGoesHere",
            type: 'GET',
            success: function (data) {
                $('#someEl_2').html(data)
            },
            dataType: JSON
        });
    });

});

