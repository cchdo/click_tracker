$ ->
  $("#clickTable").dataTable()
  get_latest = ->
    $.ajax
      url: 'http://localhost:5000/get_latest'
      type: 'GET'
      #contentType: "application/json; charset=utf-8"
      success: (response)->
        $("tbody").html("")
        $("tbody").append(response)
      error: ->
      timeout: 50000
  setInterval(get_latest, 10000)
