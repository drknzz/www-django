/* toggle for delete button */
$(document).ready(function() {
    $('#id_delete').click(function(){
        $("#id_delete").toggleClass("deletion_active");
    });
});


/* decides what to do on a file click */
function fileClick(fileName) {
    if ($("#id_delete").hasClass("deletion_active"))
        deleteFile(fileName);
    else
        showFile(fileName);
}


/* displays file in code section */
function showFile(fileName) {
    $.ajax({
        url: location.origin + '/app/js/show_file/',
        data: {
            'name': fileName
        },
        dataType: 'json',
        success: function(data) {
            if (data.previous == "true")
                return;
            $("#code").text(data.content);
            $(".focus-elements").html("");
        }
    })
}


function deleteFile(fileName) {
    $.ajax({
        url: location.origin + '/app/js/delete_file/',
        data: {
            'name': fileName
        },
        dataType: 'json',
        success: function(data) {
            $(".file-selection").html(data.tree);
        }
    })
}


function deleteDirectory(dirName) {
    if (!($("#id_delete").hasClass("deletion_active")))
        return;

    $.ajax({
        url: location.origin + '/app/js/delete_directory/',
        data: {
            'name': dirName
        },
        dataType: 'json',
        success: function(data) {
            $(".file-selection").html(data.tree);
        }
    })
}


function toggleDisplay(id) {
    if ($('#' + id).css('display') == 'block')
        $('#' + id).css('display', 'none');
    else
        $('#' + id).css('display', 'block');
}


function compile() {
    $.ajax({
        url: location.origin + '/app/js/compile/',
        dataType: 'json',
        success: function(data) {
            $(".focus-elements").html(data.compile_result);
        }
    })
}