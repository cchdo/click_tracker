(function() {
  $(function() {
    var get_latest;
    $("#files").dataTable();
    $("#users").dataTable();
    get_latest = function(types) {
      var address, selector;
      address = "http://localhost:5000/get_latest_" + types;
      selector = "#" + types + " tbody";
      return $.ajax({
        url: address,
        type: 'GET',
        success: function(response) {
          $(selector).html("");
          return $(selector).append(response);
        },
        error: function() {},
        timeout: 50000
      });
    };
    setInterval(get_latest("files"), 10000);
    return setInterval(get_latest("users"), 10000);
  });
}).call(this);
