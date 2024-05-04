

// Verifica se os cookies foram aceitos
function checkCookieConsent() {
    var cookieConsent = localStorage.getItem("cookieConsent");
  
    if (!cookieConsent || cookieConsent !== "true") {
      // Mostra a janela pop-up de consentimento de cookies
      showCookiePopup();
      
    }
  }


  //Política de privaciade
  function lerPolitica(){
    
    let site = window.location.href;
    let rota = site.split("i"); //remove da / pra frente (http://127.0.0.1:8000/)
    console.log(rota)
    let url = rota[0] + "politica/"; //http://127.0.0.1:8000/politica/
    window.location.href = url;

  }

  
  // Aceita os cookies
  function acceptCookies() {
    saveCookieConsent(true);
    closeCookiePopup();
  }
  
  // Recusa os cookies
  function rejectCookies() {
    saveCookieConsent(false);
    closeCookiePopup();
  }
  
  // Salva o consentimento de cookies no armazenamento local (localStorage)
  function saveCookieConsent(consent) {
    localStorage.setItem("cookieConsent", consent);
  }
  
  // Fecha a janela pop-up de consentimento de cookies
  function closeCookiePopup() {
    var popup = document.querySelector(".cookie-popup");
    if (popup) {
      popup.remove();
    }
  }
  
  // Verifica o consentimento de cookies ao carregar a página
  window.addEventListener("load", checkCookieConsent);
  