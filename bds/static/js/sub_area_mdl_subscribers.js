$(document).ready(function(){

    var subscribers_selected = []

    var dtbl_mdl_subscribers = $('#tbl_mdl_subscribers').DataTable({
        ajax: {
            url: "/bds/api/dtbl/subscribers",
            data: function (d) {
                d.sub_area_id = OID
            }
        },
        pageLength: 10,
        ordering: false,
        columnDefs: [
            {
                'targets': 0,
                'searchable': false,
                'orderable': false,
                'width': '1%',
                'className': 'dt-body-center',
                'checkboxes': {
                    'selectRow': true
                }
            }
        ],
        select: {
            'style': 'multi'
        },
        order: [[1, 'asc']],
        'rowCallback': function (row, data, dataIndex) {
            // Get row ID
            var rowId = data[0];

            // If row ID is in the list of selected row IDs
            if ($.inArray(rowId, subscribers_selected) !== -1) {
                $(row).find('input[type="checkbox"]').prop('checked', true);
                $(row).addClass('selected');
            }
        }
    });

    // Handle click on checkbox
    $('#tbl_mdl_subscribers tbody').on('click', 'input[type="checkbox"]', function (e) {
        var $row = $(this).closest('tr');

        // Get row data
        var data = dtbl_mdl_subscribers.row($row).data();

        // Get row ID
        var rowId = data[0];

        // Determine whether row ID is in the list of selected row IDs
        var index = $.inArray(rowId, subscribers_selected);

        // If checkbox is checked and row ID is not in list of selected row IDs
        if (this.checked && index === -1) {
            subscribers_selected.push(rowId);

            // Otherwise, if checkbox is not checked and row ID is in list of selected row IDs
        } else if (!this.checked && index !== -1) {
            subscribers_selected.splice(index, 1);
        }

        if (this.checked) {
            $row.addClass('selected');
        } else {
            $row.removeClass('selected');
        }

        // Update state of "Select all" control
        updateDataTableSelectAllCtrl(dtbl_mdl_subscribers);

        // Prevent click event from propagating to parent
        e.stopPropagation();
    });


    // Handle click on table cells with checkboxes
    $('#tbl_mdl_subscribers').on('click', 'tbody td, thead th:first-child', function (e) {
        $(this).parent().find('input[type="checkbox"]').trigger('click');
    });


    // Handle click on "Select all" control
    $('thead input[type="checkbox"]', dtbl_mdl_subscribers.table().container()).on('click', function (e) {
        if (this.checked) {
            $('#tbl_mdl_subscribers tbody input[type="checkbox"]:not(:checked)').trigger('click');
        } else {
            $('#tbl_mdl_subscribers tbody input[type="checkbox"]:checked').trigger('click');
        }

        // Prevent click event from propagating to parent
        e.stopPropagation();
    });


    // Handle table draw event
    dtbl_mdl_subscribers.on('draw', function () {
        // Update state of "Select all" control
        updateDataTableSelectAllCtrl(dtbl_mdl_subscribers);
    });


    $("#btn_add_subscriber").click(function () {
        console.log(subscribers_selected);

        dtbl_mdl_subscribers.rows('.selected').data().each(function(value, index){

            var id = value[0];
            var contract_no = value[1];
            var fname = value[2];
            var lname = value[3];
            var address = value[4];

            var new_row = dtbl_inline_subscribers.row.add([
                id,
                contract_no,
                fname,
                lname,
                address
            ]);

            dtbl_inline_subscribers.row(new_row).draw();
            
        });

        dtbl_mdl_subscribers.rows('.selected').remove().draw();

        //     var selected_row = $(this).closest('tr');

        //     var id = dtbl_mdl_subscribers.row(selected_row).data()[0];
        //     var contract_no = dtbl_mdl_subscribers.row(selected_row).data()[1];
        //     var fname = dtbl_mdl_subscribers.row(selected_row).data()[2];
        //     var lname = dtbl_mdl_subscribers.row(selected_row).data()[3];
        //     var address = dtbl_mdl_subscribers.row(selected_row).data()[4];

        //     var row = dtbl_inline_subscribers.row.add([
        //         id,
        //         contract_no,
        //         fname,
        //         lname,
        //         address
        //     ]);

        //     dtbl_inline_subscribers.row(row).draw();
        //     dtbl_mdl_subscribers.row(selected_row).remove().draw();
        // });

    });


});