document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const fnameInput = document.getElementById("fname");
  const lnameInput = document.getElementById("lname");
  const emailInput = document.getElementById("email");
  const dobInput = document.getElementById("dob");

  const fnameIcon = document.getElementById("fname-icon");
  const lnameIcon = document.getElementById("lname-icon");

  // create tooltip for email
  const emailIcon = document.createElement("span");
  emailIcon.classList.add("tooltip-wrapper");
  emailIcon.style.display = "none";
  emailIcon.innerHTML = `
    <img src="${document.querySelector('.tooltip-icon')?.getAttribute('src') || '/static/alert_5610989.png'}" alt="!" class="tooltip-icon">
    <span class="tooltip-text">Введите корректный email (например: user@mail.com)</span>
  `;
  emailInput.parentNode.insertBefore(emailIcon, emailInput.nextSibling);

  function capitalizeFirstLetter(str) {
    if (!str) return "";
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  function checkCapital(input, iconWrapper) {
    let value = input.value.trim();

    if (value && value[0] !== value[0].toUpperCase()) {
      input.value = capitalizeFirstLetter(value);
      value = input.value;
    }

    if (value) {
      iconWrapper.style.display = "none";
      input.style.borderColor = "green";
    } else {
      iconWrapper.style.display = "none";
      input.style.borderColor = "";
    }
  }

  function checkEmail(input, iconWrapper) {
    const value = input.value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!value) {
      iconWrapper.style.display = "none";
      input.style.borderColor = "";
      return;
    }

    if (emailPattern.test(value)) {
      iconWrapper.style.display = "none";
      input.style.borderColor = "green";
    } else {
      iconWrapper.style.display = "inline-block";
      input.style.borderColor = "red";
    }
  }

  // notifications
  function showNotification(message, type = "success") {
    let container = document.querySelector(".notification-container");
    if (!container) {
      container = document.createElement("div");
      container.className = "notification-container";
      document.body.appendChild(container);
    }

    const notif = document.createElement("div");
    notif.className = `notification ${type}`;
    notif.textContent = message;
    container.appendChild(notif);

    setTimeout(() => notif.classList.add("show"), 50);
    setTimeout(() => {
      notif.classList.remove("show");
      setTimeout(() => notif.remove(), 400);
    }, 3000);
  }

  // events
  fnameInput.addEventListener("input", () => checkCapital(fnameInput, fnameIcon));
  lnameInput.addEventListener("input", () => checkCapital(lnameInput, lnameIcon));
  fnameInput.addEventListener("blur", () => checkCapital(fnameInput, fnameIcon));
  lnameInput.addEventListener("blur", () => checkCapital(lnameInput, lnameIcon));

  emailInput.addEventListener("input", () => checkEmail(emailInput, emailIcon));
  emailInput.addEventListener("blur", () => checkEmail(emailInput, emailIcon));

  // submit handler: show toast and submit
  form.addEventListener("submit", function (event) {
    // client-side DOB check
    if (!dobInput.value) {
      showNotification("Пожалуйста, укажите дату рождения", "error");
      event.preventDefault();
      return;
    }
    const dob = new Date(dobInput.value);
    const now = new Date();
    let age = now.getFullYear() - dob.getFullYear();
    const m = now.getMonth() - dob.getMonth();
    if (m < 0 || (m === 0 && now.getDate() < dob.getDate())) {
      age--;
    }

    if (age < 16) {
      showNotification("Для регистрации нужно быть старше 16 лет ❌", "error");
      event.preventDefault();
      return;
    }

    // show success then submit to backend
    showNotification("Регистрация отправляется ✅", "success");
    event.preventDefault();
    setTimeout(() => form.submit(), 600);
  });
});
