(function () {
    "use strict";

    if (!g.signedIn) {
        return;
    }

    // move the blink to the end of the input/textarea
    function moveEnd(obj) {
        obj.focus();
        var len = obj.value.length;

        if (document.selection) {
            var sel = obj.createTextRange();
            sel.moveStart('character', len);
            sel.collapse();
            sel.select();
        } else if (typeof obj.selectionStart == 'number' && typeof obj.selectionEnd == 'number') {
            obj.selectionStart = obj.selectionEnd = len;
        }
    }

    $('.btn-delete-topic').click(function () {
        return confirm('确认删除此话题？');
    });

    $('.comment-item').hover(
        function () {
            $(this).find('.btn-reply-somebody').show();
        },
        function () {
            $(this).find('.btn-reply-somebody').hide();
        }
    );

    $('.btn-reply-somebody').click(function () {
        var target_username = $(this).attr('data-username');
        var comment = $(".textarea-comment").val();

        $(".textarea-comment").val("@" + target_username + " " + comment);
        moveEnd($(".textarea-comment")[0]);
    });
})();
