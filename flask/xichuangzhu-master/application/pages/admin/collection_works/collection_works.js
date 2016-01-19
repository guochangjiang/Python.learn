(function () {
    "use strict";

    var $workInput = $page('.input-work-title').first();
    var $btnAddWork = $page('.btn-add-work').first();
    var $workSelect = $page('.work-select').first();
    var $worksList = $page('.works-list').first();
    var $addWorkModal = $page('#add-work-modal');
    var $btnRemoveWorkFromCollection = $page('.btn-remove-work-from-collection');
    var $btnSearchWork = $page('.btn-search-work');

    $workInput.keyup(function (event) {
        if (event.keyCode == 13) {
            searchWork();
        }
    });

    $btnSearchWork.click(function () {
        searchWork();
    });

    $btnAddWork.click(function () {
        $.ajax({
            url: urlFor('collection.do_add_work', {uid: g.collectionId}),
            method: 'POST',
            data: {
                'work_id': $workSelect.val()
            }
        }).done(function (response) {
            if (response.result) {
                $workInput.val('').focus();
                $workSelect.empty();
            } else {
                alert("出错啦!");
            }
        });
    });

    $btnRemoveWorkFromCollection.click(function () {
        var workId = parseInt($(this).data('id'));
        var workTitle = $(this).data('title');
        var _this = $(this);

        if (!confirm('确定将《' + workTitle + '》从该合集中移除？')) {
            return false;
        }

        $.ajax({
            url: urlFor('collection.remove_work', {uid: g.collectionId, work_id: workId}),
            method: 'POST'
        }).done(function (response) {
            if (response.result) {
                _this.parents('tr').first().detach();
            }
        });
    });

    $worksList.sortable({
        helper: fixHelper,
        stop: function () {
            var orders = [];

            $worksList.find('tr').each(function (index) {
                var order = parseInt($(this).attr('data-order'));
                var id = parseInt($(this).attr('data-id'));

                if (order !== index + 1) {
                    orders.push({'id': id, 'order': index + 1});
                }
            });

            if (orders.length === 0) {
                return;
            }

            $.ajax({
                url: urlFor('collection.update_works_order'),
                method: 'POST',
                data: {
                    'orders': JSON.stringify(orders)
                }
            }).done(function (response) {
                if (response.result) {
                    $worksList.find('tr').each(function (index) {
                        $(this).attr('data-order', index + 1);
                    });
                }
            });
        }
    }).disableSelection();

    $addWorkModal.on('shown.bs.modal', function (event) {
        $workInput.focus();
    }).on('hidden.bs.modal', function (event) {
        location.reload(true);
    });

    function fixHelper(e, ui) {
        ui.children().each(function () {
            $(this).width($(this).width());
        });
        return ui;
    }

    function searchWork() {
        var workTitle = $.trim($workInput.val());

        $.ajax({
            url: urlFor('work.search'),
            method: 'POST',
            data: {
                'title': workTitle
            }
        }).done(function (response) {
            if (response.result) {
                $workSelect.empty();

                $.each(response.works, function (index, work) {
                    var option = "<option value=" + work['id'] + ">〔" + work['author'] + '〕'
                        + work['title'] + "</option>";
                    $(option).appendTo($workSelect);
                });
            }
        });
    }
})();
