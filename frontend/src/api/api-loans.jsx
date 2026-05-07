import apiClient from "./api-client";

/** @param {{ skip?: number; limit?: number }} [params] */
export async function getLoans(params = {}) {
  const { skip = 0, limit = 10 } = params;
  const { data } = await apiClient.get("/loans/", {
    params: { skip, limit },
  });
  return data;
}

/** @param {number} id */
export async function getLoanById(id) {
  const { data } = await apiClient.get(`/loans/${id}`);
  return data;
}

/** @param {number} userId @param {{ skip?: number; limit?: number }} [params] */
export async function getLoansByUser(userId, params = {}) {
  const { skip = 0, limit = 10 } = params;
  const { data } = await apiClient.get(`/loans/user/${userId}`, {
    params: { skip, limit },
  });
  return data;
}

/** @param {Record<string, unknown>} payload */
export async function createLoan(payload) {
  const { data } = await apiClient.post("/loans/", payload);
  return data;
}

/** @param {number} id */
export async function returnLoan(id) {
  const { data } = await apiClient.patch(`/loans/${id}/return`);
  return data;
}

/** @param {number} id */
export async function cancelLoan(id) {
  const { data } = await apiClient.patch(`/loans/${id}/cancel`);
  return data;
}
