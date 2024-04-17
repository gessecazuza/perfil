/* Variáveis globais */
let perfilPredominante = 0.00;
let tipoPersonalidade = 0;
let pergunta = 0;
let ids = 0;
let quizRespondido = 0;
let quizSalvo = 0;
let numero = 0;
let total = 0;

const perfis = ['DOMINANTE','INFLUENTE','ESTAVEL','CAUTELOSO'];
const notas = [01,02,03,04];

/*Pega a localização da URL em questão com o ID do quiz.
 > Vai em Urls, passa o parâmentro data em json - path('<pk>/data', quiz_data_view, name='quiz-data-view'), */
const url = window.location.href;


//Pega is Id de cada elemento no template
const quizBox = document.getElementById('quiz-box');
const scoreBox = document.getElementById('score-box');
const resultBox = document.getElementById('result-box');
const timerBox = document.getElementById('timer-box');
const btnProcessa = document.getElementById('btnProcessa');
const erros = document.getElementById('erro');


/* Função ajax que recebe os dados em JSON vindas da view quiz_data_view */
$.ajax({
    type: 'GET',  //O tipo de operação é receber (GET)
    url: `${url}data`, //Passa o rota com os dados (data)
    success: function(response){ //Se tiver success pega a resposta do dicionário em JSON
        const data = response.data; // Constante que recebe todos os dados da response
        total = response.total;

        data.forEach(el => {  //Tendo os dados, um forEach, passando por cada elemento (el)

            //Pegando cada el com o par chave e valor, podemos iterar com um for com
            //a pergunta chave (question) e as repostas (answers) como lista
            for (const [question, answers] of Object.entries(el)){
                pergunta++; pergunta.toString();

                //1. Imprime primeiro cada pergunta isoladamente
                quizBox.innerHTML += `  <hr>
                    <div class="h3 text-white bg-primary mt-3 mb-3">
                      ${pergunta}.${question} <br>
                    </div>
                 ` // Fim do for para questions

                 answers.forEach(answer => {  //Laço para todas as answers (respostas)
                    //style="background:skyblue; border:1px solid black; border-radius:10px; padding:7px
                    quizBox.innerHTML += `
                        <div class="marcador">
                           <h6> <label for="${question}" style="padding: 5px"> ${answer}  </label>   </h6>

                         <select class="form-control bg-light" id="${question}-${answer}" name="${question}">
                                    <b>
                                     <option value="1"> 1 </option>
                                     <option value="2"> 2 </option>
                                     <option value="3"> 3 </option>
                                     <option value="4"> 4 </option>
                                     </b>
                         </select>
                        </div>
                       `
                })
              }
        });
    },
    //Função que registra os erros
    error: function(error){
        console.log(error)
    }
}
)

