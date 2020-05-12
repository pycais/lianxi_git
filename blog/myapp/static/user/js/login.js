$(function () {
    $("button").click(function () {
        var name = $("#name").val();
        var pwd = $("#pwd").val();
        var verify = $("#verify").val();
        if ( name.length == 0 || pwd.length == 0 || verify.length==0) {
            alert("请填写完整信息");
            return;
        }
    //    发送请求
        $.ajax({
            url:"/login",
            method:"post",
            data:{
                name: name,
                pwd: pwd,
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