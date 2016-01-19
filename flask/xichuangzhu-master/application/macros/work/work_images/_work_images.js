// water fall layout
function waterfall() {
    // 一个很奇怪的bug，如果没有image存在，页面会崩溃。
    // 这个是不是imagesloaded插件的bug？
    var workImages = $('.work-image');
    if (workImages.length === 0) {
        return;
    }

    var parentWap = $('.work-images-wap'),
        width = workImages.width(),
        h_gap = 15,
        v_gap = 15,
        lefts = [],
        tops = [],
        parentWidth = parentWap.width(),
        columns = Math.floor(parentWidth / width);

    for (var i = 0; i < columns; i++) {
        lefts.push(i * (width + h_gap));
        tops.push(0);
    }

    parentWap.imagesLoaded().progress(function (instance, image) {
        // get the min height column
        var img = image.img;
        var minHeight = tops[0];
        var minHeightColumn = 0;

        for (var i = 0; i < tops.length; i++) {
            if (tops[i] < minHeight) {
                minHeight = tops[i];
                minHeightColumn = i;
            }
        }

        $(img).parent().css({
            'display': 'block',
            'left': lefts[minHeightColumn] + 'px',
            'top': tops[minHeightColumn] + 'px',
            'height': $(img).height()
        });

        // Overadd height
        tops[minHeightColumn] += $(img).height() + v_gap;

        // Set mother wap's height
        var maxHeight = Math.max.apply(null, tops);
        parentWap.css('height', maxHeight + 'px');
    });
}

waterfall();

$(window).resize(function () {
    waterfall();
});