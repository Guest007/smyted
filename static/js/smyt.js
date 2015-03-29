
var maxInt = 2147483647;
if( maxInt > Number.MAX_VALUE ) { maxInt = Number.MAX_VALUE; }
var minInt = (-1)*maxInt - 1;
// Models config
var cfgData = null;
// Current selected model
var currentModel = null;
// re for int check
var intRegex = /^\-?\d+$/;

var tmpDate = null;
var dateSelected = false;

// add csrf token on every jQuery POST ajax request
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$.ajaxPrefilter(function(options, originalOptions, jqXHR){
    if (options['type'].toLowerCase() === "post") {
        jqXHR.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    }
});


// Send new object model's creation form
var submitForm = function(e) {
    $('.err').hide();
    var valid = true;
    for (var k=0; k < cfgData[currentModel]['fields'].length; k++) {
        var field_id = cfgData[currentModel]['fields'][k]['id'];
        if( !cellIsValid(cfgData[currentModel]['fields'][k]['type'], $('#newobj_'+field_id).val()) ) {
            valid = false;
            $('#newobj_'+field_id+'_err').show();
        }
    }
    if( valid ) {
        $.ajax({
            type: 'POST',
            url: '/obj_create/'+currentModel+'/',
            data: $("#new_obj_form").serialize(),
            success: function(data) {
                $("#new_obj_form")[0].reset();
                loadModels(currentModel);
            },
            error: function(data) {
                alert('Ошибка создания нового объекта модели ' + currentModel);
            }
        });
    }
};

// Make new object model's creation form
var drawForm = function(model) {
    formData = '<center><b>Создать новый объект</b></center><form id="new_obj_form" action="/obj_create/'+model+'/" method="post">';
    for (var k=0; k < cfgData[model]['fields'].length; k++) {
        var field_id = cfgData[model]['fields'][k]['id'];
        var field_type = cfgData[model]['fields'][k]['type'];
        if ( field_type == 'date' ) {
            formData += '<BR>'+cfgData[model]['fields'][k]['title']+':<input class="date-picker" id="newobj_'+field_id+'" type="text" name="'+field_id+'" value="">';
        } else if ( field_type == 'int' ) {
            formData += '<BR>'+cfgData[model]['fields'][k]['title']+':<input id="newobj_'+field_id+'" type="text" name="'+field_id+'" value="">';
            formData += '<label class="err" id="newobj_'+field_id+'_err" style="display: none">Введите числовое значение</label>';
        } else {
            formData += '<BR>'+cfgData[model]['fields'][k]['title']+':<input id="newobj_'+field_id+'" type="text" name="'+field_id+'" value="">';
        }
    }
    formData += '<BR><BR><input type="button" value="Создать" onClick="submitForm()"></form>';
    return formData;
};

// Check type of changed cell
var getClickedType = function(cell) {
    var col = cell.parent().children().index(cell);
    console.log(cfgData[currentModel]['fields'][col-1]['type']);
    return cfgData[currentModel]['fields'][col-1]['type'];
};

// Send changes
var updateCell = function(cell, oldValue) {
    var col = cell.parent().children().index(cell);
    var objid = cell.parent().children('td:first').text();
    var field = cfgData[currentModel]['fields'][col-1]['id'];
    var type = cfgData[currentModel]['fields'][col-1]['type'];
    var value = '';
    if( type == 'date' ) {
        value = cell.children()[0].value;
    } else {
        value = cell.text();
    }

    // Refresh object's field
    $.ajax({
        type: 'POST',
        url: '/obj_update/'+currentModel+'/',
        data: {
            objid: objid,
            field: field,
            value: value
        },
        success: function(data) {
        },
        error: function(data) {
            cell.html(oldValue);
            cell.focus();
        }
    });
};

var validateInt = function(v) {
    var x = parseInt(v);
    return (intRegex.test(v) && (x <= maxInt) && (x >= minInt));
};

