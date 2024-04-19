/* variáveis globais para as repostas */
let dominante = 0.00;
let influente = 0.00;
let estavel = 0.00;
let cauteloso = 0.00;

//Controla o número de questoes respondidas
let questoesRespondidas = 0.00;
let minimoRespostas = 0.00;
//let arrPagina = [];

/** Barra de Progresso *****/
var element = document.getElementById("myprogressBar"); 


/* Variáveis globais */
let perfilPredominante = 0.00;
let tipoPersonalidade = 0;
let pergunta = 0;
let ids = 0;
let quizRespondido = 0;
let perfilCalculado = 0;
let quizSalvo = 0;
let numero = 0;
let nomeDominante = "";
let nomeInfluente = "";
let nomeEstavel = "";
let nomeCauteloso = "";
let timerAtivo = false; 

let filtraRespostas = []; //lista para filtrar respostas repetidas 

const perfis = ['DOMINANTE','INFLUENTE','ESTAVEL','CAUTELOSO'];
const notas = [01,02,03,04];

//Pega is Id de cada elemento no template
const quizBox = document.getElementById('quiz-box');
const scoreBox = document.getElementById('score-box');
const resultBox = document.getElementById('result-box');
const timerBox = document.getElementById('timer-box');

/**  Manipulação do DISC - **/
const enviarResposta = document.getElementById('btnEnviar'); "btnSalvar"
const finalizaQuiz = document.getElementById('btnFinaliza');
const btnRelatorioQuiz = document.getElementById('btnRelatorio');
const btnSalvar = document.getElementById('btnSalvar');
const erros = document.getElementById('erro');

/** Avançar página  **/
const btnAvanca = document.getElementById('btnProxima');

/* Capturar: >Pk; >Questoes; >Tempo  e url dos resultados */
var questao = document.getElementsByClassName("cabecalho");
let totalQuestoes = 0.00;
let pk = 0;
let time = 0.00;
let urlIndex = "";
let urlResultados = "";
for(var i = 0; i < questao.length; i++) {
    var dataset = questao[i].dataset;
    totalQuestoes = parseInt(dataset.total);
    pk = parseInt(dataset.pk);
    time = dataset.time;
    urlIndex = dataset.index;
    urlResultados = dataset.url;
}

/* Para controle de tempo do teste */
let inicioTeste = "";
let fimTeste = "";
let duracaoTeste = 0.00;

//Para o relatório final via janela modal
const modalBody = document.getElementById('modal-body-confirm')
const relatorio = document.getElementById('result-box')

// Variáveis para SALVAR em bd
const quizForm = document.getElementById('quiz-form');
const quizModal = document.getElementById('quizResultModal');
const csrf = document.getElementsByName('csrfmiddlewaretoken');


/*** Incrementa uma barra de progresse **/
window.onload = function() {
    if(!localStorage.arrHoraInicial) {
        capturaHorario();
    }
    somaBarra();
    if (timerBox) activateTimer(time);
 }