btnProcessa.onclick = function() {
    //quizRespondido = 0;
    if (quizRespondido == 0){
        try{
            // Zerar os valores do cálculo do perfil
            let  nome = "";
            let dominante = 0.00;
            let influente = 0.00;
            let estavel = 0.00;
            let cauteloso = 0.00;
            perfilPredominante = 0;

            const alternativa = document.getElementsByTagName("label");
            const lista = document.getElementsByTagName("select");
            //1. Primeiro FOR externo que pega os 02 caracteres de cada LABEL da alternativa (01,02,03,04)
            for (i=0; i < alternativa.length; i++){ //loop externo nos títulos das alternativas
                for (var i=0; i < lista.length; i++){ //loop interno nas respostas selecionadas

                    //Pega os 02 caracteres e faz cast para inteiro
                    let tipoPerfil = parseInt(alternativa[i].outerText.slice(0,2));
                    
                    //Pega a resposta de 1-4
                    let resp = parseInt(lista[i].options[lista[i].selectedIndex].text);

                    if (tipoPerfil == 01) dominante += resp;
                    else if (tipoPerfil == 02) influente += resp;
                    else if (tipoPerfil == 03) estavel += resp;
                    else if (tipoPerfil == 04) cauteloso +=  resp;
                    else {
                        document.getElementById('erro').innerHTML = "";
                        document.getElementById('erro').innerHTML = "Erro! Verfique a resposta selecionada";
                    }
                }
            }
        
            //Captura a soma geral das maiores notas (maior perfil)
            perfilPredominante = Math.max(dominante,influente,estavel,cauteloso);

            if (notas[0] == 01 && dominante == perfilPredominante){
                nome = "";
                nome = perfis[0];
                console.log(nome);
                tipoPersonalidade = notas[0];
                quizRespondido = 1;
            }
            else if (notas[1] == 2 && influente == perfilPredominante){
                nome = "";    
                nome = perfis[1];
                console.log(nome);
                tipoPersonalidade = notas[1];
                quizRespondido = 1;
            }
            else if (notas[3] == 3 && estavel == perfilPredominante) {
                nome = "";
                nome = perfis[2];
                console.log(nome); 
                tipoPersonalidade = notas[2];
                quizRespondido = 1;
            }
            else if (notas[3] == 4 && cauteloso == perfilPredominante) {
                nome = "";
                nome = perfis[3]; 
                console.log(nome);
                tipoPersonalidade = notas[3];
                quizRespondido = 1;
            }
            else {
                document.getElementById('erro').innerHTML = "";
                document.getElementById('erro').innerHTML = "Erro ao determinar o perfil. Tente responder todas as alternativas";
                quizRespondido = 0;
            }
            
            if (quizRespondido == 1) {
                               
                document.getElementById('dominante').innerHTML = "";
                document.getElementById('influente').innerHTML = "";
                document.getElementById('estavel').innerHTML = "";
                document.getElementById('cauteloso').innerHTML = "";
                document.getElementById('maiorPerfil').innerHTML = "";
        
                // Valores a serem exibidos no formulário
                const perfilDominante = `Caracterísitica com.: ${((dominante/total)*100).toFixed(2)}% de perfil DOMINANTE`;
                const perfilInfluente = `Caracterísitica com.: ${((influente/total)*100).toFixed(2)}% de perfil INFLUENTE`;
                const perfilEstavel   = `Caracterísitica com.: ${((estavel/total)*100).toFixed(2)}% de perfil ESTÁVEL`;
                const perfilCauteloso = `Caracterísitica com.: ${((cauteloso/total)*100).toFixed(2)}% de perfil CAUTELOSO`;
                const perfilMaior     = `Perfil Determinante.: ${(nome)}`;
        
                //Seta os valores atualizados para o usuário
                document.getElementById('dominante').innerHTML = perfilDominante;
                document.getElementById('influente').innerHTML = perfilInfluente;
                document.getElementById('estavel').innerHTML   = perfilEstavel;
                document.getElementById('cauteloso').innerHTML = perfilCauteloso;
                document.getElementById('maiorPerfil').innerHTML = perfilMaior;
            }
            else{
                document.getElementById('erro').innerHTML = "";
                document.getElementById('erro').innerHTML = "Por favor, responda a todas as perguntas.";
            }
        
        } catch (e){
            document.getElementById('erro').innerHTML = "";
            document.getElementById('erro').innerHTML = "Erro ao calcular tipo de perfil. "+ e;
        } 
    }else{
            document.getElementById('erro').innerHTML = "";
            document.getElementById("erro").innerHTML = "Questionário já respondido. Apenas salve-o agora.";
    }
   
}

// Variáveis para SALVAR em bd
const quizForm = document.getElementById('quiz-form')
const quizModal = document.getElementById('quizResultModal')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

//Aciona o botão salvar ao clicar 
quizForm.addEventListener('submit', e=>{
    e.preventDefault();
    if (quizRespondido == 1){
        //document.getElementById('erro').innerHTML = "";
        sendData();
        //document.getElementById('erro').innerHTML = "Pronto para ser salvo.";
    }
    else {
        document.getElementById('erro').innerHTML = "";
        document.getElementById('erro').innerHTML = "Favor responda o questionário antes de salvar.";
    }
        
})

//A função que envia os dados para salvar em HD
const sendData = () => {
    if (quizSalvo == 0) {
        try{
            const elements = [...document.getElementsByClassName('form-control')] //Gera uma matriz de selects
            const data = {}
            data['csrfmiddlewaretoken'] = csrf[0].value;
            data['tipoPersonalidade'] = tipoPersonalidade;
            data['scorePerfil'] = perfilPredominante;
    
            //Laço que percorre cada resposta
            elements.forEach(el=>{
                if (el.checked) {
                    data[el.name] = el.value
                } else {
                    if (!data[el.name]) {
                        data[el.name] = null
                    }
                }
            })
            $.ajax({
                type:'POST',
                url: `${url}save/`,
                data: data,
                success: function(response){
                    //console.log(response)
                    document.getElementById('erro').innerHTML = "Quiz salvo com sucesso!!";
                    quizRespondido = 0;
                    quizSalvo = 1;
                },
                error: function(error){
                    document.getElementById('erro').innerHTML = "Erro ao salvar na base de dados! "+ error;
                    console.log(error)
                }
                }) // fim da requisição AJAX
            } catch(e){
                document.getElementById('erro').innerHTML = "";
                document.getElementById('erro').innerHTML = "Erro ao salvar! Tente limpar o histórico do navegador e reinicie.";
                quizSalvo = 0;
            }

    } else {
        document.getElementById('erro').innerHTML = "";
        document.getElementById('erro').innerHTML = "Este quiz já foi salvo.";
    }

    

} //Fim da funcao sendData()


