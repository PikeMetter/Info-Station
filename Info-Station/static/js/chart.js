var chart1 = echarts.init(document.getElementById('map'), 'white', {renderer: 'canvas'});
var chart2 = echarts.init(document.getElementById('cure_line'), 'white', {renderer: 'canvas'});
var chart3 = echarts.init(document.getElementById('confirm_line'), 'white', {renderer: 'canvas'});
var chart4 = echarts.init(document.getElementById('word_cloud'), 'white', {renderer: 'canvas'});
$(
    function () {
        fetchMapData(chart1);
        fetchLineData(chart2);
        fetchConfirmLine(chart3);
        fetchWordCloud(chart4);
    }
);

//下面三个函数用于获取数据作图
function fetchMapData() {
    $.ajax({
        type: "GET",
        url: "/demo/map/",
        dataType: 'json',
        success: function (result) {
            chart1.setOption(result.data);
        }
    });
}
function fetchLineData() {
    $.ajax({
        type: "GET",
        url: "/demo/cure_line/",
        dataType: 'json',
        success: function (result) {
            chart2.setOption(result.data);
        }
    });
}
function fetchConfirmLine() {
    $.ajax({
        type: "GET",
        url: "/demo/confirm_line/",
        dataType: 'json',
        success: function (result) {
            chart3.setOption(result.data);
        }
    });
}
function fetchWordCloud() {
    $.ajax({
        type: "GET",
        url: "/demo/word_cloud/",
        dataType: 'json',
        success: function (result) {
            chart4.setOption(result.data);
        }
    });
}