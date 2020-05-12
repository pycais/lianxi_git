var editor;
$(function () {
    editor = KindEditor.create('textarea[name="v_content"]', {
                resizeType: 1, width: "100%", height: "200px", afterChange: function () {
                    this.sync();
                }, afterBlur: function () {
                    this.sync();
                }
            });
    $("#submit").click(function () {
        var blog_id = $(this).attr("blog_id");
        var content = $("#v_content").val();
        if (content.length<=0){
            alert("请先编辑您的答案");
            return;
        }
        $.ajax({
            url:"/blog/comment",
            method: "post",
            data:{
                blog_id: blog_id,
                content: content
            },
            success:function (res) {
                if (res.code == 0 || res.code == 1){
                    var result = confirm(res.msg);
                    if (result == true){
                        window.open(res.data.next, target="_self")
                    }
                } else{
                    confirm(res.msg);
                }
            }
        })
    })
});