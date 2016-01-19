(function () {
    var uploader = new plupload.Uploader({
        browse_button: 'btn-upload-work-image',
        url: urlFor('work.upload_image'),
        multipart_params: {
            csrf_token: g.csrfToken
        },
        filters: {
            max_file_size: '10mb'
        }
    });

    uploader.init();

    // 文件添加后立即启动上传
    uploader.bind('FilesAdded', function (up, files) {
        uploader.setOption();

        plupload.each(files, function (file) {
            uploader.start();
        });
    });

    var errorList = $('.list-form-errors');

    // 上传结束
    uploader.bind('FileUploaded', function (up, file, info) {
        var response = $.parseJSON(info.response);
        if (response.status === 'yes') {
            $('#image').val(response.filename);
            $('.preview').show().attr('src', response.url);
            errorList.empty();
        } else if (response.status === 'no') {
            errorList.html("<li>" + response.error + "</li>");
        } else {
            errorList.html("<li>上传失败，请刷新页面后再试。</li>");
        }
    });

    // 显示文件上传进度条
    uploader.bind('UploadProgress', function (up, file) {
        $('.progress-bar').css('width', file.percent + '%').text(file.percent + "%");
    });

    // 上传失败
    uploader.bind('Error', function (up, error) {
        console.log(error);
        errorList.html("<li>" + error.message + "</li>");
    });
})();