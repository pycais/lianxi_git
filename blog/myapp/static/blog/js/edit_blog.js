var editor;
        $(function () {
            editor = KindEditor.create('textarea[name="v_content"]', {
                resizeType: 1, width: "100%", height: "200px", afterChange: function () {
                    this.sync();
                }, afterBlur: function () {
                    this.sync();
                }
            });

        // {#    给标签按钮添加点击事件#}
            $(".btn.tag").click(function () {
                var current_class = $(this).attr("class");
                if (current_class == "btn tag"){
                    $(this).removeClass(current_class).addClass("btn btn-primary tag");
                } else {
                    $(this).removeClass(current_class).addClass("btn tag");
                }
            })
        });
        $(".btn.btn-success.submit").click(function () {
        // {#    拿标题#}
            var title = $("#title").val();
            var content = $("#v_content").val();

            var tags = [];
            $(".btn.btn-primary.tag").each(function () {
                tags.push($(this).attr("tag_id"));
            })
        // {#    校验数据#}
            if (title.length<4){
                alert("标题要大于四个字");
                return;
            }
            if (content.length==0){
                alert("请编辑您的内容");
                return;
            }
            if (tags.length == 0){
                alert("至少选择一个标签");
                return;
            }
        //  发送请求
            $.ajax({
                url:"/blog",
                method:"post",
                data:{
                    title: title,
                    content: content,
                    tags: JSON.stringify(tags)
                },
                success: function (res) {
                    alert(res.msg);
                }
            });
        })