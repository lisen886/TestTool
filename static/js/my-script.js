var cateid = 0;
$('#modal-container-829514').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    cateid = button.data('id').split(",");
	//向模态框中传值
	userName = cateid[0];
	team = cateid[1];
	password = cateid[2];
	tel = cateid[3];
    $('#userName').val(userName);
    $('#team').val(team);
    $('#password').val(password);
    $('#tel').val(tel);
    $('#update').modal('show');
});

$('#modal-container-829515').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    userName = button.data('id');
	//向模态框中传值
    $('#deleteUserName').val(userName);
    $('#update').modal('show');
});

$('#modal-container-82951').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    cateid = button.data('id').split(",");
	//向模态框中传值
	Name = cateid[0];
	value = cateid[1];

    $('#Name').val(Name);
    $('#value').val(value);
    $('#update').modal('show');
});

function deleteUser() {
	var catename = $("#deleteUserName").val();
    // if (catename == '') {
    //     alert("请输入要删除的用户名！！！");
    //     return;
    // }
    $.ajax({
        url:'/deleteUser',
        type:'post',
        dataType: 'json',
        data:{catename:catename},
        error:function(){
            alert('出现错误！');
        },success:function (data){
            if(data.status == 200){
                $('#modal-container-829515').modal('hide');
                location.reload();
            }else {
                alert("无法删除该用户！！！")
            }

        }
    })
}

function updateUser() {
	var userName = $("#userName").val();
	var team = $("#team").val();
	var password = $("#password").val();
	var tel = $("#tel").val();
    $.ajax({
        url:'/updateUser',
        type:'post',
        dataType: 'json',
        data:{userName:userName,team:team,password:password,tel:tel},
        error:function(){
            alert('出现错误！');
        },success:function (data){
            if(data.status == 200){
                $('#modal-container-829514').modal('hide');
                location.reload();
            }else {
                alert("无法更新该用户信息！！！")
            }

        }
    })
}

function updateConfig() {
	var Name = $("#Name").val();
	var value = $("#value").val();
    $.ajax({
        url:'/updateConfig',
        type:'post',
        dataType: 'json',
        data:{Name:Name,value:value},
        error:function(){
            alert('出现错误！');
        },success:function (data){
            if(data.status == 200){
                $('#modal-container-829514').modal('hide');
                location.reload();
            }else {
                alert("无法更新配置信息！！！")
            }

        }
    })
}

/**
 * 重写确认框 fun:函数对象 params:参数列表， 可以是数组
 */
function my_confirm(fun, params,msg) {
    if ($("#myConfirm").length > 0) {
        $("#myConfirm").remove();
    }
    var html = "<div class='modal fade' id='myConfirm' >"
            + "<div class='modal-backdrop in' style='opacity:0; '></div>"
            + "<div class='modal-dialog' style='z-index:2901; margin-top:60px; width:400px; '>"
            + "<div class='modal-content'>"
            + "<div class='modal-header'  style='font-size:16px; '>"
            + "<span class='glyphicon glyphicon-envelope'>&nbsp;</span>信息！<button type='button' class='close' data-dismiss='modal'>"
            + "<span style='font-size:20px;  ' class='glyphicon glyphicon-remove'></span><tton></div>"
            + "<div class='modal-body text-center' id='myConfirmContent' style='font-size:18px; '>"
            + msg
            + "</div>"
            + "<div class='modal-footer ' style=''>"
            + "<button class='btn btn-danger ' id='confirmOk' >确定<tton>"
            + "<button class='btn btn-info ' data-dismiss='modal'>取消<tton>"
            + "</div>" + "</div></div></div>";
    $("body").append(html);

    $("#myConfirm").modal("show");

    $("#confirmOk").on("click", function() {
        $("#myConfirm").modal("hide");
        fun(params); // 执行函数
    });
}

function my_showTip(msg) {
    if ($("#myConfirm").length > 0) {
        $("#myConfirm").remove();
    }
    var html = "<div class='modal fade' id='myConfirm' >"
            + "<div class='modal-backdrop in' style='opacity:0; '></div>"
            + "<div class='modal-dialog' style='z-index:2901; margin-top:60px; width:400px; '>"
            + "<div class='modal-content'>"
            + "<div class='modal-header'  style='font-size:16px; '>"
            + "<span class='glyphicon glyphicon-envelope'>&nbsp;</span>提示！！！<button type='button' class='close' data-dismiss='modal'>"
            + "<span style='font-size:20px;  ' class='glyphicon glyphicon-remove'></span><tton></div>"
            + "<div class='modal-body text-center' id='myConfirmContent' style='font-size:18px; '>"
            + msg
            + "</div>"
            + "<div class='modal-footer ' style=''>"
            + "<button class='btn btn-danger ' id='confirmOk' >确定<tton>"
            + "</div>" + "</div></div></div>";
    $("body").append(html);

    $("#myConfirm").modal("show");
    $("#confirmOk").on("click", function() {
        $("#myConfirm").modal("hide");
    });
}
function formatDateTime(inputTime) {
    var date = new Date(inputTime);
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    m = m < 10 ? ('0' + m) : m;
    var d = date.getDate();
    d = d < 10 ? ('0' + d) : d;
    var h = date.getHours();
    h = h < 10 ? ('0' + h) : h;
    var minute = date.getMinutes();
    var second = date.getSeconds();
    minute = minute < 10 ? ('0' + minute) : minute;
    second = second < 10 ? ('0' + second) : second;
    // return y + '-' + m + '-' + d+' '+h+':'+minute+':'+second;
    return y + m + d
};