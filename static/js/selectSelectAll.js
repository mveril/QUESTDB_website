function selectSelectAll_click(e) {
  ctrl=$(e.target).next()
  if (ctrl.prop('type') == 'select-multiple' ) {
    ctrl.find("option").each(function() {
      $(this).attr('selected', 'selected');
      });
  }
}