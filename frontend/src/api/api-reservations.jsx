import apiClient from "./api-client";

/** @param {{ skip?: number; limit?: number }} [params] */
export async function getReservations(params = {}) {
  const { skip = 0, limit = 10 } = params;
  const { data } = await apiClient.get("/reservations/", {
    params: { skip, limit },
  });
  return data;
}

/** @param {number} id */
export async function getReservationById(id) {
  const { data } = await apiClient.get(`/reservations/${id}`);
  return data;
}

/** @param {number} userId @param {{ skip?: number; limit?: number }} [params] */
export async function getReservationsByUser(userId, params = {}) {
  const { skip = 0, limit = 10 } = params;
  const { data } = await apiClient.get(`/reservations/user/${userId}`, {
    params: { skip, limit },
  });
  return data;
}

/** @param {Record<string, unknown>} payload */
export async function createReservation(payload) {
  const { data } = await apiClient.post("/reservations/", payload);
  return data;
}

/** @param {number} id */
export async function cancelReservation(id) {
  const { data } = await apiClient.patch(`/reservations/${id}/cancel`);
  return data;
}

/** @param {number} id */
export async function completeReservation(id) {
  const { data } = await apiClient.patch(`/reservations/${id}/complete`);
  return data;
}
