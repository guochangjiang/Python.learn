(function () {
    "use strict";

    // 生成注释及tooltip
    $('.work-content sup').tooltip().each(function (index, element) {
        // $(this).text('〔' + (index + 1) + '〕');
        // $(this).text('[' + (index + 1) + ']');
        $(this).text(index + 1);

        var annotate = $(element).data('original-title');
        $('.work-annotate').append("<div><span class='annotate-index'>" + (index + 1)
            + '</span>&nbsp;&nbsp' + annotate + '</div>');
    });

    //// 对居中排版的诗进行重新排版
    //function layout() {
    //    var wap = $('.work-type-shi.work-layout-center');
    //    if (wap.length != 0) {
    //        var wapWidth = wap.width();
    //        var sum = 0, mean = 0;
    //
    //        // 将p设置为inline-block，以获取其宽度
    //        wap.children('p').each(function () {
    //            $(this).css({
    //                display: 'inline-block',
    //                paddingLeft: '0px'
    //            });
    //        });
    //
    //        // 计算p的平均宽度
    //        wap.children('p').each(function () {
    //            sum += $(this).width();
    //        });
    //        mean = sum / wap.children('p').length;
    //
    //        // 设置p的左间距
    //        wap.children('p').each(function () {
    //            $(this).css({
    //                display: 'block',
    //                paddingLeft: ((wapWidth - mean) / 2) + 'px'
    //            });
    //        });
    //    }
    //}
    //
    //layout();
    //
    //$(window).resize(function () {
    //    layout();
    //});

    $('.btn-rm-quote').click(function () {
        if (!confirm('确认删除此摘录？')) {
            return false;
        }
    });
})();
