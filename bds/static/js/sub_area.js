//
// Updates "Select all" control in a data table
//

var dtbl_inline_subscribers;

function updateDataTableSelectAllCtrl(table) {
    var $table = table.table().node();
    var $chkbox_all = $('tbody input[type="checkbox"]', $table);
    var $chkbox_checked = $('tbody input[type="checkbox"]:checked', $table);
    var chkbox_select_all = $('thead input[type="checkbox"]', $table).get(0);

    // If none of the checkboxes are checked
    if ($chkbox_checked.length === 0) {
        chkbox_select_all.checked = false;
        if ('indeterminate' in chkbox_select_all) {
            chkbox_select_all.indeterminate = false;
        }

        // If all of the checkboxes are checked
    } else if ($chkbox_checked.length === $chkbox_all.length) {
        chkbox_select_all.checked = true;
        if ('indeterminate' in chkbox_select_all) {
            chkbox_select_all.indeterminate = false;
        }

        // If some of the checkboxes are checked
    } else {
        chkbox_select_all.checked = true;
        if ('indeterminate' in chkbox_select_all) {
            chkbox_select_all.indeterminate = true;
        }
    }
}


$(document).ready(function () {

    var rows_selected = [];

    dtbl_inline_subscribers = $("#tbl_inline_subscribers").DataTable({
        ajax: {
            url: "/bds/api/sub-areas/" + OID + "/subscribers",
            data: function (d) {
                d.column_order = "inline",
                d.client_side = true
            }
        },
        pageLength: 10,
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
            if ($.inArray(rowId, rows_selected) !== -1) {
                $(row).find('input[type="checkbox"]').prop('checked', true);
                $(row).addClass('selected');
            }
        }
    });


    // Handle click on checkbox
    $('#tbl_inline_subscribers tbody').on('click', 'input[type="checkbox"]', function (e) {
        var $row = $(this).closest('tr');

        // Get row data
        var data = dtbl_inline_subscribers.row($row).data();

        // Get row ID
        var rowId = data[0];

        // Determine whether row ID is in the list of selected row IDs
        var index = $.inArray(rowId, rows_selected);

        // If checkbox is checked and row ID is not in list of selected row IDs
        if (this.checked && index === -1) {
            rows_selected.push(rowId);

            // Otherwise, if checkbox is not checked and row ID is in list of selected row IDs
        } else if (!this.checked && index !== -1) {
            rows_selected.splice(index, 1);
        }

        if (this.checked) {
            $row.addClass('selected');
        } else {
            $row.removeClass('selected');
        }

        // Update state of "Select all" control
        updateDataTableSelectAllCtrl(dtbl_inline_subscribers);

        // Prevent click event from propagating to parent
        e.stopPropagation();
    });


    // Handle click on table cells with checkboxes
    $('#tbl_inline_subscribers').on('click', 'tbody td, thead th:first-child', function (e) {
        $(this).parent().find('input[type="checkbox"]').trigger('click');
    });


    // Handle click on "Select all" control
    $('thead input[type="checkbox"]', dtbl_inline_subscribers.table().container()).on('click', function (e) {
        if (this.checked) {
            $('#tbl_inline_subscribers tbody input[type="checkbox"]:not(:checked)').trigger('click');
        } else {
            $('#tbl_inline_subscribers tbody input[type="checkbox"]:checked').trigger('click');
        }

        // Prevent click event from propagating to parent
        e.stopPropagation();
    });


    // Handle table draw event
    dtbl_inline_subscribers.on('draw', function () {
        // Update state of "Select all" control
        updateDataTableSelectAllCtrl(dtbl_inline_subscribers);
    });


    $("#btn_delete_subscriber").click(function () {
        $("#tbl_subscribers_line tr").each(function () {
            var check = $(this).find("input.chkbox").is(':checked');
            if (check) {

                var row = dtbl_mdl_subscribers.row.add([
                    $(this).find("input").eq(0).val(),
                    "<input class='chkbox' type='checkbox'>",
                    $(this).find("td").eq(2).html(),
                    $(this).find("td").eq(3).html(),
                    $(this).find("td").eq(4).html(),
                ]);
                dtbl_mdl_subscribers.row(row).column(0).nodes().to$().addClass('myHiddenColumn');
                dtbl_mdl_subscribers.row(row).draw();
                //$(this).remove();
                dtbl_inline_subscribers.row($(this)).remove().draw();
            }
        });
    });

});