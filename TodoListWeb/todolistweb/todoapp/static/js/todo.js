$(function () {

  $(".js-create-todo").click(function () {
    console.log('called')
    $.ajax({
      url: 'todo/create/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-todo").modal("show");
      },
      success: function (data) {
        $("#modal-todo .modal-content").html(data.html_form);
      }
    });
  });

});

