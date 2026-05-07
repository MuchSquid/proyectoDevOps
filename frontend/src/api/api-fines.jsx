import apiClient from "./api-client";

/** @param {{ skip?: number; limit?: number }} [params] */
export async function getFines(params = {}) {
  const { skip = 0, limit = 10 } = params;
  const { data } = await apiClient.get("/fines/", {
    params: { skip, limit },
  });
  return data;
}

/** @param {number} id */
export async function getFineById(id) {
  const { data } = await apiClient.get(`/fines/${id}`);
  return data;
}

/** @param {number} userId @param {{ skip?: number; limit?: number }} [params] */
export async function getFinesByUser(userId, params = {}) {
  const { skip = 0, limit = 10 } = params;
  const { data } = await apiClient.get(`/fines/user/${userId}`, {
    params: { skip, limit },
  });
  return data;
}

/**
 * @param {{ user_id: number; loan_id: number; amount: string | number; reason: string }} payload
 */
export async function createFine(payload) {
  const { data } = await apiClient.post("/fines/", payload);
  return data;
}

/** @param {number} id */
export async function payFine(id) {
  const { data } = await apiClient.patch(`/fines/${id}/pay`);
  return data;
}

/** @param {number} id */
export async function cancelFine(id) {
  const { data } = await apiClient.patch(`/fines/${id}/cancel`);
  return data;
}
