(function() {
  $(function() {
    var get_latest;
    get_latest = function(types) {
      var address, selector;
      address = "/get_latest_" + types;
      selector = "#" + types + " tbody";
      return $.ajax({
        url: address,
        type: 'GET',
        success: function(response) {
          $(selector).html("");
          $(selector).append(response);
          return $("#" + types).dataTable({
            "sDom": 'T<"clear">lfrtip',
            "oTableTools": {
              "sSwfPath": 'static/swf/copy_csv_xls.swf',
              "aButtons": ["csv", "xls"]
            }
          });
        },
        error: function() {},
        timeout: 900000
      });
    };
    get_latest("files");
    return get_latest("users");
  });
}).call(this);
