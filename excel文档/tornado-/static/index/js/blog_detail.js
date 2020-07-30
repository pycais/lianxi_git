$(function () {
    // 基于准备好的dom，初始化echarts实例

        var pythons = [],tornados=[],flasks=[], spides=[], djangos=[],
            others=[],analysis=[], dates=[];
        var myChart = echarts.init(document.getElementById('main'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                    text: 'Django博文'
                },
                xAxis: {
                    type: 'category',
                    data: []
                },
                yAxis: {
                    type: 'value'
                },
                series: [{
                    data: [],
                    type: 'line'
                }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);

        var lineChart = echarts.init(document.getElementById("python"));

        setline_data(lineChart, dates, pythons, "python博文");
        function setline_data(Chart,dates, data, title ) {
            var option = {
                title: {
                    text: title
                },
                xAxis: {
                    type: 'category',
                    data: dates
                },
                yAxis: {
                    type: 'value'
                },
                series: [{
                    data: data,
                    type: 'line'
                }]
            };
        Chart.setOption(option);
        }
        var tornadoChart = echarts.init(document.getElementById("tornado"));
        setline_data(tornadoChart, dates, tornados, "tornado博文");


        var spiderChart = echarts.init(document.getElementById("spider"));
        setline_data(spiderChart, dates, spides, "爬虫博文");


        var flaskChart = echarts.init(document.getElementById("flask"));
        setline_data(flaskChart, dates, flasks, "flask博文");


        var analysisChart = echarts.init(document.getElementById("analysis"));
        setline_data(analysisChart, dates, analysis, "数据分析博文");

        var otherChart = echarts.init(document.getElementById("other"));

        setline_data(otherChart, dates, others, "其他博文");

        var ws = new WebSocket("ws://sharemsg.cn:12341/ws/data")
        ws.onmessage = function (ev) {
            var res = JSON.parse(ev.data);
            date_data = res.now;
            dates.push(date_data);
            if (dates.length>7){
                dates.shift();
            }
            py_data = res.data[0].count_id
            pythons.push(py_data)
            if (pythons.length>7){
                pythons.shift();
            }
            setline_data(lineChart, dates, pythons, "python博文")
            django_data = res.data[1].count_id
            djangos.push(django_data);
            if (djangos.length>7){
                djangos.shift();
            }
            setline_data(myChart, dates, djangos, "django博文")
            flask_data = res.data[2].count_id
            flasks.push(flask_data)
            if (flasks.length>7){
                flasks.shift();
            }
            setline_data(flaskChart, dates, flasks, "flask博文")
            tor_data = res.data[3].count_id
            tornados.push(tor_data)
            if (tornados.length>7){
                tornados.shift();
            }
            setline_data(tornadoChart, dates, tornados, "tornado博文");
            py_data = res.data[4].count_id
            spides.push(py_data)
            if (spides.length>7){
                spides.shift();
            }
            setline_data(spiderChart, dates, spides, "爬虫博文");
            py_data = res.data[5].count_id
            analysis.push(py_data)
            if (analysis.length>7){
                analysis.shift();
            }
            setline_data(analysisChart, dates, analysis, "数据分析博文");
            py_data = res.data[6].count_id
            others.push(py_data)
            if (others.length>7){
                others.shift();
            }
            setline_data(otherChart, dates, others, "其他博文");
        }
})