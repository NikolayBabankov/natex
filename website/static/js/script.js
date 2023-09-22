'use strict'


const swiper = new Swiper(".mySwiper", {
    slidesPerView: 1,
    pagination: {
        el: ".swiper-pagination",
    },
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
});

// Показывать-скрывать меню
const ElMenuService = document.querySelector('.js-menu-services');

function showSub(item){
    const child = item.querySelector('.menu_item_sub');
    child.classList.add('menu_item_sub_show');
  }
  
  function hideSub(item){
    const child = item.querySelector('.menu_item_sub');
    child.classList.remove('menu_item_sub_show');
}

ElMenuService.addEventListener('mouseover', () => {
    showSub(ElMenuService);
});
ElMenuService.addEventListener('mouseleave', () => {
    hideSub(ElMenuService);
});

const ElListLinkSidebar = document.querySelectorAll('.js-sidebar-link');

function shineLinks(item){
    let url=document.location.href;
    let urlKLink = item.href
    if (url==urlKLink){
        item.classList.add('service_link_active');
    };
};

ElListLinkSidebar.forEach(function(item){
    shineLinks(item);
});