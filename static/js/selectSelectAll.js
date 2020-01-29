function selectSelectAll_click(e) {
  const ctrl = $(e.target).next()
  if (ctrl.prop('type') == 'select-multiple') {
    ctrl.find("option").each(function () {
      $(this).prop('selected', true);
      ctrl.trigger("change")
    });
  }
}