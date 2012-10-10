(function() {
  $(function() {
    var get_latest;
    $("#clickTable").dataTable();
    get_latest = function() {
      return $.ajax({
        url: 'http://localhost:5000/get_latest',
        type: 'GET',
        success: function(response) {
          $("tbody").html("");
          return $("tbody").append(response);
        },
        error: function() {},
        timeout: 50000
      });
    };
    return setInterval(get_latest, 10000);
  });
}).call(this);
