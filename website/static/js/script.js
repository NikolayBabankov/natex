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

    const screenWidth = window.screen.width;
    if (screenWidth > 991){
        ElMenuService.addEventListener('mouseover', () => {
            showSub(ElMenuService);
        });
        ElMenuService.addEventListener('mouseleave', () => {
            hideSub(ElMenuService);
        });
    }

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
    const ElTekhosmotr = document.querySelector('.js-tekhosmotr');
    if (ElTekhosmotr){
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
    }


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



    // Отображение удачной записи на ТО
    function renderSuccessEntry(data){
        showAndHideLoading(false);
        Overlay.classList.add('active');
        let dataEntry = data.data
        let ModalMsgEl = ModalMsg.querySelector('.modal_msg_text');
        let dayFormatStr = moment(dataEntry['day']).locale('ru').format('LL');
        ModalMsgEl.innerHTML = '';
        ModalMsgEl.innerHTML = `
            <div class="modal_msg_title">
                Вы успешно записаны на техосмотр!
            </div>
            <div class="modal_msg_date">
                Номер заявки: ${dataEntry['id']}
            </div>
            <div class="modal_msg_date">
                Дата: ${dayFormatStr} Время: ${dataEntry['time']}
            </div>
            <ul class="modal_msg_list">
                <li class="modal_msg_list_item">
                    ФИО: ${dataEntry['name']}
                </li>
                <li class="modal_msg_list_item">
                    Телефон: ${dataEntry['phone']}
                </li>
                <li class="modal_msg_list_item">
                    Марка и модель ТС: ${dataEntry['automobile']}
                </li>
                <li class="modal_msg_list_item">
                    Год выпуска: ${dataEntry['year']}
                </li>
                <li class="modal_msg_list_item">
                    Гос. регистрационный знак: ${dataEntry['number']}
                </li>
            </ul>
        `;
        ModalMsg.classList.add('active');
    }

    // Отображение что запись уже занята
    function showReserveEntry(){
        showAndHideLoading(false);
        Overlay.classList.add('active');
        let ModalMsgEl = ModalMsg.querySelector('.modal_msg_text');
        ModalMsgEl.innerHTML = '';
        ModalMsgEl.innerHTML = `
        <div class="modal_msg_msg">
            Это время уже занято <br>
            перезагрузите страницу и выберите другое время!
        </div>`;
        ModalMsg.classList.add('active');
    }


        // Отображение что запись уже занята
    function showErorrEntry(){
        showAndHideLoading(false);
        Overlay.classList.add('active');
        let ModalMsgEl = ModalMsg.querySelector('.modal_msg_text');
        ModalMsgEl.innerHTML = '';
        ModalMsgEl.innerHTML = `
        <div class="modal_msg_msg">
            Произошла ошибка <br>
            попробуйте перезагрузить страницу!
        </div>`;
        ModalMsg.classList.add('active');
    }

    // Отправка записи на ТО по Ajax
    const ElFormEntry = document.querySelector('.js-time-form');

    if (ElFormEntry){

        // Форма записи на ТО
        ElFormEntry.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(ElFormEntry);
            const entrySelectEl = document.querySelector('.select');
            if (entrySelectEl === null){
                return alert('Выберите время для записи');
            }
            formData.append('time', entrySelectEl.getAttribute('data-entry-id'));
            const json = JSON.stringify(Object.fromEntries(formData.entries()));
            showAndHideLoading(true);
            postData(url_post_entry, json)
            .then(data => {
                if ('data' in data){
                    renderSuccessEntry(data);
                    ElFormEntry.reset();
                    delSelcetEntry()
                }
                else if (data['status'] = 'Reserve'){
                    showReserveEntry();
                    ElFormEntry.reset();
                    delSelcetEntry()
                }
                else{
                    showErorrEntry();
                    ElFormEntry.reset();
                    delSelcetEntry()
                }
            }).catch(() => {
                showErorrEntry();
                ElFormEntry.reset();
                delSelcetEntry();
            })
        });
        // Удалить кнопку записи на ТО на странице ТО
        const ElBtnBottom = document.querySelector('.js-bottom-btn');
        ElBtnBottom.style.display = 'none';
    }



    // Модальные окна

    const Overlay = document.querySelector('.js-overlay'),
          Modal = document.querySelector('.js-modal'),
          ModalMsg = document.querySelector('.js-modal-msg'),
          Spinner = document.querySelector('.js-spinner'),
          BtnsOpenModal = document.querySelectorAll('.js-modal-btn'),
          BtnsCloseModal = document.querySelectorAll('.js-modal-close');

    // Показать или скрыть экран ожидание при записи
    function showAndHideLoading(parametr){
        if (parametr){
            Overlay.classList.add('load');
            Spinner.classList.add('load');
        }
        else{
            Overlay.classList.remove('load');
            Spinner.classList.remove('load');
        }
    }   

    // Удалить active у всех элементов
    function closeModalBlock(){
        const elInActiveList = document.querySelectorAll('.active');
        elInActiveList.forEach(function(item) {
            item.classList.remove('active')
        });
    }
    
    // Открыть модальное окно при нажатие на обратный звонок
    BtnsOpenModal.forEach(function(item) {
        item.addEventListener('click', function(event) {
            Overlay.classList.add('active');
            Modal.classList.add('active');
        });
    });
    
    // Удалить active у всех элементов при нажатии на overlay
    Overlay.addEventListener('click', () => {
        closeModalBlock();
    });
    
     // Удалить active у всех элементов при нажатии на крестик
    BtnsCloseModal.forEach(function(item) {
        item.addEventListener('click', () => {
            closeModalBlock();
        });
    });
    
     // Удалить active у всех элементов при нажатии на Ecs
    document.body.addEventListener('keyup', function (e) {
        var key = e.keyCode;
        if (key == 27) {
            closeModalBlock();
        };
    }, false);


    // Онлайн запись

    const EntryListEl = document.querySelectorAll('.js-time-entry');


    function delSelcetEntry(){
        const NewEntryListEl = document.querySelectorAll('.js-time-entry');
        NewEntryListEl.forEach(function(item){
            if (item.classList.contains('select')){
                item.classList.remove('select');
            }
        });
    }

    function activeEntry(item){
        delSelcetEntry();
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


    // Скрол к блокам на странице товаров по id
    const ElBtnScrollProduct = document.querySelectorAll('.js-block-scroll');

    function scrollToBlock(el){
        el.addEventListener('click', function(e) {
            e.preventDefault();
            let href = this.getAttribute('href').substring(1);
            const scrollTarget = document.getElementById(href);
            const topOffset = 100; // если не нужен отступ сверху 
            const elementPosition = scrollTarget.getBoundingClientRect().top;
            const offsetPosition = elementPosition - topOffset;
        
            window.scrollBy({
                top: offsetPosition,
                behavior: 'smooth'
            });
         });
    }

    ElBtnScrollProduct.forEach(item => {
        scrollToBlock(item);
    });


    function maskPhone(selector, masked = '+7 (___) ___-__-__') {
        const elems = document.querySelectorAll(selector);
    
        function mask(event) {
            const keyCode = event.keyCode;
            const template = masked,
                def = template.replace(/\D/g, ""),
                val = this.value.replace(/\D/g, "");
            let i = 0,
                newValue = template.replace(/[_\d]/g, function (a) {
                    return i < val.length ? val.charAt(i++) || def.charAt(i) : a;
                });
            i = newValue.indexOf("_");
            if (i !== -1) {
                newValue = newValue.slice(0, i);
            }
            let reg = template.substr(0, this.value.length).replace(/_+/g,
                function (a) {
                    return "\\d{1," + a.length + "}";
                }).replace(/[+()]/g, "\\$&");
            reg = new RegExp("^" + reg + "$");
            if (!reg.test(this.value) || this.value.length < 5 || keyCode > 47 && keyCode < 58) {
                this.value = newValue;
            }
            if (event.type === "blur" && this.value.length < 5) {
                this.value = "";
            }
    
        }
    
        for (const elem of elems) {
            elem.addEventListener("input", mask);
            elem.addEventListener("focus", mask);
            elem.addEventListener("blur", mask);
        }
        
    }

    maskPhone('.js-mask-phone');

    // Отправка заявки
    const ElModalForm = document.querySelector('.js-modal-form');
    ElModalForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(ElModalForm);
        const json = JSON.stringify(Object.fromEntries(formData.entries()));
        postData(url_lead, json)
        .then(data => {
            if (data['status'] === 'Send'){
                window.location.href = url_success_lead;
            }
            else{
                ElModalForm.reset();
                alert('Произошла ошибка, попробуйте еще раз');
            }
        }).catch(() => {
            ElModalForm.reset();
            alert('Произошла ошибка, попробуйте еще раз');
        })
    });

    // Мобильное меню
    const ELMobileMenu = document.querySelector('.js-menu'),
          ElMobileBtnMenu = document.querySelector('.js-menu-btn');

    ElMobileBtnMenu.addEventListener('click', function(e) {
        if (ElMobileBtnMenu.classList.contains('is-active')){
            ElMobileBtnMenu.classList.remove('is-active');
            ELMobileMenu.classList.remove('menu_view');
        }
        else{
            ElMobileBtnMenu.classList.add('is-active');
            ELMobileMenu.classList.add('menu_view');
        }
    });

});
