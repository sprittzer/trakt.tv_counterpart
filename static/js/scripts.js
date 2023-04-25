const icon = document.querySelector('.icon');
const search = document.querySelector('.search');

icon.onclick = function() {
    search.classList.toggle('active');
    if (icon.style.background == 'rgb(237, 28, 36)') {
        icon.style.background = 'none';
        icon.style.border = 'none'
    } else {
        icon.style.background = '#ed1c24';
        icon.style.border = '1px solid #ed1c24'
    }
};
// ---------------------------------------------------------------
const buttonElems = document.querySelectorAll('.btn-adding-to-list');
const btnClose = document.querySelector('.btn-close-modal-win');
const modalElem = document.querySelector('.modal');

modalElem.style.cssText = `
    display: flex;
    visibility: hidden;
    opacity: 0;
    transition: opacity 300ms ease-in-out;
`;

const closeModal = event => {
    const target = event.target;

    if (target === btnClose) {
        modalElem.style.opacity = 0;
        setTimeout(() => {
          modalElem.style.visibility = 'hidden';
        }, 300);
    }
}

const openModal = () => {
    modalElem.style.visibility = 'visible';
    modalElem.style.opacity = 1;
}

buttonElems.forEach(btn => {
    btn.addEventListener('click', openModal)
})
btnClose.addEventListener('click', closeModal)

// ------------------------------------------------
$(document).ready(function(){
    $('.btn-adding-to-list').click(function(event){
        event.preventDefault();
        var filmId = $(this).closest('.btn-adding-to-list').val();
        $.ajax({
            url: '/select_list',
            type: 'GET',
            contentType: 'application/json',
            success: function(data){
                var options_list = data.list;
                var radio_list = '';
                for (var i = 0; i < options_list.length; i++) {
                    radio_list += '<input type="checkbox" class="checkbox" name="list" value="' + options_list[i] + '">' + options_list[i] + '<br>';
                }
                radio_list += '<input type="hidden" name="filmId" value="' + filmId + '">';
                $('.list-content').html(radio_list);
            }
        });
    });
});
// ________________________________________________
$(document).ready(function() {
    $('.start-btn').click(function() {
        var checked_boxes = [];
        var filmId = $('input[name="filmId"]', '.list-content').val();
        $('.list-content input:checked').each(function() {
            checked_boxes.push($(this).val());
            var watchlist = $(this).val();
            $.ajax({
                type: 'POST',
                url: '/save_movie',
                data: {'watchlist': watchlist, 'filmId': filmId}
            })
        })
        if (checked_boxes.length === 1) {
            alert("Фильм добавлен в список");
        } else if (checked_boxes.length > 1) {
            alert('Фильм добавлен в списки')
        }
    });
});
// ________________________________________________
$(document).ready(function() {
    $('.add-to-history').click(function(event) {
        event.preventDefault();
        var dataToSend = $(this).closest('.add-to-history').val();
        $.ajax({
            url: '/watched',
            data: {'movie_id': dataToSend},
            type: 'POST', 
            success: function() {
                alert('Фильм добавлен в просмотренные');
            }
        })
    })
})
// ________________________________________________
$(document).ready(function() {
    $('.btn-recommendation').click(function(event) {
        event.preventDefault();
        var dataToSend = $(this).closest('.btn-recommendation').val();
        $.ajax({
            url: '/recommendation',
            data: {'movie_id': dataToSend},
            type: 'POST', 
            success: function() {
                alert('Фильм добавлен в ваши рекомендации');
            }
        })
    })
})