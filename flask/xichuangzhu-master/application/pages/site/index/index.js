(function () {
    "use strict";

    $('#work-refresh').click(function () {
        $.ajax({
            url: urlFor('site.works'),
            type: 'POST',
            success: function (data) {
                $('#index-works-wap').html(data);

                // s2t
                var bodyIsFt = $.cookie("bodyIsFt");
                if (bodyIsFt == "1") {
                    StranObj($('#4works-wap')[0], 1);
                }
            }
        });
    });
})();
