(function ($) {
  "use strict";

  // 🔹 Spinner
  var spinner = function () {
    setTimeout(function () {
      if ($("#spinner").length > 0) {
        $("#spinner").removeClass("show");
      }
    }, 1000);
  };
  spinner();

  // 🔹 Back to Top Button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
      $(".back-to-top").fadeIn("slow");
    } else {
      $(".back-to-top").fadeOut("slow");
    }
  });

  $(".back-to-top").click(function () {
    $("html, body").animate({ scrollTop: 0 }, 1500, "easeInOutExpo");
    return false;
  });

  // 🔹 Sidebar Toggler
  $(".sidebar-toggler").click(function () {
    $(".sidebar, .content").toggleClass("open");
    return false;
  });

  // 🔹 Testimonials Carousel (Latest News Slider)
  function initializeCarousel() {
    $(".owl-carousel").owlCarousel({
      autoplay: true,
      smartSpeed: 1000,
      items: 1,
      dots: true,
      loop: true,
      nav: false,
    });
  }

  // 🔹 Fetch Latest Crime News
  document.addEventListener("DOMContentLoaded", function () {
    const apiKey = "22ff55cf5fe5489ca46c93d6e67b552f"; // ❌ Expose API key (Use backend instead)
    const newsContainer = document.getElementById("latest-crime-news");

    fetch(`https://newsapi.org/v2/everything?q=crime&apiKey=${apiKey}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.articles && data.articles.length > 0) {
          data.articles.forEach((article) => {
            const newsItem = document.createElement("div");
            newsItem.classList.add("testimonial-item", "text-center");
            newsItem.innerHTML = `
              <img class="img-fluid rounded-circle mx-auto mb-4" src="${
                article.urlToImage || "img/default-user.png"
              }" style="width: 100px; height: 100px" />
              <h5 class="mb-1">${article.title}</h5>
              <p>${article.source.name}</p>
              <p class="mb-0">${article.description || ""}</p>
            `;
            newsContainer.appendChild(newsItem);
          });

          // ✅ Initialize carousel **AFTER** adding news items
          initializeCarousel();
        } else {
          newsContainer.innerHTML = "<p>No news articles found.</p>";
        }
      })
      .catch((error) => {
        console.error("Error fetching news:", error);
        newsContainer.innerHTML = "<p>Error fetching news articles.</p>";
      });
  });
})(jQuery);
