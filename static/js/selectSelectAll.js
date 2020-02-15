function selectSelectAll_click(e) {
  const ctrl = $(e.target).next()
  selectSelectAll(ctrl)
}
function selectSelectAll(target) {
  if (target.prop('type') == 'select-multiple') {
    const old=target.val()
    target.find("option").each(function () {
      $(this).prop('selected', true);
    });
    if (old!==target.val()) {
      target.trigger("change") 
    }
  }
}