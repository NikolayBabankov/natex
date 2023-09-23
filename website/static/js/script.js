'use strict'

document.addEventListener('DOMContentLoaded', () => {

    

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

    // Календарь
    const options = {
        actions: {
            clickDay(event, dates) {
              if (dates.length != 0){
                showFreeEntrysInDay(dates);
              }
              else{
                return
                    // let today = new Date();
                    // showFreeEntrysInDay(today);
              }
            },
        },
        settings: {
          lang: 'ru-RU',
          range: {
            min: to_day,
            max: end_day,
            disabled: no_work_day,
          },
          visibility: {
            weekend: false,
            disabled: true,
            theme: 'light',
          },
        },
    };
    const calendar = new VanillaCalendar('#calendar', options);
    calendar.init();

    // Получение токена 
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
            }
        }
        }
        return cookieValue;
    }
    
    // Отправка Ajax на сервер
    const postData = async (url, data) => {
        let res = await fetch(url, {
        method: "POST",
        headers: {
        "X-Requested-With": "XMLHttpRequest",
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie('csrftoken'),
        },
        body: data
        });
        return await res.json();
    };

    // Показать свобоное время записи для определенного дня

    const ElTimeDay = document.querySelector('.js-time-day'),
          ElTimeMsg = document.querySelector('.js-time-msg'),
          ElTimeOverlay = document.querySelector('.js-time-overlay'),
          ElTimeList = document.querySelector('.js-time-list');


    // Отрисовка html свобоного времени для записи
    function renderFreeEntryDays(data){
        let freeEntry = data.data;
        ElTimeList.innerHTML = '';
        for ( let item in freeEntry) {
            let entryDiv = document.createElement('div');
            entryDiv.classList.add('tekhosmotr_entry_time_list_item', 'js-time-entry');
            addListenerEntryItem(entryDiv);
            entryDiv.setAttribute("data-entry-id", `${item}`);
            entryDiv.innerHTML = `${freeEntry[item]}`;
            ElTimeList.appendChild(entryDiv);
        }

    }

    function showErrorRenderFreeEntry(){
        ElTimeList.innerHTML = '';
        ElTimeMsg.innerHTML = 'Произошла ошибка, попробуйте перезагрузить страницу';
    }

    function showFreeEntrysInDay(date){
        let data = date[0];
        // Отображение даты в блоке со свободным временем
        let data_str = moment(date[0]).locale('ru').format('LL');
        ElTimeDay.innerHTML = '';
        ElTimeDay.innerHTML= `${data_str}`;
        ElTimeOverlay.classList.add('hidden_time');
        // Ajax запрос на сервер
        const formData = new FormData();
        formData.append('date', data);
        const json = JSON.stringify(Object.fromEntries(formData));
        postData(url_free_entry, json)
        .then(data => {
            if ('data' in data){
                renderFreeEntryDays(data);
                ElTimeOverlay.classList.remove('hidden_time');
            }
            else{
                showErrorRenderFreeEntry();
            }
        }).catch(() => {
            showErrorRenderFreeEntry();
        })
    }

    // Отправка записи Ajax

    const ElFormEntry = document.querySelector('.js-time-form');


    ElFormEntry.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(ElFormEntry);
        const entrySelectEl = document.querySelector('.select');
        if (entrySelectEl === null){
            return alert('Выберите время для записи')
        }
        formData.append('time', entrySelectEl.getAttribute('data-entry-id'));
        const json = JSON.stringify(Object.fromEntries(formData.entries()));
        postData(url_post_entry, json)
        .then(data => {
            console.log(data);
        //   if (data['status'] == 'Send'){
        //     RemoveActive();
        //     over.classList.add('active');
        //     appSuccesModal.classList.add('active');
        //   }
        //   else{
        //     AjaxErrorModal(formClickBuy, modalClick);
        //   }
        }).catch(() => {
            // AjaxErrorModal(formClickBuy, modalClick);
        })
    });



    // Онлайн запись

    const EntryListEl = document.querySelectorAll('.js-time-entry');

    function activeEntry(item){
        const NewEntryListEl = document.querySelectorAll('.js-time-entry');
        NewEntryListEl.forEach(function(item){
            if (item.classList.contains('select')){
                item.classList.remove('select');
            }
        });
        item.classList.add('select');
    }

    function addListenerEntryItem(item){
        item.addEventListener('click', () => {
            activeEntry(item);
        });
    }

    EntryListEl.forEach(function(item){
        addListenerEntryItem(item);
    });
});
