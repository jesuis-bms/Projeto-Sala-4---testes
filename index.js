const sala4 = document.getElementById("atividades-704");
function sala_4() {}
addEventListener("click", sala_4);

const sumario = document.getElementById("sumario");
const sumarioBtn = document.getElementById("sumario-btn");

sumarioBtn.addEventListener("click", () => sumario.classList.toggle("show"));

const modal4 = document.getElementById("modal-sala4");
const modal5 = document.getElementById("modal-sala5");
const abrirModal5 = document.getElementById("atividades-705");
const abrirModal4 = document.getElementById("atividades-704");
const fecharModal4 = document.getElementById("fecharModal-sala4");
const fecharModal5 = document.getElementById("fecharModal-sala5");

function setupModal(openBtn, closeBtn, modal) {
  openBtn.addEventListener("click", () => modal.showModal());
  closeBtn.addEventListener("click", () => modal.close());
}

setupModal(abrirModal4, fecharModal4, modal4);
setupModal(abrirModal5, fecharModal5, modal5);
