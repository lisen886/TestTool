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