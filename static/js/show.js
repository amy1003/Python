/**
 * Created by huangdaye on 2017/12/26.
 */

$(function () {

    //隔行变色
    $(".tr:odd").css("background-color","#E6E6FA");

    //点击班级图表事件
    $("#class").click(function () {
        window.location.href="/student/class_chart";
    });

    //点击学历图表事件
    $('#academic').click(function () {
        window.location.href='/student/academic_chart';
    });
});