window.onload = function() {
    var cookieForm = document.getElementById('cookiePreferencesForm');
    cookieForm.addEventListener('submit', function(event) {
      event.preventDefault();
      saveCookiePreferences();
    });
  
    // Carregar preferências de cookies do localStorage, se existirem
    loadCookiePreferences();
  };
  
  function saveCookiePreferences() {
    var preferences = [];
    var checkboxes = document.getElementsByName('preferences');
    for (var i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i].checked) {
        preferences.push(checkboxes[i].value);
      }
    }
  
    // Salvar as preferências no localStorage
    localStorage.setItem('cookiePreferences', JSON.stringify(preferences));
  
    // Exemplo de feedback ao usuário
    alert('Preferências de cookies salvas com sucesso!');
  }
  
  function loadCookiePreferences() {
    var storedPreferences = localStorage.getItem('cookiePreferences');
    if (storedPreferences) {
      var preferences = JSON.parse(storedPreferences);
      var checkboxes = document.getElementsByName('preferences');
      for (var i = 0; i < checkboxes.length; i++) {
        if (preferences.includes(checkboxes[i].value)) {
          checkboxes[i].checked = true;
        }
      }
    }
  }
  