// 搜索作者
$('#btn-search-author').click(function () {
    var author_name = $('#input-author-name').val();
    $.ajax({
        'url': urlFor('work.search_authors'),
        'type': 'POST',
        'dataType': 'json',
        'data': {
            'author_name': author_name
        },
        'success': function (authors) {
            $('#author_id').empty();

            $.each(authors, function (index, author) {
                var option = "<option value=" + author['id'] + ">〔" + author['dynasty'] + '〕'
                    + author['name'] + "</option>";
                $(option).appendTo('#author_id');
            });
        }
    });

    return false;
});

// type-layout联动
$('#type_id').change(function () {
    var type_id = parseInt($(this).val());

    if (type_id === 1) {
        $('#layout').val('center');
    } else {
        $('#layout').val('indent');
    }
});