/**** Passo 1 - Capturar cada resposta enviada individualmente */
function capturaResposta(){
    
    if(perfilCalculado == 0) {    
        /* Array interno para a soma acumulada de cada nota */
        nome = "";
        let dominante = [];
        let influente = [];
        let estavel = [];
        let cauteloso = [];
        perfilPredominante = 0;

        //lista para filtrar respostas repetidas 
        filtraRespostas = [];

        /***** pegar com um FOR as opçoes... clicadas  *****/
        const alternativa = document.getElementsByTagName("label");
        const lista = document.getElementsByTagName("select");
        
        //1. Primeiro FOR externo que pega os 02 caracteres de cada LABEL da alternativa (01,02,03,04)
        for (i=0; i < alternativa.length; i++){ //loop externo nos títulos das alternativas

            for (var i=0; i < lista.length; i++){ //loop interno nas respostas selecionadas

                //Pega a resposta de 1-4
                let resp = parseInt(lista[i].options[lista[i].selectedIndex].text);
                console.log("Resposta selecionada:" + resp);

                //Adiciona as repostas de cada questão isoladamente
                filtraRespostas.push(resp);

            } /* Fim do For interno*/

            /* ############ SE NÃO tiver notas repetidas ###################### */
            if (!testaDuplicados(filtraRespostas)){

                /******  //loop interno nas respostas selecionadas ***********/
                for (var i=0; i < lista.length; i++){ 
                    //Pega os 02 caracteres da alternativa e faz cast para inteiro
                    let tipoPerfil = parseInt(alternativa[i].outerText.slice(0,2));
                    console.log("Perfil selecionado:" + tipoPerfil);
                    
                    //Pega a resposta de 1-4
                    let resp = parseInt(lista[i].options[lista[i].selectedIndex].text);
                    console.log("Resposta selecionada:" + resp);

                    if (tipoPerfil == 01) {
                        if (localStorage.arrDominante){
                            dominante = JSON.parse(localStorage.getItem('arrDominante'));
                        }
                        dominante.push(resp);
                        localStorage.arrDominante = JSON.stringify(dominante);
                        //nome = perfis[0];
                        console.log("======== função capturaResposta ========")
                        console.log("Array arrDominante: " + dominante);
                    }else if (tipoPerfil == 02) {
                        if (localStorage.arrInfluente){
                            influente = JSON.parse(localStorage.getItem('arrInfluente'));
                        }
                        influente.push(resp);
                        localStorage.arrInfluente = JSON.stringify(influente);
                    }else if (tipoPerfil == 03) {
                        if (localStorage.arrEstavel){
                            estavel = JSON.parse(localStorage.getItem('arrEstavel'));
                        }
                        estavel.push(resp);
                        localStorage.arrEstavel = JSON.stringify(estavel);
                    }else if (tipoPerfil == 04 ){
                        if (localStorage.arrCauteloso){
                            cauteloso = JSON.parse(localStorage.getItem('arrCauteloso'));
                        }
                        cauteloso.push(resp);
                        localStorage.arrCauteloso = JSON.stringify(cauteloso);
                    }else {
                        erros.innerHTML = "";
                        erros.innerHTML = "<h4 class='text-danger bg-white text-center mt-1'> \
                        Erro ao capturar o perfil e a resposta </h4>";
                    }
            
                } /* Fim do For interno das respostas duplicadas */
                somaQuestoes();
            
            } else { // Se forem notas repetidas...
                erros.innerHTML = "";
                erros.innerHTML = "<h4 class='text-danger bg-white text-center mt-1'> \
                Erro! As notas não devem ser repetidas. </h4>";
            }
    
        } /* Fim do For SUPERIOR - */ 
    }else{
        erros.innerHTML = "";
        erros.innerHTML = "<h4 class='text-danger text-center bg-white'> \
        Erro! O Perfil já foi calculado. Apenas salve-o agora. </h4>";  
    }
}

/** Passo 1.1 - Testar respostas repetidas */
function testaDuplicados(array) {
    return array.some(x => array.indexOf(x) !== array.lastIndexOf(x));
}

// Passo 2 - Incrementa 1 a cada questao respondida
const somaQuestoes = function() {
    let arr = [];
    if (localStorage.arrPagina){
        arr = JSON.parse(localStorage.getItem('arrPagina'));
    }
    arr.push(1); //Soma 1 a cada passada
    localStorage.arrPagina = JSON.stringify(arr);

    //console.log("== função conta Página ===")
    for(var i=0;  i < arr.length; i++){
            questoesRespondidas += parseInt(arr[i]);
    }
    console.log("== Total de Questões respondidas: " + questoesRespondidas);
    
    //armazena o mínimo do teste (%) em memoria
    localStorage.arrMinimoExigido = JSON.stringify(questoesRespondidas);
    
    //armazena o total de  questões respondidas
    localStorage.arrRespondidas = JSON.stringify(questoesRespondidas);

    arr = JSON.parse(localStorage.getItem('arrPagina'));
    minimoRespostas = (questoesRespondidas/totalQuestoes*100).toFixed(2);
    
    /**Avança página ao enviar resposta **/
     if (btnAvanca){
        btnAvanca.click(); 
    }
    
}

/** Incrementa barra de progresso no REFRESH da página*/
function somaBarra() {
   let width = 1; 
   let arr = [];
   if (localStorage.arrPagina){
       arr = JSON.parse(localStorage.getItem('arrPagina'));
   }
  
   for(var i=0;  i < arr.length; i++){
           width += parseInt(arr[i]);
   }

   let  mudaCss = (width/totalQuestoes*100).toFixed(2);
   //console.log("Valor de WIDTH: " + mudaCss);

   const calculaTaxa = `<b> <h6 class='text-white text-center mt-2'> 
        ${((width/totalQuestoes)*100).toFixed(2)}% </h6> </b>`;
   if (mudaCss > 100) {
    mudaCss = 0;
    }else{
        mudaCss++; 
        element.style.width = mudaCss + '%'; 
        //element.innerHTML = teste * 1  + '%';
        element.innerHTML = calculaTaxa;
        
    }
}

