import apiClient from "./api-client";

/** @param {{ skip?: number; limit?: number }} [params] */
export async function getUsers(params = {}) {
  const { skip = 0, limit = 10 } = params;
  const { data } = await apiClient.get("/users/", {
    params: { skip, limit },
  });
  return data;
}

/** @param {number} id */
export async function getUserById(id) {
  const { data } = await apiClient.get(`/users/${id}`);
  return data;
}

/** @param {Record<string, unknown>} payload */
export async function createUser(payload) {
  const { data } = await apiClient.post("/users/", payload);
  return data;
}

/** @param {number} id @param {Record<string, unknown>} payload */
export async function updateUser(id, payload) {
  const { data } = await apiClient.put(`/users/${id}`, payload);
  return data;
}

/** @param {number} id */
export async function deleteUser(id) {
  await apiClient.delete(`/users/${id}`);
}
