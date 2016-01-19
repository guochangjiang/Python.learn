(function () {
    "use strict";

    var dynasty = $.trim($("#dynasty-selector li.active").text());
    var work_type = $.trim($("#type-selector li.active").text());

    if (dynasty === '全部' && work_type === '全部') {
        $('#dynasty_type_tag').text('作品');
    } else if (dynasty === '全部') {
        $('#dynasty_type_tag').text(work_type);
    } else if (work_type === '全部') {
        $('#dynasty_type_tag').text(dynasty);
    } else {
        $('#dynasty_type_tag').text(dynasty + ' / ' + work_type);
    }
})();
