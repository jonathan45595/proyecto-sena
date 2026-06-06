const API_BASE = "http://127.0.0.1:8001/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let detail = "Error en la solicitud";
    try {
      const data = await response.json();
      detail = data.detail || detail;
    } catch {
      // ignore parse errors
    }
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const api = {
  health: () => fetch("http://127.0.0.1:8001/health").then((r) => r.json()),
  getClientes: () => request("/clientes/"),
  createCliente: (payload) =>
    request("/clientes/", { method: "POST", body: JSON.stringify(payload) }),
  getParcelas: () => request("/parcelas/"),
  createParcela: (payload) =>
    request("/parcelas/", { method: "POST", body: JSON.stringify(payload) }),
  getCitas: () => request("/citas/"),
  createCita: (payload) =>
    request("/citas/", { method: "POST", body: JSON.stringify(payload) }),
};
