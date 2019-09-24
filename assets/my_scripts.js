function setBannerStyle() {
    var w = $(window).width();
    var width_param = 1600 / w;
    var height_param = w / 1600;
    var scale_param = w / 1600;
    if (w > 1600) {
        width_param = 1;
        height_param = 1;
        scale_param = 1;
    }

    $(".HomeBanner").css({ "width": Math.floor(width_param * 100).toString() + "%", "transform": "scale(" + scale_param.toString() + ")" });
}

function moveUp() {
    var w = $(window).width();
    if (w < 400) { w = 400 };
    if (w > 1600) { w = 1600 };
    var value = 550 * ((w-400)/1200) + 200;
    $(".ifwrap").css({ "height": value+"px"});
}

$(window).resize(function() {
    setBannerStyle();
    moveUp();
});
