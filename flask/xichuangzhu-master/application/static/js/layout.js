(function () {
    "use strict";

    // convert simple to fanti if needed
    var bodyIsFt = $.cookie("bodyIsFt");

    if (bodyIsFt == "1") {
        $(document.body).s2t();
        $('#btn-s2t').text('繁');
    } else {
        $('#btn-s2t').text('简');
    }

    // Add CSRF token header for Ajax request
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", g.csrfToken);
            }
        }
    });

    // Flash message
    var flashMessage = $('.flash-message');
    var flashWidth = ($(window).width() - flashMessage.width()) / 2;
    flashMessage.css({'left': flashWidth + 'px'});
    flashMessage.fadeIn(200);
    setTimeout(flashMessageFade, 2000);

    // 百度统计
    var _bdhmProtocol = (("https:" == document.location.protocol) ? " https://" : " http://");
    document.write(unescape("%3Cscript src='" + _bdhmProtocol + "hm.baidu.com/h.js%3Ff6ec6187fb2e01e57301c5f03953176f' type='text/javascript'%3E%3C/script%3E"));


    function flashMessageFade() {
        $('.flash-message').fadeOut('slow');
    }
})();