/******* Eventos dos botoes Finalizar, Salvar e Relatório ****/
if(finalizaQuiz){ //Se foi criado o elemento HTML...
   
        finalizaQuiz.addEventListener('click', ()=>{
            if (perfilCalculado == 0) {
                var confirma = confirm("ATENÇÃO!!  Só será possível calcular o perfil uma vez. Deseja prosseguir?");
                if (confirma) {
                    capturaResposta(); // para última pergunta do quiz                  
                    finalizaDisc();                  
                }      
            }else {
                erros.innerHTML = "";
                erros.innerHTML = "<h4 class='text-danger text-center bg-white'> \
                        Este perfil já foi calculado.</4>";                
            }
        })
}

/**  Passo 3 - Finaliza o quiz ** */
function finalizaDisc(){
    try{
        let arr = [];

        //Calcula a soma das notas para DOMINANTE
        if (localStorage.arrDominante){
            // Captura as respostas para o dominante
            arr = JSON.parse(localStorage.getItem('arrDominante'));
        } 
        for(var i=0;  i < arr.length; i++){
            console.log("Notas do array arrDominante: " + arr[i]);
            dominante += parseInt(arr[i]);
            console.log("==== Soma das notas dominantes: " + dominante);
        }
        
        //Calcula a soma das notas para INFLUENTE
        if (localStorage.arrInfluente){
            // Captura as respostas para o influente
            arr = JSON.parse(localStorage.getItem('arrInfluente'));
        
        }
        for(var i=0; i < arr.length; i++){
            console.log("Notas do array Influente: " +arr[i]);
            influente += parseInt(arr[i]);
            console.log("==== Soma das notas influentes: " + influente);
        }

        //Calcula a soma das notas para ESTAVEL
        if (localStorage.arrEstavel){    
            // Captura as respostas para o estavel
            arr = JSON.parse(localStorage.getItem('arrEstavel'));
        }
        for(var i=0; i < arr.length; i++){
            //console.log("Notas do array estável: " +arr[i]);
            estavel += parseInt(arr[i]);
            console.log("==== Soma das notas estável: " + estavel);
        }
        
        //Calcula a soma das notas para CAUTELOSO
        if (localStorage.arrCauteloso){    
            // Captura as respostas para o cauteloso
            arr = JSON.parse(localStorage.getItem('arrCauteloso'))
        }  
        for(var i in arr){
            //console.log("Notas do array cauteloso: " +arr[i]);
            cauteloso += parseInt(arr[i]);
            console.log("==== Soma das notas cauteloso: " + cauteloso);
        }
        quizRespondido =1;
        determinaPerfil();
    }catch(error) {
        erros.innerHTML = "";
        erros.innerHTML = "<h4 class='text-danger bg-white text-center' > \
           Erro ao DETERMINAR o perfil, código: </h4> " + error;
            perfilCalculado = 0;
    }
}

