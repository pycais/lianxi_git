$(function () {
    $("button").click(function () {
        var email = $("#exampleInputEmail1").val();
        var name = $("#name").val();
        var pwd = $("#pwd").val();
        var confirm_pwd = $("#confirm_pwd").val();
        var verify = $("#verify").val();
        if (email.length == 0 || name.length == 0 || pwd.length == 0 || verify.length ==0) {
            alert("请填写完整信息");
            return;
        }
        if (pwd != confirm_pwd) {
            alert("两次密码不一致");
            return;
        }
    //    发送请求
        $.ajax({
            url:"/register",
            method:"post",
            data:{
                name: name,
                pwd: pwd,
                confirm_pwd: confirm_pwd,
                email: email,
                verify: verify
            },
            success:function (res) {
                if (res.code == 0){
                    window.open(res.data.next, target="_self");
                } else {
                    alert(res.msg);
                }
            }
        })
    });
    $("img").click(function () {
        $(this).attr("src", "/captcha/" + Math.random());
    });
});