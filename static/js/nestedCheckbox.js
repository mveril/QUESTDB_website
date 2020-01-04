function nestedCheckbox_change(e) {
  checkbox = e.target;
  //Apply children
  if (!checkbox.indeterminate) {
    var ul = $(checkbox).parent("li").next("ul")
    if (ul.length != 0) {
      ul.children("li").children("input[type=checkbox]").prop("checked", checkbox.checked);
    }
  }
  //Apply parent
  var ul=$(checkbox).parent("li").parent("ul")
  var checkbox=$(ul).prev("li").children("input[type=checkbox]")
  checkboxes=ul.children("li").children("input[type=checkbox]")
  var checkeds=Array.from(checkboxes).map(el=>el.checked)
  var scheckeds=new Set(checkeds)
  if (scheckeds.size>1) {
    $(checkbox).prop("checked",false);
    checkbox.prop("indeterminate",true);
  }
  else{
    checkbox.indeterminate=false;
    checkbox=scheckeds[0];
  }
}