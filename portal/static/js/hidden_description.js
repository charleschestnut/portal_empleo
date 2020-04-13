function hide_description() {
  var x = document.getElementByClassName("hidden_description");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}