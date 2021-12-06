function selectFilter_Click(e) {
  const target=$(e.target)
  const ctrl = target.nextAll("select").first()
  selectFilter(ctrl,target.val())
}
function selectFilter(target,text) {
  target.find("option").each(function () {
    if (text==='' || $(this).text().toLowerCase().includes(text.toLowerCase())) {
      $(this).show()
    }
    else {
      $(this).hide()
    }
  });
}