/**  Passo 4 - Determina o perfil e exibe na janela modal ** */
function determinaPerfil(){
    if (quizRespondido == 1) {
        if(perfilCalculado == 0) {        
            try { 
                //Captura a soma geral das maiores notas (maior perfil)
                console.log("========= DETERMINANDO PERFIL ===============")
                perfilPredominante = Math.max(dominante,influente,estavel,cauteloso);
        
                console.log("==== NOTAS dominante: " + dominante);
                console.log("==== NOTAS Influente: " + influente);
                console.log("==== NOTAS estavel: " + estavel);
                console.log("==== NOTAS cauteloso: " + cauteloso);
                console.log("Determinante:" + perfilPredominante)

                if (notas[0] == 01 && dominante == perfilPredominante){
                    nome = "";
                    nome = perfis[0];
                    console.log("PERFIL: " + nome);
                    tipoPersonalidade = notas[0];
                    quizRespondido = 1;
                    perfilCalculado = 1;
                }
                else if (notas[1] == 2 && influente == perfilPredominante){
                    nome = "";    
                    nome = perfis[1];
                    console.log("PERFIL: " + nome);
                    tipoPersonalidade = notas[1];
                    quizRespondido = 1;
                    perfilCalculado = 1;
                }
                else if (notas[2] == 3 && estavel == perfilPredominante) {
                    nome = "";
                    nome = perfis[2];
                    console.log("PERFIL: " + nome);
                    tipoPersonalidade = notas[2];
                    quizRespondido = 1;
                    perfilCalculado = 1;
                }
                else if (notas[3] == 4 && cauteloso == perfilPredominante) {
                    let nome = "";
                    nome = perfis[3]; 
                    console.log("PERFIL: " + nome);
                    tipoPersonalidade = notas[3];
                    quizRespondido = 1;
                    perfilCalculado = 1;
                }
                document.getElementById('dominante').innerHTML = "";
                document.getElementById('influente').innerHTML = "";
                document.getElementById('estavel').innerHTML = "";
                document.getElementById('cauteloso').innerHTML = "";
                document.getElementById('maiorPerfil').innerHTML = "";

                // Valores a serem exibidos no formulário
                const perfilDominante = `Perfil com: ${((dominante*100)/100).toFixed(2)}% de DOMINÂNCIA`;
                const perfilInfluente = `Perfil com: ${((influente*100)/100).toFixed(2)}% de INFLUÊNCIA`;
                const perfilEstavel   = `Perfil com: ${((estavel*100)/100).toFixed(2)}% de ESTABILIDADE`;
                const perfilCauteloso = `Perfil com: ${((cauteloso*100)/100).toFixed(2)}% de CAUTELA`;
                const perfilMaior     = `Perfil Determinante.: ${(nome)}`;

                //Seta os valores atualizados para o usuário
                document.getElementById('dominante').innerHTML = perfilDominante;
                document.getElementById('influente').innerHTML = perfilInfluente;
                document.getElementById('estavel').innerHTML   = perfilEstavel;
                document.getElementById('cauteloso').innerHTML = perfilCauteloso;
                document.getElementById('maiorPerfil').innerHTML = perfilMaior;
            }catch (error) {
                erros.innerHTML = "";
                erros.innerHTML = "<h4 class='text-danger text-center mt-1'> \
                                Erro ao determinar o perfil. Tente responder todas as alternativas </h4>";
            }      
        }else{
            erros.innerHTML = "";
            erros.innerHTML = "<h4 class='text-danger text-center bg-white'> \
            Erro! O Perfil já foi calculado. Apenas salve-o agora. </h4>";  
        }
    }else {
        erros.innerHTML = "";
        erros.innerHTML = "Por favor, responda a todas as perguntas antes de calcular o PERFIL.";

    }
}

/**  Passo 4.1 - Testa as condições antes SALVAR: >> Somente após calcular o perfil */ 
const preparaSalvaDisc = function(){
    if (quizSalvo == 0) { 
        if (perfilCalculado = 1){
            var salvar = confirm("Deseja salvar o questionário?");
            if(salvar){
                salvarDisc();
            }else{
                erros.innerHTML = "";
                erros.innerHTML = "<h4 class='text-danger text-center bg-white'> \
                            Gravação cancelada. Este quiz NÃO foi salvo. </4>";
            }
        }else{
            erros.innerHTML = "";
            erros.innerHTML = "<h4 class='text-danger text-center bg-white'> \
                    Por favor, CALCULE O PERFIL antes para salvar. </4>";
        }
    }else{
        erros.innerHTML = "";
        erros.innerHTML = "<h4 class='text-danger text-center bg-white'> \
                Erro! Este quiz JA FOI salvo. </4>";
    }
}

//Passo 5 - Enviar os dados para salvar em HD
function salvarDisc(){
    try{

        let arr = [];
        if (localStorage.arrHoraInicial){
            arr = JSON.parse(localStorage.getItem('arrHoraInicial'));
        } 
        for(var i=0;  i < arr.length; i++){
            inicioTeste = String(arr[i]);
        }

        //tempo do teste
        console.log("Hora início: " + inicioTeste);
        fimTeste = capturaHorario();

        console.log("Hora Fim: " + fimTeste);
        duracaoTeste = diferenca(inicioTeste, fimTeste);   

        console.log("Duração: " + duracaoTeste);
        /*Pega a localização da URL em questão com o ID do quiz. */
        let site = window.location.href;
        let rota = site.split("?"); //remove da ? pra frente (http://127.0.0.1:8000/joga-disc/1/?page=25)
        let url = rota[0] +"save/"; //http://127.0.0.1:8000/joga-disc/1/save/
        
        const data = {}
        if (localStorage.arrRespondidas !== '')
            var totalRespondido = (parseFloat(localStorage.arrRespondidas)/parseFloat(totalQuestoes))*100;
        else 
            var totalRespondido = 1;
        data['csrfmiddlewaretoken'] = csrf[0].value;
        data['tipoPersonalidade'] = tipoPersonalidade;
        data['scorePerfil'] = perfilPredominante;
        data['NomePerfil'] = nome;
        data['scoreDominante'] = dominante;
        data['scoreInfluente'] = influente;
        data['scoreEstavel'] = estavel;
        data['scoreCauteloso'] = cauteloso;
        data['tempoDuracao'] = duracaoTeste;
        data['totalRespondido'] =  totalRespondido;

        $.ajax({
            type:'POST',
            url: `${url}`,
            data: data,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response){
                erros.innerHTML = "<h4 class='text-danger text-center bg-white'> \
                Quiz salvo com sucesso! Gerando relatório.....</h4>";
                quizRespondido = 0;
                perfilCalculado = 1;
                quizSalvo = 1;
                clearItems();
                //location.reload(); //Refresh na pagina

                // Corta até a letra j (http://127.0.0.1:8000/joga-disc/1/?page=2)
                let rotaResult = site.split("j");
                                    
                /** Abre a rota http://127.0.0.1:8000/resultado/ em 5s  **/ 
                setTimeout(function(){
                    window.location.href = rotaResult[0] + "resultado/";
                    },5000); 
                   
            },
            error: function(error){
                erros.innerHTML = "<h4 class='text-danger text-center bg-white mt-1'> \
                Falha na requisição Ajax! Erro ao ENVIAR ao banco de dados, código: </h4> "+ error;
            }
            }) // fim da requisição AJAX
        } catch(e){
            erros.innerHTML = "";
            erros.innerHTML = "<h4 class='text-danger text-center bg-white mt-1'> \
            Erro ao salvar os parâmetros essencias do QUIZ. Código: </h4>" + e;
            quizSalvo = 0;
        }
}

