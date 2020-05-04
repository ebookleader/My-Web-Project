$(".js-create-todo").click(function () {
  $.ajax({
    url: "{% url 'todo_create' day='mon' %}",
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

$("#modal-todo").on("submit", ".js-todo-create-form", function () {
  var form = $(this);
  $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        $("#todo-table tbody").html(data.html_todo_list);
        $("#modal-todo").modal("hide");
      }
      else {
        alert('data is not valid')
        $("#modal-todo .modal-content").html(data.html_form);
      }
    }
  });
  return false;
});