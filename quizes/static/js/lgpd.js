

// Verifica se os cookies foram aceitos
function checkCookieConsent() {
    var cookieConsent = localStorage.getItem("cookieConsent");
  
    if (!cookieConsent || cookieConsent !== "true") {
      // Mostra a janela pop-up de consentimento de cookies
      showCookiePopup();
      
    }
  }

  /** Mostra a janela pop-up de consentimento de cookies
  function showCookiePopup() {
    var popup = document.createElement("div");
    popup.className = "cookie-popup";
    
    popup.innerHTML = `
      <div class="container px-4 px-lg-5"> 
            <p> Utilizamos cookies para melhor experiência do usuário; 
              Para conferir detalhadamente, por favor leia nossa 
              <a href="javascript:void(0);" onclick="abrirPopup();"> política de privacidade. </a>
              <p> Ao ACEITAR estará concordando com os termos de uso de nosso portal. </p>
            </p> 
            <hr>
            <form method="POST" action="{% url 'salvaPreference' %}">
              {% csrf_token %}
                <div class="checkbox-group">
                    <input type="checkbox" id="essentialCookies" name="preferences" value="essential" checked disabled>
                    <label for="essentialCookies">Cookies Essenciais (Necessários)</label>
                </div>
                    <div class="checkbox-group">
                    <input type="checkbox" id="analyticsCookies" name="preferences" value="analytics" checked >
                    <label for="analyticsCookies">Cookies de Análise (Análise de tráfego e estatísticas)</label>
                </div>
                    <div class="checkbox-group">
                    <input type="checkbox" id="marketingCookies" name="preferences" value="marketing" checked>
                    <label for="marketingCookies">Cookies de Marketing (Conteúdo e exibição de anúncios)</label>
                </div> 
                    <hr>
                    <div class="justify-content-center text-center">
                    <button class="btn btn-primary" onclick="acceptCookies()"> Aceitar</button>
                    <button class="btn btn-secondary" type="submit"> SALVAR </button>
                  
                    <button class="btn btn-danger" onclick="rejectCookies()"> Recusar</button>
                    
                </div>
            </form>
      </div>`;
  
    document.body.appendChild(popup);
  }
 */

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
  