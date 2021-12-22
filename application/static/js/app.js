function get_captcha() {
    $.get(
        "/ajax/get_captcha",
        function (result) {
            $("#captcha>img").attr('src', result['msg']['img_src'])
        }
    )
}


function upload_img_modal() {
    $("#upModal").modal("show");
}

function password_modal() {
    $("#passwordModal").modal("show");
}

function comment_modal() {
    $("#commentModal").modal("show");
}

function email_modal() {
    $("#emailModal").modal("show");
}

function formation_up() {
    $("#formationModal").modal("show");
    $.get(
        "/ajax/get_captcha",
        function (result) {
            $("#captcha>img").attr('src', result['msg']['img_src'])
        }
    )
}

function upload_img(file) {
    let formData = new FormData()
    formData.append('file', file.files[0]);
    if (file.files.length > 0) {
        $.ajax({
            type: 'post',
            url: '/ajax/upload_img',
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            success: function (result) {
                $("#uploaded>img").attr("src", result['msg']['data']);
            },
            error: function (result) {
                alert("上传文件失败")
            }
        })
    }
}

function concel() {
    $("#uploaded>img").attr("src", "");
    var file = $("#upModal > input[type=file]");
    file.val("")
    file.attr("value", "")
}

function ok(v) {
    $("#uploaded>img").attr("src", "");
    var file = $("#upModal > input[type=file]");
    file.val("")
    file.attr("value", "")
    alert("上传成功")
}

function down_formation() {
    $("#name").val("");
    $("#sex").val("");
    $("#zy").val("");
    $("#zym").val("");
    $("#yzm").val("");
}

function modify_formation() {
    alert($('#yzm_formation').val())
    var data = {
        'name': $("#name").val(),
        'sex': $("#sex").val(),
        'zy': $("#zy").val(),
        'zym': $("#zym").val(),
        'yzm': $("#yzm_formation").val()
    }
    $.post(
        '/ajax/modify_formation',
        JSON.stringify(data),
        function (result) {
            alert(result['msg']);
            location.reload();
        }
    )
}

function send_email() {
    var data = {
        'email': $("input[type=email]").val()
    }
    if (data['email'] !== "") {
        $.post(
            "/ajax/get_email_yzm",
            JSON.stringify(data),
            function (result) {
                alert(result['msg']);
            }
        )
    }
}

function send_email_pass() {
    var data = {
        'email': "已经绑定了邮箱"
    }
    if (data['email'] !== "") {
        $.post(
            "/ajax/get_email_yzm",
            JSON.stringify(data),
            function (result) {
                alert(result['msg']);
            }
        )
    }
}

function modify_email() {

    var data = {
        'email': $("input[type=email]").val(),
        'yzm': $('#yzm').val()
    }
    $.post(
        "/ajax/modify_email",
        JSON.stringify(data),
        function (result) {
            alert(result['msg']);
            $("input[type=email]").val("")
        }
    )
}

function modify_passwd() {
    var data = {
        'passwd': $("#new_passwd").val(),
        'yzm': $('#yzm_passwd').val()
    }
    $.post(
        "/ajax/modify_passwd",
        JSON.stringify(data),
        function (result) {
            alert(result['msg']);
            $("input[type=email]").val("")
        }
    )
}

function concel_email() {
    $("input[type=email]").val("")
    $("#yzm").val("");
}

function concel_passwd() {
    $("#new_passwd").val("")
    $("#yzm_passwd").val("")
}

function dz() {
    $("#dz").removeClass("glyphicon-heart-empty");
    $("#dz").addClass("glyphicon-heart")
}

function collect() {
    $("#collect").removeClass("glyphicon-star-empty")
    $("#collect").addClass("glyphicon-star")
}

function concel_comment() {
    $("#comment_content").val("")
}

function cancel_modal(id) {
    $("#" + id).val("")
}

function send_comments() {
    concel_comment()
}

function page(v) {
    var page = v.getAttribute("data-page");
    show_posts(page);
}

function show_posts(page = 1) {

    $.post(
        '/ajax/get_posts',
        JSON.stringify({'page': parseInt(page)}),
        function (result) {
            $("#show_posts").html(result['msg']['data'])
            document.getElementById("self_btn").dataset.type = 'post'
        }
    )
}

function show_collect_posts(page = 1) {

    $.post(
        '/ajax/get_collect_posts',
        JSON.stringify({'page': parseInt(page)}),
        function (result) {
            $("#show_collect_posts").html(result['msg']['data'])
        }
    )
}

function show_works(page = 1) {

    $.post(
        '/ajax/get_works',
        JSON.stringify({'page': parseInt(page)}),
        function (result) {
            $("#show_works").html(result['msg']['data'])
            document.getElementById("self_btn").dataset.type = 'work'
        }
    )
}

function show_works_sp(page = 1, sp) {

    $.post(
        '/ajax/get_works_species',
        JSON.stringify({'page': parseInt(page), 'sp_id': sp}),
        function (result) {
            $("#show_works").html("")
            $("#show_works").html(result['msg']['data'])
        }
    )
}

