$(document).ready(function () {
  $(".sidenav").sidenav();
  $('.collapsible').collapsible();
  $('input#input_text, textarea#textarea2').characterCounter();
  $('select').formSelect();
  $('.datepicker').datepicker({
    format: "dd/mm/yyyy"
  });
  $('.tabs').tabs();
  $('.tooltipped').tooltip();
});