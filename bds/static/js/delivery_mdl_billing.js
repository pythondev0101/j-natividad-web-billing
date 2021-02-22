$(document).ready(function(){

    var dtbl_billings = $("#tbl_mdl_billings").DataTable({
        pageLength: 10,
        columnDefs: [
            {
                "targets": 0,
                "visible": false,
            },
            {
                "targets": 1,
                "render": function(data, type, row){
                    if (!(data)){
                        return `<div class="mb-2 mr-2 badge badge-pill badge-secondary">INACTIVE</div>`;
                    }
                    
                    return `<div class="mb-2 mr-2 badge badge-pill badge-success">ACTIVE</div>`;

                    
                }
            }
        ],
        ajax: {
            url: "/bds/api/dtbl/billings",
        }
    });

    $('#tbl_mdl_billings tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            dtbl_billings.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );


    $('#btn_confirm_billing').click( function () {
        var selected_billing = dtbl_billings.row('.selected').data();

        localStorage.setItem('billingID', selected_billing[0]);

        $("#billing_no").val(selected_billing[1]);
        $("#name").val(selected_billing[2]);
        $("#date_from").val(selected_billing[3]);
        $("#date_to").val(selected_billing[4]);

        location.reload();

    } );
});