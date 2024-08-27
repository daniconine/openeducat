(function (doc, $) {

    'use strict';

    function initSliders() {
        var odooEditor = doc.querySelector('.o_action_manager');
        if (odooEditor) return;
        
        var sliderSelector = '.g-slider';

        $(sliderSelector).slick({
            dots: true,
            customPaging : function(slider, i) {
                return '<button type="button" class="g-slider-dot"></button>';
            },
            prevArrow: '<button type="button" class="g-slider-button g-slider-prev"><img src="/web_design/static/src/img/web_new/slider-prev-icon.png"/></button>',
            nextArrow: '<button type="button" class="g-slider-button g-slider-next"><img src="/web_design/static/src/img/web_new/slider-next-icon.png"/></button>'
        });
    }

    function initParallaxBackgrounds() {
        var scrollableElementOptionSelectorList = ['#wrapwrap', 'main', 'body'];
        var sectionElements = document.querySelectorAll('section.g-section.g-large.g-image-bg.g-parallax');
        var scrollableElement = null;

        for (var i = 0; i < scrollableElementOptionSelectorList.length; i++) {
            var newScrollableElement = document.querySelector(scrollableElementOptionSelectorList[i]);

            if (newScrollableElement) {
                scrollableElement = newScrollableElement;
                break;
            }
        }

        if (!sectionElements) return;
        
        sectionElements = Array.prototype.slice.call(sectionElements);

        renderBackgrounds();

        scrollableElement.addEventListener('scroll', renderBackgrounds);
        window.addEventListener('resize', renderBackgrounds);

        function renderBackgrounds() {
            var currentScrollY = scrollableElement ? scrollableElement.scrollTop : window.scrollY;

            sectionElements.forEach(function (element) {
                if (window.innerHeight === element.offsetHeight) {
                    var topPosition = element.offsetTop;
                    var parallaxY = (topPosition - currentScrollY) / 2;
    
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
