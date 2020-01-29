function selectSelectAll_click(e) {
  const ctrl = $(e.target).next()
  selectSelectAll(ctrl)
}
function selectSelectAll(target) {
  if (target.prop('type') == 'select-multiple') {
    target.find("option").each(function () {
      $(this).prop('selected', true);
      target.trigger("change")
    });
  }
}