const sumario = document.getElementById("sumario");
const sumarioBtn = document.getElementById("sumario-btn");

sumarioBtn.addEventListener("click", () => sumario.classList.toggle("show"));

const modal4 = document.getElementById("modal-sala4");
const modal5 = document.getElementById("modal-sala5");
const abrirModal5 = document.getElementById("atividades-705");
const abrirModal4 = document.getElementById("atividades-704");
const fecharModal4 = document.getElementById("fecharModal-sala4");
const fecharModal5 = document.getElementById("fecharModal-sala5");

const abrirLogin = document.getElementById("login");
const fecharLogin = document.getElementById("fecharlogin-modal");
const modalLogin = document.getElementById("login-modal");  

function setupModal(openBtn, closeBtn, modal) {
  openBtn.addEventListener("click", () => modal.showModal());
  closeBtn.addEventListener("click", () => modal.close());
}

setupModal(abrirModal4, fecharModal4, modal4);
setupModal(abrirModal5, fecharModal5, modal5);
setupModal(abrirLogin, fecharLogin, modalLogin);
