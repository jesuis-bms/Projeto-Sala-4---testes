const sumario = document.getElementById("sumario");
const sumarioBtn = document.getElementById("sumario-btn");

if (sumario && sumarioBtn) {
  sumarioBtn.addEventListener("click", () => sumario.classList.toggle("show"));
}

const modal4 = document.getElementById("modal-sala4");
const modal5 = document.getElementById("modal-sala5");
const abrirModal5 = document.getElementById("atividades-705");
const abrirModal4 = document.getElementById("atividades-704");
const fecharModal4 = document.getElementById("fecharModal-sala4");
const fecharModal5 = document.getElementById("fecharModal-sala5");

const abrirLogin = document.getElementById("login");
const fecharLogin = document.getElementById("fecharlogin-modal");
const modalLogin = document.getElementById("login-modal");
const erroLogin = document.querySelector(".erro-login");

document.querySelectorAll(".atividade-card").forEach((card) => {
  const menuBtn = card.querySelector(".menu-btn");
  const menu = card.querySelector(".atividade-menu");
  const editarBtn = card.querySelector(".editar-btn");
  const editarForm = card.querySelector(".editar-form");

  if (menuBtn && menu) {
    menuBtn.addEventListener("click", () => {
      menu.classList.toggle("oculto");
    });
  }

  if (editarBtn && editarForm && menu) {
    editarBtn.addEventListener("click", () => {
      editarForm.classList.toggle("oculto");
      menu.classList.add("oculto");
    });
  }
});

function setupFiltroMateria(modal, selectId) {
  if (!modal) return;

  const select = document.getElementById(selectId);
  if (!select) return;

  select.addEventListener("change", () => {
    const materiaEscolhida = select.value;
    const cards = modal.querySelectorAll(".atividade-card");

    cards.forEach((card) => {
      const materiaCard = card.dataset.materia;

      if (materiaEscolhida === "todas" || materiaCard === materiaEscolhida) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  });
}

setupFiltroMateria(modal4, "materias-sala4");
setupFiltroMateria(modal5, "materias-sala5");

if (modalLogin && erroLogin) {
  modalLogin.showModal();
}

function setupModal(openBtn, closeBtn, modal) {
  if (!openBtn || !closeBtn || !modal) return;

  openBtn.addEventListener("click", () => modal.showModal());
  closeBtn.addEventListener("click", () => modal.close());
}

setupModal(abrirModal4, fecharModal4, modal4);
setupModal(abrirModal5, fecharModal5, modal5);
setupModal(abrirLogin, fecharLogin, modalLogin);
