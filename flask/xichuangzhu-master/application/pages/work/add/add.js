(function () {
    "use strict";

    $('.btn-search-wiki').click(function () {
        var title = $.trim($("#title").val());
        var title_suffix = $.trim($("#title_suffix").val());
        if (title_suffix) {
            title += " " + title_suffix;
        }
        window.open("http://baike.baidu.com/search?word=" + title);
    });
})();
