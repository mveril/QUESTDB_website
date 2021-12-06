function selectFilter_Click(e) {
  const target=$(e.target)
  const ctrl = target.nextAll("select").first()
  selectFilter(ctrl)
}
function selectFilter(target) {
  const text=$(target).prevAll("input.selectSearch").first().val()
  target.find("option").each(function () {
    if (text==='' || $(this).text().toLowerCase().includes(text.toLowerCase())) {
      $(this).show()
    }
    else {
      $(this).hide()
    }
  });
}

function clearSelectFilter(target) {
  $(target).prevAll("input.selectSearch").val("")
}