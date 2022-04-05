let value = 0;
let page = "quali";

$(document).ready(function () {
  $(".sidenav").sidenav();
  $(".collapsible").collapsible();
  $("input#input_text, textarea#textarea2").characterCounter();
  $("select").formSelect();
  $(".datepicker").datepicker({
    format: "dd/mm/yyyy",
  });
  $(".tabs").tabs();
  $(".tooltipped").tooltip();
  $(".modal").modal({});
});

$("#driverModal").click(function () {
  $("#driverSearch").val("");
  $(".list")
    .find("tr")
    .each(function () {
      $(this).show();
    });
});

$("#constructorModal").click(function () {
  $("#constructorSearch").val("");
  $(".list")
    .find("tr")
    .each(function () {
      $(this).show();
    });
});

$("#driverSearch").keyup(function () {
  $(".list")
    .find("tr")
    .each(function () {
      if (
        $(this)
          .text()
          .toLowerCase()
          .includes($("#driverSearch").val().toLowerCase())
      ) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
});

$("#constructorSearch").keyup(function () {
  $(".list")
    .find("tr")
    .each(function () {
      if (
        $(this)
          .text()
          .toLowerCase()
          .includes($("#constructorSearch").val().toLowerCase())
      ) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
});

$(".quali").click(function () {
  page = "quali";
  console.log(page);
});

$(".race").click(function () {
  page = "race";
  console.log(page);
});

$(".select").click(function () {
  value = $(this).closest("tr").children("td:first").text().slice(0, -1) - 1;
});

$(".driverSelect").click(function () {
  console.log(value);
  console.log(page);
  if (page == "quali") {
    $("#driver_forename_pos_quali_" + value).val(
      $(this).closest("tr").children("td:first").text()
    );
    $("#driver_surname_pos_quali_" + value).val(
      $(this).closest("tr").children("td:eq(1)").text()
    );
    $("#driver_id_pos_quali_" + value).val(
      $(this).closest("tr").children("td:eq(2)").text()
    );
  } else if (page == "race") {
    $("#driver_forename_pos_race_" + value).val(
      $(this).closest("tr").children("td:first").text()
    );
    $("#driver_surname_pos_race_" + value).val(
      $(this).closest("tr").children("td:eq(1)").text()
    );
    $("#driver_id_pos_race_" + value).val(
      $(this).closest("tr").children("td:eq(2)").text()
    );
  }
});

$(".constructorSelect").click(function () {
  if (page == "quali") {
    $("#constructor_quali_pos_" + value).val(
      $(this).closest("tr").children("td:first").text()
    );
    $("#constructor_id_quali_pos_" + value).val(
      $(this).closest("tr").children("td:eq(2)").text()
    );
  } else if (page == "race") {
    $("#constructor_race_pos_" + value).val(
      $(this).closest("tr").children("td:first").text()
    );
    $("#constructor_id_race_pos_" + value).val(
      $(this).closest("tr").children("td:eq(2)").text()
    );
  }
});

$('input[type="checkbox"]').on("change", function () {
  $('input[type="checkbox"]').not(this).prop("checked", false);
});
