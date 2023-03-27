let num = 1;

$('#but_add').click(function(){
    num ++;
    var lastel = $('div[id^="id_question_"]:last');
    var newel = lastel.clone().prop('id', 'id_question_'+num );
    $(newel).insertAfter(lastel);

    h2 = $(`#id_question_${num} > h2`).html('');
    h2.append('<svg id="'+num+'" onclick="delQuestion('+num+')" style="color: red" height="21" viewBox="0 0 21 21" width="21" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" transform="translate(2 2)"><circle cx="8.5" cy="8.5" r="8"></circle><g transform="matrix(0 1 -1 0 17 0)"><path d="m5.5 11.5 6-6" fill="red"></path><path d="m5.5 5.5 6 6" fill="red"></path></g></g></svg> Question n°'+num);

    let svg = $(`#id_question_${num} > h2 > svg`).attr("id", "id_cross_"+num);

    let select = $(`#id_question_${num} > #id_fields > .input_div > select`);
    select.attr("id", "id_select_type_question_"+num);
    select.attr("onchange", "addAnswer('id_select_type_question_"+num+"')");

    let input = $(`#id_question_${num} > #id_fields > .input_div > #id_title_1`).attr({"id": "id_title_"+num, "name": "title_"+num});
    let input2 = $(`#id_question_${num} > #id_fields > .input_div >  #id_description_1`).attr({"id": "id_description_"+num, "name": "description_"+num});

});

function delQuestion(param){
    $("#id_question_"+param).remove();
}

function addAnswer(id){
    if($("#"+id).val() == "Choix multiple"){
        console.log("Ajout reponses multiples");
    }else{
        if($("#"+id).val() == "Choix unique"){
            console.log("Ajout reponses unique");
        }
    }
}


