let num = $('.one_question').length;

$('#but_add').click(function(){
    num ++;
    var lastel = $('div[id^="id_question_"]:last');
    var newel = lastel.clone().prop('id', 'id_question_'+num );
    $(newel).insertAfter(lastel);

    h2 = $(`#id_question_${num} > h2`).html('');
    h2.append('<svg id="'+num+'" onclick="delQuestion('+num+')" style="color: red" height="21" viewBox="0 0 21 21" width="21" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" transform="translate(2 2)"><circle cx="8.5" cy="8.5" r="8"></circle><g transform="matrix(0 1 -1 0 17 0)"><path d="m5.5 11.5 6-6" fill="red"></path><path d="m5.5 5.5 6 6" fill="red"></path></g></g></svg> Question n°'+num);

    let svg = $(`#id_question_${num} > h2 > svg`).attr("id", "id_cross_"+num);

    let select = $(`#id_question_${num} > #id_fields > .input_div > select`).attr({"id": "id_type_question_"+num, "name": "type_question_"+num, "onchange": "addAnswer('id_type_question_"+num+"')"});
    select.val("Réponse libre");

    let reponses = $("#id_question_"+num+" > .reponses");
    reponses.empty();
    reponses.attr({"id": "id_reponses_"+num});

    let input = $(`#id_question_${num} > #id_fields > .input_div > #id_title_${num-1}`).attr({"id": "id_title_"+num, "name": "title_"+num});
    input.val('');
    let input3 = $(`#id_question_${num} > #id_fields > .input_div >  #id_point_${num-1}`).attr({"id": "id_point_"+num, "name": "point_"+num});
    input3.val('');
});