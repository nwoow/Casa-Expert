jQuery(
  (function ($) {
    "use strict";

    // Menu Shrink JS
    $(window).on("scroll", function () {
      if ($(this).scrollTop() > 50) {
        $(".main-nav").addClass("menu-shrink");
      } else {
        $(".main-nav").removeClass("menu-shrink");
      }
    });

    // Mean Menu JS
    jQuery(".mean-menu").meanmenu({
      meanScreenWidth: "991",
    });

    // Odometer JS
    $(".odometer").appear(function (e) {
      var odo = $(".odometer");
      odo.each(function () {
        var countNumber = $(this).attr("data-count");
        $(this).html(countNumber);
      });
    });

    // Popup Youtube JS
    $(".popup-youtube").magnificPopup({
      disableOn: 320,
      type: "iframe",
      mainClass: "mfp-fade",
      removalDelay: 160,
      preloader: false,
      fixedContentPos: false,
    });
    $(".test-popup-link").magnificPopup({
      type: "image",
      // other options
    });

    // Review Slider JS
    $(".review-slider").owlCarousel({
      loop: true,
      margin: 0,
      nav: true,
      dots: false,
      smartSpeed: 1000,
      autoplay: true,
      autoplayTimeout: 4000,
      autoplayHoverPause: true,
      navText: [
        "<i class='bx bx-left-arrow-alt'></i>",
        "<i class='bx bx-right-arrow-alt'></i>",
      ],
      responsive: {
        0: {
          items: 1,
        },
        600: {
          items: 2,
        },
        1000: {
          items: 2,
        },
      },
    });

    // Nice Select JS
    $("select").niceSelect();

    // Accordion JS
    $(".accordion > li:eq(0) a").addClass("active").next().slideDown();
    $(".accordion a").on("click", function (j) {
      var dropDown = $(this).closest("li").find("p");
      $(this).closest(".accordion").find("p").not(dropDown).slideUp();
      if ($(this).hasClass("active")) {
        $(this).removeClass("active");
      } else {
        $(this).closest(".accordion").find("a.active").removeClass("active");
        $(this).addClass("active");
      }
      dropDown.stop(false, true).slideToggle();
      j.preventDefault();
    });

    // Timer JS
    let getDaysId = document.getElementById("days");
    if (getDaysId !== null) {
      const second = 1000;
      const minute = second * 60;
      const hour = minute * 60;
      const day = hour * 24;

      let countDown = new Date("December 30, 2022 00:00:00").getTime();
      setInterval(function () {
        let now = new Date().getTime();
        let distance = countDown - now;

        (document.getElementById("days").innerText = Math.floor(
          distance / day
        )),
          (document.getElementById("hours").innerText = Math.floor(
            (distance % day) / hour
          )),
          (document.getElementById("minutes").innerText = Math.floor(
            (distance % hour) / minute
          )),
          (document.getElementById("seconds").innerText = Math.floor(
            (distance % minute) / second
          ));
      }, second);
    }

    // Subscribe Form JS
    $(".newsletter-form")
      .validator()
      .on("submit", function (event) {
        if (event.isDefaultPrevented()) {
          // Hande the invalid form...
          formErrorSub();
          submitMSGSub(false, "Please enter your email correctly.");
        } else {
          // Everything looks good!
          event.preventDefault();
        }
      });
    function callbackFunction(resp) {
      if (resp.result === "success") {
        formSuccessSub();
      } else {
        formErrorSub();
      }
    }
    function formSuccessSub() {
      $(".newsletter-form")[0].reset();
      submitMSGSub(true, "Thank you for subscribing!");
      setTimeout(function () {
        $("#validator-newsletter").addClass("hide");
      }, 4000);
    }
    function formErrorSub() {
      $(".newsletter-form").addClass("animated shake");
      setTimeout(function () {
        $(".newsletter-form").removeClass("animated shake");
      }, 1000);
    }
    function submitMSGSub(valid, msg) {
      if (valid) {
        var msgClasses = "validation-success";
      } else {
        var msgClasses = "validation-danger";
      }
      $("#validator-newsletter").removeClass().addClass(msgClasses).text(msg);
    }

    // AJAX Mail Chimp JS
    $(".newsletter-form").ajaxChimp({
      url: "https://envytheme.us20.list-manage.com/subscribe/post?u=60e1ffe2e8a68ce1204cd39a5&amp;id=42d6d188d9", // Your url MailChimp
      callback: callbackFunction,
    });

    // Preloader JS
    jQuery(window).on("load", function () {
      jQuery(".loader").fadeOut(500);
    });

    // Back to Top JS
    $("body").append(
      '<div id="toTop" class="back-to-top-btn"><i class="bx bxs-up-arrow-alt"></i></div>'
    );
    $(window).on("scroll", function () {
      if ($(this).scrollTop() != 0) {
        $("#toTop").fadeIn();
      } else {
        $("#toTop").fadeOut();
      }
    });
    $("#toTop").on("click", function () {
      $("html, body").animate({ scrollTop: 0 }, 900);
      return false;
    });

    // Switch Btn
    // $("body").append(
    //   "<div class='switch-box'><label id='switch' class='switch'><input type='checkbox' onchange='toggleTheme()' id='slider'><span class='slider round'></span></label></div>"
    // );
  })(jQuery)
);

// function to set a given theme/color-scheme
function setTheme(themeName) {
  localStorage.setItem("lixi_theme", themeName);
  document.documentElement.className = themeName;
}

// function to toggle between light and dark theme
function toggleTheme() {
  if (localStorage.getItem("lixi_theme") === "theme-dark") {
    setTheme("theme-light");
  } else {
    setTheme("theme-dark");
  }
}

// Immediately invoked function to set the theme on initial load
(function () {
  if (localStorage.getItem("lixi_theme") === "theme-dark") {
    setTheme("theme-dark");
    document.getElementById("slider").checked = false;
  } else {
    setTheme("theme-light");
    document.getElementById("slider").checked = true;
  }
})();

// ----------------------------------------------------------------

const itemsContainer = document.getElementById("load-ser");
const loadMoreButton = document.getElementById("load-more");
const itemsPerPage = 3;
let currentPage = 1;

function showItems(start, end) {
  const items = itemsContainer.querySelectorAll(".serli");
  for (let i = 0; i < items.length; i++) {
    if (i >= start && i < end) {
      items[i].style.display = "block";
    } else {
      items[i].style.display = "none";
    }
  }
}

function loadMore() {
  const start = currentPage * itemsPerPage;
  const end = start + itemsPerPage;

  showItems(0, end);

  currentPage++;

  if (end >= itemsContainer.querySelectorAll(".serli").length) {
    loadMoreButton.style.display = "none";
  }
}

loadMoreButton.addEventListener("click", loadMore);
showItems(0, itemsPerPage);

//  Gallery

// active part navbar


const parentContainer = document.querySelector('.read-more-container');

parentContainer.addEventListener('click', event => {

    const current = event.target;

    const isReadMoreBtn = current.className.includes('read-more-btn');

    if (!isReadMoreBtn) return;

    const currentText = event.target.parentNode.querySelector('.read-more-text');

    currentText.classList.toggle('read-more-text--show');

    current.textContent = current.textContent.includes('View More') ? "View Less Offers..." : "View More Offers...";

})


