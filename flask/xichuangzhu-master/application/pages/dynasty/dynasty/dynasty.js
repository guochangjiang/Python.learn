(function () {
    "use strict";

    // get random rgb color in css style
    function random_color() {
        var r, g, b;

        r = Math.floor(Math.random() * 255 + 1);
        g = Math.floor(Math.random() * 200 + 1);
        b = Math.floor(Math.random() * 255 + 1);
        return 'rgb(' + r + ',' + g + ',' + b + ')';
    }

    var dynastiesCount = g.dynastiesCount;

    // set random color
    $('#dyn-selector a').each(function () {
        $(this).css({
            'height': '22px',
            'width': $(window).width() / dynastiesCount + 'px',
            'background-color': random_color()
        });
    });

    // when change window size
    $(window).resize(function () {
        $('#dyn-selector a').css({
            'width': $(window).width() / dynastiesCount + 'px'
        });
    });
})();
