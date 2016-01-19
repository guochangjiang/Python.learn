(function () {
    "use strict";

    var left = $(document).outerWidth() - $(window).width();

    // $('#main-wap').s2t();

    adjustHeight();
    $('body, html').scrollLeft(left);
    $('.work-content sup').detach();
    $('body').on("mousewheel", mouseWheelEvt);

    $(window).resize(function () {
        adjustHeight();
    });

    /**
     * 滚动鼠标滚轮时窗口左右滑动
     * @param event
     * @returns {boolean}
     */
    function mouseWheelEvt(event) {
        if (document.body.doScroll)
            document.body.doScroll(event.wheelDelta > 0 ? "left" : "right");
        else if ((event.wheelDelta || event.detail) > 0)
            document.body.scrollLeft -= 10;
        else
            document.body.scrollLeft += 10;

        return false;
    }

    function adjustHeight() {
        var windowHeight = $(window).height();

        if (windowHeight < 600 + 60 * 2) {
            $('#main-wap').height(windowHeight - 60 * 2).css('paddingRight', 60);
        } else {
            $('#main-wap').height(600).css('paddingRight', 100);
        }
    }
})();
