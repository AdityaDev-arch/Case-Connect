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
      responsive: {
        0: { items: 1 }, // 1 item for small screens
        600: { items: 2 }, // 2 items for medium screens
        1000: { items: 3 }, // 3 items for large screens
      },
    });
    console.log("Carousel initialized successfully.");
  }

  // 🔹 Fetch Latest Crime News
  document.addEventListener("DOMContentLoaded", function () {
    const rssUrl = "/fetch-rss"; // Backend endpoint to fetch RSS feed
    const newsContainer = document.getElementById("latest-crime-news");

    fetch(rssUrl)
      .then((response) => response.json())
      .then((articles) => {
        if (articles.length > 0) {
          articles.forEach((article) => {
            const newsItem = document.createElement("div");
            newsItem.classList.add("item"); // Add the 'item' class required by Owl Carousel
            newsItem.innerHTML = `
              <h5 class="mb-1">${article.title}</h5>
              <p>${article.published}</p>
              <a href="${article.link}" target="_blank">Read more</a>
            `;
            newsContainer.appendChild(newsItem);
          });

          // Initialize carousel after adding news items
          initializeCarousel();
        } else {
          newsContainer.innerHTML = "<p>No news articles found.</p>";
        }
      })
      .catch((error) => {
        console.error("Error fetching RSS feed:", error);
        newsContainer.innerHTML = "<p>Error fetching news articles.</p>";
      });
  });
})(jQuery);
window.onload = function () {
  fetch("/api/criminals")
    .then((response) => response.json())
    .then((data) => {
      const leftPanel = document.getElementById("inner_left_pannel");
      leftPanel.innerHTML = "";
      data.forEach((criminal) => {
        const div = document.createElement("div");
        div.className = "criminal-name";
        div.textContent = criminal.name;
        div.onclick = () => showDetails(criminal.id);
        leftPanel.appendChild(div);
      });
    });
};

function showDetails(criminalId) {
  fetch(`/api/criminals/${criminalId}`)
    .then((response) => response.json())
    .then((data) => {
      const detailsContent = document.getElementById("inner_right_pannel");
      detailsContent.innerHTML = `
                <img src="${
                  data.photo_url
                }" style="width: 200px; border-radius: 10px; margin-top: 10px;"><br>
                <h3>${data.name}</h3>
                <p><strong>Age:</strong> ${data.age}</p>
                <p><strong>Criminal ID:</strong> ${data.criminal_id}</p>
                <p><strong>Crime:</strong> ${data.crime}</p>
                <p><strong>In Custody:</strong> ${
                  data.in_custody ? "Yes" : "No"
                }</p>
            `;
    });
}
