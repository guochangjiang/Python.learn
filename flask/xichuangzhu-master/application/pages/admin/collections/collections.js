(function () {
    "use strict";
    var $collectionsLists = $page('.collections-list');

    $collectionsLists.each(function () {
        var $collectionsList = $(this);

        $collectionsList.sortable({
            helper: fixHelper,
            stop: function () {
                var orders = [];

                $collectionsList.find('tr').each(function (index) {
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
                    url: urlFor('collection.update_order'),
                    method: 'POST',
                    data: {
                        'orders': JSON.stringify(orders)
                    }
                }).done(function (response) {
                    if (response.result) {
                        $collectionsList.find('tr').each(function (index) {
                            $(this).attr('data-order', index + 1);
                        });
                    }
                });
            }
        }).disableSelection();
    });

    function fixHelper(e, ui) {
        ui.children().each(function () {
            $(this).width($(this).width());
        });
        return ui;
    }
})();
