(function (doc, $) {

    'use strict';

    function initSliders() {
        var sliderSelector = '.g-slider';

        $(sliderSelector).slick({
            dots: true,
            customPaging : function(slider, i) {
                return '<button type="button" class="g-slider-dot"></button>';
            },
            prevArrow: '<button type="button" class="g-slider-button g-slider-prev"><img src="/img/slider-prev-icon.png"/></button>',
            nextArrow: '<button type="button" class="g-slider-button g-slider-next"><img src="/img/slider-next-icon.png"/></button>'
        });
    }

    function initParallaxBackgrounds() {
        var sectionElements = document.querySelectorAll('section.g-section.g-large.g-image-bg.g-parallax');

        console.log('initParallaxBackgrounds', sectionElements);

        if (!sectionElements) return;

        sectionElements = Array.prototype.slice.call(sectionElements);;

        renderBackgrounds();

        window.addEventListener('scroll', renderBackgrounds);
        window.addEventListener('resize', renderBackgrounds);

        function renderBackgrounds() {
            var windowScrollY = window.scrollY;

            sectionElements.forEach(function (element) {
                if (window.innerHeight === element.offsetHeight) {
                    var topPosition = element.offsetTop;
                    var parallaxY = (topPosition - windowScrollY) / 2;
    
                    element.style.backgroundPositionY = parallaxY + 'px';
                }
                else {
                    element.style.backgroundPositionY = '0px';
                }
            });
        }
    }

    if (document.readyState === 'complete' || document.readyState === 'loaded') {
        init();
    }
    else {
        doc.addEventListener('DOMContentLoaded', init, false);
    }

    function init() {
        initSliders();
        initParallaxBackgrounds();
        console.log('web_gerens.js: init done!');
    }

})(document, jQuery);
