function nestedCheckbox_change(e) {
  checkbox = $(e.target);
  //Apply children
  if (!checkbox.is(":indeterminate")) {
    var ul = checkbox.parent("li").next("ul")
    if (ul.length != 0) {
      ul.children("li").children("input[type=checkbox]").prop("checked", checkbox.is(":checked"));
    }
  }
  nestedCheckbox_refreshMainValidity(checkbox)
  //Apply parent
  var ul=checkbox.parent("li").parent("ul")
  var checkbox=$(ul).prev("li").children("input[type=checkbox]")
  checkboxes=ul.children("li").children("input[type=checkbox]")
  var checkeds=Array.from(checkboxes).map(el=>el.checked)
  var scheckeds=Array.from(new Set(checkeds))
  if (scheckeds.length>1) {
    checkbox.prop("checked",false);
    checkbox.prop("indeterminate",true);
  }
  else{
    checkbox.prop("indeterminate",false);
    checkbox.prop("checked",scheckeds[0]);
  }
  nestedCheckbox_refreshMainValidity(checkbox)
}
function nestedCheckbox_refreshMainValidity(checkbox) {
  if (checkbox.data("onerequired") && !(checkbox.is(":checked") || checkbox.is(":indeterminate")) )  {
    checkbox.first().each(function() {
      this.setCustomValidity("Please check at least one of the checkboxes below")
    })
  }
  else {
    checkbox.first().each(function() {
      this.setCustomValidity("")
    })
  }
}