var cellIsValid = function(cType, cData) {
    if( cType == 'int' ) {
        return validateInt(cData);
    } else { return true }
};

// Check if content is changed
var checkOnChange = function() {
    $('body')
        .on('focus', '[contenteditable]', function() {
            console.log(data);
            $(this).data('before', $(this).html());
        })
        .on('blur', '[contenteditable]', function() {
            // changed
            if ($(this).data('before') !== $(this).html()) {
                var cellType = getClickedType($(this));
                if( cellIsValid(cellType, $(this).html()) ) {
                    updateCell($(this), $(this).data('before'));
                } else {
                    $(this).html($(this).data('before'));
                    $(this).focus();
                }
            }
        });
};

// Objects load(json)
// @param model: Model's ID (string)
var loadModels = function(model) {
    $('#tabcontent').html("");
    $("#divform_new_obj").html("");
    currentModel = model;
    $.ajax({
        type: "GET",
        url: "/json_obj/"+model,

        // Make table with data
        success: function(data) {

            if( data.length == 0 ) {
                $('#tabcontent').hide();
            } else {
                $('#tabcontent').show();
            }

            var tabHeader = '<thead><tr><th><b>ID</b></th>';
            for (var i=0; i < cfgData[model]['fields'].length; i++) {
                tabHeader += '<th>'+cfgData[model]['fields'][i]['title']+'</th>';
            }
            tabHeader += '</tr></thead>';

            var tabBody = '<tbody>';
            for (var i=0; i < data.length; i++) {
                tabBody += '<tr><td>'+data[i]['pk']+'</td>';
                for (var k=0; k < cfgData[model]['fields'].length; k++) {
                    if(cfgData[model]['fields'][k]['type'] != 'date') {
                        tabBody += '<td contenteditable="true">'+data[i]['fields'][cfgData[model]['fields'][k]['id']]+'</td>';
                    } else {
                        tabBody += '<td><input id="'+data[i]['pk']+'_'+k+'" class="date-picker date-cell" value="'+data[i]['fields'][cfgData[model]['fields'][k]['id']]+'"></td>';
                    }
                }
                tabBody +='</tr>';
            }
            tabBody += '</tbody>';
            // refresh table
            $('#tabcontent').html(tabHeader+tabBody);
            $("#divform_new_obj").html(drawForm(model));
            $("#divform_new_obj").css('display', 'inline-block');
            // block changing cell with date
            $('.date-picker').keydown(function(){return false;});
            $('.date-picker').bind("cut paste", function(e){ e.preventDefault(); });
            var $datepicker = $('.date-picker').pikaday({
                format: 'YYYY-MM-DD',
                onOpen: function() {
                    tmpDate = this.getMoment().format('YYYY-MM-DD');
                    dateSelected = false
                },
                onSelect: function() {
                    dateSelected = true
                },
                onClose: function() {
                    // date field was changed
                    if(dateSelected && tmpDate !== this.getMoment().format('YYYY-MM-DD')) {
                        var id = this._o.field.getAttribute('id');
                        if(id.substr(0,3) !== 'new') {
                            updateCell($('#'+id).parent(), tmpDate);
                        }
                    }
                }
            });
        },
        error: function(data) {
            alert('Ошибка загрузки объектов модели '+model);
        }
    });
};

// Load models in json and make menu
$( document ).ready(function() {

    checkOnChange();
    $.ajax({
        type: "GET",
        url: "/json_cls/",
        //
        success: function(data) {
            cfgData = data;
            var modList = $('<ul/>');

            for(model in data) {
                var li = $('<li/>')
                    .appendTo(modList);
                var a = $('<a/>')
                    .text(data[model]['title'])
                    .attr("id", model)
                    .attr("href", "#")
                    .appendTo(li);
            }
            $('#menu').html(modList.html());
            $('a').click(function() {
                loadModels($(this).attr('id'));
            });
        },
        error: function(data) {
            alert('Ошибка загрузки конфигурации моделей');
        }

    });

});

