import { api } from "./api.js";

const statusEl = document.getElementById("api-status");
const toastEl = document.getElementById("toast");

const clienteSelects = [
  document.getElementById("cita-cliente"),
  document.getElementById("parcela-cliente"),
];

function showToast(message, isError = false) {
  toastEl.textContent = message;
  toastEl.classList.toggle("error", isError);
  toastEl.classList.remove("hidden");

  setTimeout(() => toastEl.classList.add("hidden"), 3200);
}

function formatDate(value) {
  return new Intl.DateTimeFormat("es-MX", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function fillSelect(select, items, labelFn) {
  select.innerHTML = items.length
    ? items.map((item) => `<option value="${item.id}">${labelFn(item)}</option>`).join("")
    : `<option value="">Sin registros disponibles</option>`;
}

async function loadClientes() {
  const clientes = await api.getClientes();
  clienteSelects.forEach((select) => {
    fillSelect(select, clientes, (c) => `${c.nombre} (${c.email})`);
  });
  return clientes;
}

async function loadParcelas() {
  const parcelas = await api.getParcelas();
  const select = document.getElementById("cita-parcela");
  fillSelect(select, parcelas, (p) => `${p.nombre} - ${p.cultivo}`);
  return parcelas;
}

async function loadCitas(clientes, parcelas) {
  const citas = await api.getCitas();
  const list = document.getElementById("citas-list");

  if (!citas.length) {
    list.innerHTML = `<p class="empty">No hay citas programadas todavía.</p>`;
    return;
  }

  const clientesMap = new Map(clientes.map((c) => [c.id, c.nombre]));
  const parcelasMap = new Map(parcelas.map((p) => [p.id, p.nombre]));

  list.innerHTML = citas
    .map(
      (cita) => `
        <article class="card">
          <h3 class="card__title">${clientesMap.get(cita.cliente_id) || "Cliente"} · ${parcelasMap.get(cita.parcela_id) || "Parcela"}</h3>
          <p class="card__meta">${formatDate(cita.fecha_programada)} · ${cita.tipo_servicio}</p>
          <p class="card__meta">${cita.operador ? `Operador: ${cita.operador}` : "Operador pendiente"}</p>
          <span class="badge ${cita.estado}">${cita.estado.replace("_", " ")}</span>
        </article>
      `
    )
    .join("");
}

async function refreshAll() {
  const [clientes, parcelas] = await Promise.all([loadClientes(), loadParcelas()]);
  await loadCitas(clientes, parcelas);
}

document.getElementById("form-cliente").addEventListener("submit", async (event) => {
  event.preventDefault();

  try {
    await api.createCliente({
      nombre: document.getElementById("cliente-nombre").value.trim(),
      email: document.getElementById("cliente-email").value.trim(),
      telefono: document.getElementById("cliente-telefono").value.trim() || null,
    });

    event.target.reset();
    showToast("Cliente registrado correctamente.");
    await refreshAll();
  } catch (error) {
    showToast(error.message, true);
  }
});

document.getElementById("form-parcela").addEventListener("submit", async (event) => {
  event.preventDefault();

  try {
    await api.createParcela({
      cliente_id: Number(document.getElementById("parcela-cliente").value),
      nombre: document.getElementById("parcela-nombre").value.trim(),
      cultivo: document.getElementById("parcela-cultivo").value.trim(),
      hectareas: Number(document.getElementById("parcela-hectareas").value),
      ubicacion: document.getElementById("parcela-ubicacion").value.trim() || null,
    });

    event.target.reset();
    showToast("Parcela registrada correctamente.");
    await refreshAll();
  } catch (error) {
    showToast(error.message, true);
  }
});

document.getElementById("form-cita").addEventListener("submit", async (event) => {
  event.preventDefault();

  try {
    const fechaLocal = document.getElementById("cita-fecha").value;
    await api.createCita({
      cliente_id: Number(document.getElementById("cita-cliente").value),
      parcela_id: Number(document.getElementById("cita-parcela").value),
      fecha_programada: new Date(fechaLocal).toISOString(),
      tipo_servicio: document.getElementById("cita-servicio").value,
      operador: document.getElementById("cita-operador").value.trim() || null,
      notas: document.getElementById("cita-notas").value.trim() || null,
    });

    event.target.reset();
    showToast("Cita agendada correctamente.");
    await refreshAll();
  } catch (error) {
    showToast(error.message, true);
  }
});

document.getElementById("btn-refresh").addEventListener("click", refreshAll);

async function bootstrap() {
  try {
    await api.health();
    statusEl.textContent = "API conectada";
    await refreshAll();
  } catch {
    statusEl.textContent = "API no disponible";
    statusEl.classList.add("error");
  }
}

bootstrap();
