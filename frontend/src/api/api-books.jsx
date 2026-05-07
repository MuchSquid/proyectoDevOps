import apiClient from "./api-client";

/** @param {{ skip?: number; limit?: number }} [params] */
export async function getBooks(params = {}) {
  const { skip = 0, limit = 10 } = params;
  const { data } = await apiClient.get("/books/", {
    params: { skip, limit },
  });
  return data;
}

/** @param {number} id */
export async function getBookById(id) {
  const { data } = await apiClient.get(`/books/${id}`);
  return data;
}

/** @param {Record<string, unknown>} payload */
export async function createBook(payload) {
  const { data } = await apiClient.post("/books/", payload);
  return data;
}

/** @param {number} id @param {Record<string, unknown>} payload */
export async function updateBook(id, payload) {
  const { data } = await apiClient.put(`/books/${id}`, payload);
  return data;
}

/** @param {number} id */
export async function deleteBook(id) {
  await apiClient.delete(`/books/${id}`);
}
