$(document).ready(function(){

    var table_messengers = $('#tbl_messengers').DataTable({
    });
    var dtbl_messengers = $("#tbl_messengers_line").DataTable({
        "dom": 'rtip'
    });


    $("#btn_add_messenger").click(function(){
        $("tr").each(function() {
            var check = $(this).find("input.chkbox").is(':checked');
            if(check){

                var id = $(this).find("td").eq(0).html();
                var fname = $(this).find("td").eq(2).html();
                var lname = $(this).find("td").eq(3).html();
                var username = $(this).find("td").eq(4).html();

                var row = dtbl_messengers.row.add([
                    `<input name="messengers[]" type="hidden" value="${id}">`,
                    `<input class="chkbox" type="checkbox">`,
                    fname,
                    lname,
                    username
                ]);  

                dtbl_messengers.row(row).column(0).nodes().to$().addClass('myHiddenColumn');
                dtbl_messengers.row(row).draw();
                table_messengers.row($(this)).remove().draw();
            }
        });
    });


    $("#btn_delete_messenger").click(function(){
        $("#tbl_messengers_line tr").each(function() {
            var check = $(this).find("input.chkbox").is(':checked');
            if (check){
        
                var row = table_messengers.row.add([
                    $(this).find("input").eq(0).val(),
                    "<input class='chkbox' type='checkbox'>",
                    $(this).find("td").eq(2).html(),
                    $(this).find("td").eq(3).html(),
                    $(this).find("td").eq(4).html()
                ]);
                table_messengers.row(row).column(0).nodes().to$().addClass('myHiddenColumn');
                table_messengers.row(row).draw();
                dtbl_messengers.row($(this)).remove().draw();
            }
        });
    });

});