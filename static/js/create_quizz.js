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

    let reponses = $("#id_question_"+num+" > .reponses");
    reponses.empty();
    reponses.attr({"id": "id_reponses_"+num});

    let input = $(`#id_question_${num} > #id_fields > .input_div > #id_title_1`).attr({"id": "id_title_"+num, "name": "title_"+num});
    input.val('');
    let input2 = $(`#id_question_${num} > #id_fields > .input_div >  #id_description_1`).attr({"id": "id_description_"+num, "name": "description_"+num});
    input2.val('');
    let input3 = $(`#id_question_${num} > #id_fields > .input_div >  #id_point_1`).attr({"id": "id_point_"+num, "name": "point_"+num});
    input3.val('');
});

function delQuestion(param){
    $("#id_question_"+param).remove();
}

function delAnswer(id_answer, id){
console.log(id_answer, id);
    $("#id_reponses_"+id+" > div[name='answer_"+id_answer+"']").remove();
}

function addAnswer(id_s){
    let id = id_s.replace(/[^\d.]/g, "")
    $("#id_reponses_"+id).empty();
    switch ($("#"+id_s).val()){
        case "Choix multiple":
            $("#id_reponses_"+id).append('Points / Réponse :<div class="input_div" name="answer_1"><label for="id_q_'+id+'_answer_1">'+getPourcentages(id, id_s)+'</label><input type="text" id="id_q_'+id+'_answer_1" name="q_'+id+'_answer_1" style="width: 90%;" required></div><button id="id_but_add_answer_'+id+'" type="button" onclick="addOneAnswer('+id+')">Ajouter une réponse</button>');
            break;
        case "Choix unique":
            $("#id_reponses_"+id).append('<div class="input_div" name="answer_1"><label for="id_q_'+id+'_answer_1">Bonne réponse :</label><input type="text" id="id_q_'+id+'_answer_1" name="q_'+id+'_answer_1" required></div><button id="id_but_add_answer_'+id+'" type="button" onclick="addOneUniqueAnswer('+id+')">Ajouter une réponse fausse</button>');
            break;
        case "Vrai/Faux":
            $("#id_reponses_"+id).append('<div class="input_div" name="answer_1"><label for="id_q_'+id+'_answer_1">Bonne réponse :</label><select id="id_q_'+id+'_answer_1" name="q_'+id+'_answer_1" required><option value="True">Vrai</option><option value="False">Faux</option></select></div>');
            break;

    }
}

function addOneAnswer(id){
    let id_answer = parseInt($("#id_but_add_answer_"+id).prev().attr('name').replace(/[^\d.]/g, ""))+1;
    $("#id_but_add_answer_"+id).before('<div class="input_div" name="answer_'+id_answer+'"><svg id="id_cross_'+id+'_'+id_answer+'" onclick="delAnswer('+id_answer+','+id+')" style="color: red" height="21" viewBox="0 0 21 21" width="21" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" transform="translate(2 2)"><circle cx="8.5" cy="8.5" r="8"></circle><g transform="matrix(0 1 -1 0 17 0)"><path d="m5.5 11.5 6-6" fill="red"></path><path d="m5.5 5.5 6 6" fill="red"></path></g></g></svg><label for="id_q_'+id+'_answer_'+id_answer+'">'+getPourcentages(id, id_answer)+'</label><input type="text" id="id_q_'+id+'_answer_'+id_answer+'" name="q_'+id+'_answer_'+id_answer+'" style="width: 90%;" required></div>');
}

function addOneUniqueAnswer(id){
    let id_answer = parseInt($("#id_but_add_answer_"+id).prev().attr('name').replace(/[^\d.]/g, ""))+1;
    $("#id_but_add_answer_"+id).before('<div class="input_div" name="answer_'+id_answer+'"><svg id="id_cross_'+id+'_'+id_answer+'" onclick="delAnswer('+id_answer+','+id+')" style="color: red" height="21" viewBox="0 0 21 21" width="21" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" transform="translate(2 2)"><circle cx="8.5" cy="8.5" r="8"></circle><g transform="matrix(0 1 -1 0 17 0)"><path d="m5.5 11.5 6-6" fill="red"></path><path d="m5.5 5.5 6 6" fill="red"></path></g></g></svg><input type="text" id="id_q_'+id+'_answer_'+id_answer+'" name="q_'+id+'_answer_'+id_answer+'" style="width: 98%;" required></div>');
}

function getPourcentages(id, id_answer){
    let returnedStr = '<select style="width: 8%;" id="id_point_'+id+'_answer_'+id_answer+'" name="point_'+id+'_answer_'+id_answer+'" required>';
    for(var i=-10; i < 11; i++){
        if(i==0){
            returnedStr += "<option value=0 selected='selected'>0%</option>";
        }else{
            returnedStr += "<option value="+1/i+">"+Math.round(1/i*10000, 2)/100+"%</option>";
        }
    }
    returnedStr += "</select>"
    return returnedStr;
}