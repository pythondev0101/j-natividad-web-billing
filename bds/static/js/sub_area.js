$(document).ready(function(){

    var table_subscribers = $('#tbl_subscribers').DataTable({
    });
    var dtbl_subscribers = $("#tbl_subscribers_line").DataTable({
    });

    $("#btn_add_subscriber").click(function(){
        $("tr").each(function() {
            var check = $(this).find("input.chkbox").is(':checked');
            if(check){

                var id = $(this).find("td").eq(0).html();
                var fname = $(this).find("td").eq(2).html();
                var lname = $(this).find("td").eq(3).html();
                var address = $(this).find("td").eq(4).html();

                var row = dtbl_subscribers.row.add([
                    `<input name="subscribers[]" type="hidden" value="${id}">`,
                    `<input class="chkbox" type="checkbox">`,
                    fname,
                    lname,
                    address
                ]);

                dtbl_subscribers.row(row).column(0).nodes().to$().addClass('myHiddenColumn');
                dtbl_subscribers.row(row).draw();
                table_subscribers.row($(this)).remove().draw();
            }
        });
    });


    $("#btn_delete_subscriber").click(function(){
        $("#tbl_subscribers_line tr").each(function() {
            var check = $(this).find("input.chkbox").is(':checked');
            if (check){
        
                var row = table_subscribers.row.add([
                    $(this).find("input").eq(0).val(),
                    "<input class='chkbox' type='checkbox'>",
                    $(this).find("td").eq(2).html(),
                    $(this).find("td").eq(3).html(),
                    $(this).find("td").eq(4).html(),
                ]);
                table_subscribers.row(row).column(0).nodes().to$().addClass('myHiddenColumn');
                table_subscribers.row(row).draw();
                //$(this).remove();
                dtbl_subscribers.row($(this)).remove().draw();
            }
        });
    });

});