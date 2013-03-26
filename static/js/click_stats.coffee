$ ->
  get_latest = (types)->
    address = "/get_latest_" + types
    selector = "#" + types + " tbody"
    $.ajax
      url: address
      type: 'GET'
      #contentType: "application/json; charset=utf-8"
      success: (response)->
        $(selector).html("")
        $(selector).append(response)
        $("#"+types).dataTable
          "sDom":'T<"clear">lfrtip'
          "oTableTools":
              "sSwfPath": 'static/swf/copy_csv_xls.swf'
              "aButtons":    [ "csv", "xls" ] 
      error: ->
      timeout: 900000

  get_latest("files")
  get_latest("users")
