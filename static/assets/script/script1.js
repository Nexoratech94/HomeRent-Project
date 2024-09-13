// search-box open close js code
let navbar = document.querySelector(".navbar");
let searchBox = document.querySelector(".search-box .bx-search");
// let searchBoxCancel = document.querySelector(".search-box .bx-x");

searchBox.addEventListener("click", () => {
  navbar.classList.toggle("showInput");
  if (navbar.classList.contains("showInput")) {
    searchBox.classList.replace("bx-search", "bx-x");
  } else {
    searchBox.classList.replace("bx-x", "bx-search");
  }
});

// sidebar open close js code
let navLinks = document.querySelector(".nav-links");
let menuOpenBtn = document.querySelector(".navbar .bx-menu");
let menuCloseBtn = document.querySelector(".nav-links .bx-x");
menuOpenBtn.onclick = function () {
  navLinks.style.left = "0";
}
menuCloseBtn.onclick = function () {
  navLinks.style.left = "-100%";
}


// sidebar submenu open close js code
let htmlcssArrow = document.querySelector(".htmlcss-arrow");
htmlcssArrow.onclick = function () {
  navLinks.classList.toggle("show1");
}
let moreArrow = document.querySelector(".more-arrow");
moreArrow.onclick = function () {
  navLinks.classList.toggle("show2");
}
let jsArrow = document.querySelector(".js-arrow");
jsArrow.onclick = function () {
  navLinks.classList.toggle("show3");
}


//room page animation
// Function to handle form submission
function searchRooms() {
  // Get selected values from dropdowns
  var location = encodeURIComponent(document.getElementById('location').value);
  var prototype = encodeURIComponent(document.getElementById('prototype').value);
  var price = document.getElementById('price').value.replace(' TAKA', ''); // Remove ' TAKA' from price

  // Construct the search URL with selected values
  var searchURL = "/search/?location=" + location + "&prototype=" + prototype + "&price=" + price;

  // Redirect to the search URL
  window.location.href = searchURL;




  function showSuggestions(str) {
    if (str.length == 0) {
      document.getElementById("suggestions").innerHTML = "";
      return;
    }

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
        var suggestions = JSON.parse(this.responseText);
        var suggestionsBox = document.getElementById("suggestions");
        suggestionsBox.innerHTML = "";
        suggestions.forEach(function (suggestion) {
          var div = document.createElement("div");
          div.textContent = suggestion;
          div.classList.add("suggestion-item");
          suggestionsBox.appendChild(div);
        });
      }
    };
    xhr.open("GET", "/get_suggestions/?q=" + str, true);
    xhr.send();
  }
}
