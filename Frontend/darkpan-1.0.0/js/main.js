(function ($) {
  "use strict";

  // Spinner
  var spinner = function () {
    setTimeout(function () {
      if ($("#spinner").length > 0) {
        $("#spinner").removeClass("show");
      }
    }, 1);
  };
  spinner();

  // Back to top button
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

  // Sidebar Toggler
  $(".sidebar-toggler").click(function () {
    $(".sidebar, .content").toggleClass("open");
    return false;
  });

  // Progress Bar
  $(".pg-bar").waypoint(
    function () {
      $(".progress .progress-bar").each(function () {
        $(this).css("width", $(this).attr("aria-valuenow") + "%");
      });
    },
    { offset: "80%" }
  );

  // Calender
  $("#calender").datetimepicker({
    inline: true,
    format: "L",
  });

  // Testimonials carousel
  $(".testimonial-carousel").owlCarousel({
    autoplay: true,
    smartSpeed: 1000,
    items: 1,
    dots: true,
    loop: true,
    nav: false,
  });

  // Chart Global Color
  Chart.defaults.color = "#6C7293";
  Chart.defaults.borderColor = "#000000";

  // Worldwide Sales Chart
  var ctx1 = $("#worldwide-sales").get(0);
  if (ctx1) {
    var myChart1 = new Chart(ctx1.getContext("2d"), {
      type: "bar",
      data: {
        labels: ["2016", "2017", "2018", "2019", "2020", "2021", "2022"],
        datasets: [
          {
            label: "USA",
            data: [15, 30, 55, 65, 60, 80, 95],
            backgroundColor: "rgba(235, 22, 22, .7)",
          },
          {
            label: "UK",
            data: [8, 35, 40, 60, 70, 55, 75],
            backgroundColor: "rgba(235, 22, 22, .5)",
          },
          {
            label: "AU",
            data: [12, 25, 45, 55, 65, 70, 60],
            backgroundColor: "rgba(235, 22, 22, .3)",
          },
        ],
      },
      options: {
        responsive: true,
      },
    });
  }

  // Sales & Revenue Chart
  var ctx2 = $("#salse-revenue").get(0);
  if (ctx2) {
    var myChart2 = new Chart(ctx2.getContext("2d"), {
      type: "line",
      data: {
        labels: ["2016", "2017", "2018", "2019", "2020", "2021", "2022"],
        datasets: [
          {
            label: "Sales",
            data: [15, 30, 55, 45, 70, 65, 85],
            backgroundColor: "rgba(235, 22, 22, .7)",
            fill: true,
          },
          {
            label: "Revenue",
            data: [99, 135, 170, 130, 190, 180, 270],
            backgroundColor: "rgba(235, 22, 22, .5)",
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
      },
    });
  }

  // Single Line Chart
  var ctx3 = $("#line-chart").get(0);
  if (ctx3) {
    var myChart3 = new Chart(ctx3.getContext("2d"), {
      type: "line",
      data: {
        labels: [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150],
        datasets: [
          {
            label: "Sales",
            fill: false,
            backgroundColor: "rgba(235, 22, 22, .7)",
            data: [7, 8, 8, 9, 9, 9, 10, 11, 14, 14, 15],
          },
        ],
      },
      options: {
        responsive: true,
      },
    });
  }

  // Single Bar Chart
  var ctx4 = $("#bar-chart").get(0);
  if (ctx4) {
    var myChart4 = new Chart(ctx4.getContext("2d"), {
      type: "bar",
      data: {
        labels: ["Italy", "France", "Spain", "USA", "Argentina"],
        datasets: [
          {
            backgroundColor: [
              "rgba(235, 22, 22, .7)",
              "rgba(235, 22, 22, .6)",
              "rgba(235, 22, 22, .5)",
              "rgba(235, 22, 22, .4)",
              "rgba(235, 22, 22, .3)",
            ],
            data: [55, 49, 44, 24, 15],
          },
        ],
      },
      options: {
        responsive: true,
      },
    });
  }

  // Pie Chart
  var ctx5 = $("#pie-chart").get(0);
  if (ctx5) {
    var myChart5 = new Chart(ctx5.getContext("2d"), {
      type: "pie",
      data: {
        labels: ["Italy", "France", "Spain", "USA", "Argentina"],
        datasets: [
          {
            backgroundColor: [
              "rgba(235, 22, 22, .7)",
              "rgba(235, 22, 22, .6)",
              "rgba(235, 22, 22, .5)",
              "rgba(235, 22, 22, .4)",
              "rgba(235, 22, 22, .3)",
            ],
            data: [55, 49, 44, 24, 15],
          },
        ],
      },
      options: {
        responsive: true,
      },
    });
  }

  // Doughnut Chart
  var ctx6 = $("#doughnut-chart").get(0);
  if (ctx6) {
    var myChart6 = new Chart(ctx6.getContext("2d"), {
      type: "doughnut",
      data: {
        labels: ["Italy", "France", "Spain", "USA", "Argentina"],
        datasets: [
          {
            backgroundColor: [
              "rgba(235, 22, 22, .7)",
              "rgba(235, 22, 22, .6)",
              "rgba(235, 22, 22, .5)",
              "rgba(235, 22, 22, .4)",
              "rgba(235, 22, 22, .3)",
            ],
            data: [55, 49, 44, 24, 15],
          },
        ],
      },
      options: {
        responsive: true,
      },
    });
  }
})(jQuery);

document.addEventListener("DOMContentLoaded", function () {
  const apiKey = "22ff55cf5fe5489ca46c93d6e67b552f"; // Replace with your News API key
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

        // Initialize the carousel after adding the news items
        $(".owl-carousel").owlCarousel({
          loop: true,
          margin: 10,
          nav: true,
          responsive: {
            0: {
              items: 1,
            },
            600: {
              items: 1,
            },
            1000: {
              items: 1,
            },
          },
        });
      } else {
        newsContainer.innerHTML = "<p>No news articles found.</p>";
      }
    })
    .catch((error) => {
      console.error("Error fetching news:", error);
      newsContainer.innerHTML = "<p>Error fetching news articles.</p>";
    });
});