//Passo 6 - Limpar os arrays do localStorage para próximo quiz
function clearItems(){
    try {
        let arr = [];
        localStorage.arrDominante = JSON.stringify(arr);
        localStorage.arrInfluente = JSON.stringify(arr);
        localStorage.arrEstavel = JSON.stringify(arr); 
        localStorage.arrCauteloso = JSON.stringify(arr); 
        localStorage.arrPagina = JSON.stringify(arr); 
        localStorage.arrMinimoExigido = JSON.stringify(arr); 
        localStorage.arrRespondidas = JSON.stringify(arr);
        localStorage.arrHoraInicial = JSON.stringify(arr); //limpa o horario anterior
        localStorage.removeItem('arrHoraInicial');
    } catch (error){
        alert("Erro ao limpar o armazenamento local. Tente Limpa manualmente. Código: " + error)
    }
}


const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    //Executada a cada 1s...
    const timer = setInterval(()=>{
        seconds--; 
        if (seconds < 0) {
            seconds = 59
            minutes --
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0'+minutes
        } else {
            displayMinutes = minutes
        }
        if(seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                //alert('Time over')
                //finalizaDisc();
                capturaResposta();
            }, 500)
        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}

/*** 1. Capturao horario atual e grava no localStorage  **/
function capturaHorario() {
    
    var data = new Date();
    var h = data.getHours() + "";
    var m = data.getMinutes() + "";
    var s = data.getSeconds() + "";
    if (h.length == 1) h = "0" + h;
    if (m.length == 1) m = "0" + m; 
    if (s.length == 1) s = "0" + s;
    let horario = h + ":" + m + ":" + s;
    
    let arr = [];
    arr.push(horario);

    /**Grava no localStorage SE o browser suportar ****/
    if (window.localStorage) {
        if (!localStorage.arrHoraInicial) {//evita dupla gravação 
            //localStorage.setItem('arrHoraInicial', arr);
            localStorage.arrHoraInicial = JSON.stringify(arr); 
        }
        else {
            arr = JSON.parse(localStorage.getItem('arrHoraInicial'));
        }  
    }else {
        alert("Navegador web não suportado. Favor usar outra versão.");
    }
    console.log("Início da prova: " + localStorage.arrHoraInicial);
    return horario;
}

/*** 2.Faz a conversão de um horário string em minutos  **/
function parse(horario) {
    try {
    // divide a string em duas partes, separado por dois-pontos, e transforma em número
    let [hora, minuto] = horario.split(':').map(v => parseInt(v));
    if (!minuto) { // para o caso de não ter os minutos
        minuto = 0;
    }
    let total = minuto + (hora * 60);
    return total;
    } catch(erro){
        console.log("Erro ao converter horários: " + erro)
    }
}

/***** 3. Calcula a duração total de dois horarios em minutos ******/
function diferenca(inicio, termino){
    try {
        let entrada = parse(inicio);
        let saida = parse(termino);

        // diferença entre as jornadas
        let diff = Math.abs(saida - entrada);
        if (diff != 0) {
            let horas = Math.floor(diff / 60);
            let minutos = diff - (horas * 60);
            console.log(`${horas} horas e ${minutos} minutos a ${saida > entrada ? 'mais' : 'menos'}`);
        }
        return diff;
    } catch(erro) {
        console.log("Erro ao calcular diferença: " + erro)

    }
}
