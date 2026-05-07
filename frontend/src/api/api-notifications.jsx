import apiClient from "./api-client";

/** @param {{ skip?: number; limit?: number }} [params] */
export async function getNotifications(params = {}) {
  const { skip = 0, limit = 10 } = params;
  const { data } = await apiClient.get("/notifications/", {
    params: { skip, limit },
  });
  return data;
}

/** @param {number} id */
export async function getNotificationById(id) {
  const { data } = await apiClient.get(`/notifications/${id}`);
  return data;
}

/** @param {number} userId @param {{ skip?: number; limit?: number }} [params] */
export async function getNotificationsByUser(userId, params = {}) {
  const { skip = 0, limit = 10 } = params;
  const { data } = await apiClient.get(`/notifications/user/${userId}`, {
    params: { skip, limit },
  });
  return data;
}

/** @param {number} userId @param {{ skip?: number; limit?: number }} [params] */
export async function getUnreadNotifications(userId, params = {}) {
  const { skip = 0, limit = 10 } = params;
  const { data } = await apiClient.get(
    `/notifications/user/${userId}/unread`,
    { params: { skip, limit } }
  );
  return data;
}

/**
 * @param {{ user_id: number; title: string; message: string; type: string }} payload
 */
export async function createNotification(payload) {
  const { data } = await apiClient.post("/notifications/", payload);
  return data;
}

/** @param {number} id */
export async function markAsRead(id) {
  const { data } = await apiClient.patch(`/notifications/${id}/read`);
  return data;
}
