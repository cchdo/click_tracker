$(function() {
  var get_latest = function(types) {
    var address = "/get_latest_" + types;
    var selector = "#" + types + " tbody";
    return $.ajax({
      url: address,
      success: function(response) {
        $(selector).html(response);
      },
      timeout: 50000
    });
  };

  $("#files").dataTable();
  $("#users").dataTable();
  get_latest('files');
  get_latest('users');
  var interval = 10000;
  setInterval(function() {get_latest("files")}, interval);
  setInterval(function() {get_latest("users")}, interval);
});
