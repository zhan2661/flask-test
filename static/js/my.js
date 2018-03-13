
function car(){
$('.carousel').carousel({
            interval:10000,
        })

}
$(car);
function roll(){
$('a[href^="#"]').on('click', function(event) {
    var target = $(this.getAttribute('href'));
    if( target.length ) {
        event.preventDefault();
        $('html, body').stop().animate({
            scrollTop: target.offset().top
        }, 1000);
    }
});
}
$(roll);
function nav(){
var scrolling = false;
$(window).on('scroll', function(){
	if( !scrolling ) {
		scrolling = true;
		(!window.requestAnimationFrame)
			? setTimeout(autoHideHeader, 250)
			: requestAnimationFrame(autoHideHeader);
	}
});
}
$(nav);


function toTop(){
$(window).scroll(function() {
    if ($(this).scrollTop() > 50 ) {
        $('.scrolltop:hidden').stop(true, true).fadeIn();
    } else {
        $('.scrolltop').stop(true, true).fadeOut();
    }
});
$(function(){$(".scroll").click(function(){$("html,body").animate({scrollTop:$("#intro").offset().top},"100");return false})})
}

$(toTop);

function wa(){
        new WOW().init();

}

$(wa);
