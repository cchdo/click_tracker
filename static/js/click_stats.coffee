$ ->
  $("#files").dataTable()
  $("#users").dataTable()
  get_latest = (types)->
    address = "http://localhost:5000/get_latest_" + types
    selector = "#" + types + " tbody"
    $.ajax
      url: address
      type: 'GET'
      #contentType: "application/json; charset=utf-8"
      success: (response)->
        $(selector).html("")
        $(selector).append(response)
      error: ->
      timeout: 50000
  setInterval(get_latest("files"), 10000)
  setInterval(get_latest("users"), 10000)