function show_posts_sp(page = 1, sp) {

    $.post(
        '/ajax/get_posts/species',
        JSON.stringify({'page': parseInt(page), 'sp_id': sp}),
        function (result) {
            $("#show_posts").html("")
            $("#show_posts").html(result['msg']['data'])
        }
    )
}

function show_message() {
    $.get(
        '/ajax/get_messages',
        function (result) {
            $("#show_message").html(result['data'])
        }
    )
}

function readed(id) {
    $.post(
        '/ajax/is_read',
        JSON.stringify({'id': parseInt(id)}),
        function (result) {
            $("#" + result['id']).removeClass('label-danger')
            $("#" + result['id']).removeClass('btn-danger')
            $("#" + result['id']).addClass('label-success')
            $("#" + result['id']).addClass('btn-success')
            $("#" + result['id']).text("已读")
            $(".badge").text(result['count']);
        }
    )
}

function del_msg(id) {
    $.post(
        '/ajax/del_msg',
        JSON.stringify({'id': parseInt(id)}),
        function (result) {
            if (result['code'] === 200) {
                show_message()
            }
        }
    )
}

function collect(id) {
    $.post(
        '/ajax/collect_post',
        JSON.stringify({'id': parseInt(id)}),
        function (result) {
            if (result['code'] === 200) {
                alert(result['msg'])
                $("button.btn:nth-child(7)").text("取消收藏")
                $("button.btn:nth-child(7)").attr('onclick', 'un_collect(' + result['id'] + ')')
            }
        }
    )
}

function un_collect(id) {
    $.post(
        '/ajax/un_collect_post',
        JSON.stringify({'id': parseInt(id)}),
        function (result) {
            if (result['code'] === 200) {
                alert(result['msg'])
                $("button.btn:nth-child(7)").text("收藏")
                $("button.btn:nth-child(7)").attr('onclick', 'collect(' + result['id'] + ')')
            }
        }
    )
}

function un_collect_by_self(id) {
    $.post(
        '/ajax/un_collect_post',
        JSON.stringify({'id': parseInt(id)}),
        function (result) {
            if (result['code'] === 200) {
                alert(result['msg'])
                show_collect_posts(1)
            }
        }
    )
}

function load_file(file) {
    alert(file)
    $.post(
        '/ajax/download_file',
        JSON.stringify({'file': file}),
        function (result) {
            alert(result['code']);
            console.log(result['data'])
        }
    )
}

function show_file_submit() {
    $("#submitModal_by_file").modal('show')
}

function show_blog_url() {
    $("#submitModal_by_blog").modal('show')
}

function choose_way() {
    var msg = "选择上传博客链接还是上传文件：点击是 则是上传博客链接"
    if (confirm(msg) === true) {
        show_blog_url();
    } else {
        show_file_submit()
    }
}

function submit_blog(flag = 'blog', file = null) {
    var url = null
    if (flag === 'blog') {
        url = $("#blog_url").val()
    } else {
        url = file
    }

    var id = $("#get_h_id").data("hid")
    $.post(
        '/ajax/submit_homework',
        JSON.stringify({'url': url, 'id': parseInt(id), 'flag': 'blog'}),
        function (result) {
            alert('作业提交成功');
            $("body > div.col-lg-8.col-sm-offset-3.post-text > div:nth-child(4) > button:nth-child(7)").text("提交作业/完成")
            $("body > div.col-lg-8.col-sm-offset-3.post-text > div:nth-child(4) > button:nth-child(7)").removeClass("btn-info");
            $("body > div.col-lg-8.col-sm-offset-3.post-text > div:nth-child(4) > button:nth-child(7)").addClass("btn-success");
        }
    )
}

function submit_file(file) {
    let formData = new FormData()
    formData.append('file', file.files[0]);
    if (file.files.length > 0) {
        $.ajax({
            type: 'post',
            url: '/ajax/submit_homework_file',
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            success: function (result) {
                $("#submit_file").click(function () {
                    alert('作业提交成功');
                    submit_blog('file', result['path'])
                })

            },
            error: function (result) {
                alert("上传文件失败")
            }
        })
    }
}

function search() {
    var data = {
        'type': $("#p_w").val(),
        'page': 1,
        'content': $("#search_content").val()
    }
    $.post(
        '/ajax/search',
        JSON.stringify(data),
        function (result) {
            if (result['msg']['type'] === 'work'){
                $("#works").html()
                $("#works").html(result['msg']['data'])
            }
            else{
                $("#posts").html()
                $("#posts").html(result['msg']['data'])
            }

        }
    )
}
function search_self() {
    var data = {
        'type': document.getElementById("self_btn").dataset.type,
        'page': 1,
        'content': $("#search_content_self").val()
    }
    $.post(
        '/ajax/search_self',
        JSON.stringify(data),
        function (result) {
            if (result['msg']['type'] === 'work'){
                $("#show_works").html()
                $("#show_works").html(result['msg']['data'])
            }
            else{
                $("#show_posts").html()
                $("#show_posts").html(result['msg']['data'])
            }

        }
    )
}