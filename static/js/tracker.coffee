$ ->
  $(document).click((event)->
    if event.target.nodeName == 'A'
      classes = $(event.target).attr("class")
      #alert classes
      #for c in classes.split(" ")
        #alert c
      #alert document.location
      #expocode = $(event.target).attr('expocode') || undefined
      expocode = $(event.target).parent().attr('expocode') || undefined
      fileType = $(event.target).parent().parent().parent().attr('class') || undefined
      #sourceLocation = document.referer
      #alert 'Tcross'
      string = '{"expocode":"'+ expocode+'", "file_type":"'+ fileType+'"}'
      #alert string
      if expocode
        #alert 'posting'
        $.ajax
          url: 'http://localhost:5000/'
          type: 'POST'
          dataType: 'json'
          crossDomain: true
          #contentType: "application/json; charset=utf-8"
          data: string
          success: (response)->
            alert response
          error: ->
            #alert "got ta error"
          timeout: 500000
  )
