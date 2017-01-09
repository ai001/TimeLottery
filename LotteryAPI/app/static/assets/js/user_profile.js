$(function(){
    $('.edit').click(function(){
        //console.log("Edit Clicked");
        $(this).off("click");
        $(this).css('cursor', 'default');
        //$(this).parent().parent().css("display", "none");
        //console.log($(this).parent().parent().parent().children("div#persinfo_edit").html());
        $(this).parent().parent().parent().children("div#edit_form").css("display","");
        $(this).parent().parent().parent().children("div#field_div").css("display","");
        $(this).parent().parent().parent().children("div#readonly_div").css("display","none");
        $(this).parent().parent().parent().children("div#ro_info").css("display","none");
        $("#save").removeAttr("disabled");

        //$(this).parent().children("input").off('click');
        //$(this).parent().children("input").prop('readonly', false);
        //$(this).parent().children("select").prop('disabled', false);
        //$(this).parent().children("input").css('background-color', '#fff');
        //$(this).parent().children("select").css('background-color', '#fff');
        //$(this).parent().children("input").css('border', '1px solid #ccc');
        //$(this).parent().children("select").css('border', '1px solid #ccc');
        //$(this).parent().children("input").css('border-radius', '4px');
        //$(this).parent().children("select").css('border-radius', '4px');
        //$(this).parent().children("input").css('box-shadow', 'inset 0 1px 1px rgba(0,0,0,.075);');
        //$(this).parent().children("select").css('box-shadow', 'inset 0 1px 1px rgba(0,0,0,.075);');
        //$(this).parent().children("input").css('box-sizing', 'border-box;');
        //$(this).parent().children("select").css('box-sizing', 'border-box;');
    });
});
