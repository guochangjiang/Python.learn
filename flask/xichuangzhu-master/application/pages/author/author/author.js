(function () {
    "use strict";

    var isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    if (isMac) {
        $('.work-title').each(function () {
            $(this).text($(this).text().replace(/ /g, ''));
        });
    }

    $('.works-num-wap span').click(function () {
        $('.works-num-wap span').removeClass('active');
        $(this).addClass('active');

        // show works of certain type
        var type = $(this).attr('data-work-type');
        if (type == 'all') {
            $('.work-item').show();
        } else {
            $('.work-item').each(function () {
                if ($(this).attr('data-work-type') === type) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        }
    });

    $('.author-quote').tooltip({
        placement: 'right'
    });

    $('.quote').tooltip();

    $('.btn-rm-quote').click(function () {
        if (!confirm('确认删除此摘录？')) {
            return false;
        }
    });
})();
