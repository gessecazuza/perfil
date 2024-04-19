
/*
 > Retorna uma coleção de elementos HTML do botão modal.
 > Os [... ] transforma a colection num array que permite um laço forEach
*/


const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

//Pega a URL atual em uso
const url = window.location.href
console.log("endereço:" + url);

modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
    const pk = modalBtn.getAttribute('data-pk')
    const name = modalBtn.getAttribute('data-quiz')
    const numQuestions = modalBtn.getAttribute('data-questions')
    const difficulty = modalBtn.getAttribute('data-difficulty')
    const scoreToPass = modalBtn.getAttribute('data-pass')
    const time = modalBtn.getAttribute('data-time')

    modalBody.innerHTML = `
        <div class="h5 mb-3">Deseja iniciar o quiz: "<b>${name}</b>"?</div>
        <div class="text-muted">
            <ul>
                <li>Nível de Dificuldade: <b>${difficulty}</b></li>
                <li>Número de Perguntas: <b>${numQuestions}</b></li>
                <li>Pontuação mínima   : <b>${scoreToPass}%</b></li>
                <li>Tempo máximo       : <b>${time} min</b></li>
            </ul>
        </div>
    `

    startBtn.addEventListener('click', ()=>{
        window.location.href = url + pk
    })
}))
