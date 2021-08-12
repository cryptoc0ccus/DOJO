$.fn.dataTable.TableTools.buttons.copy_to_div = $.extend(
  true,
  {},
  $.fn.dataTable.TableTools.buttonBase,
  {
      "sNewLine":    ">br<",
      "sButtonText": "Copy to element",
      "target":      "",
      "fnClick": function( button, conf ) {
          $(conf.target).html( this.fnGetTableData(conf) );
      }
  }
);




$(document).ready( function () {
    $('#students').DataTable({
        responsive: true

        dom': 'T<"clear">lfrtip',
        tableTools': {
            "aButtons": [ {
                "sExtends":    "copy_to_div",
                "sButtonText": "Copy to div",
                "target":      "#copy",
            } ]
        }



      });
    } );
    