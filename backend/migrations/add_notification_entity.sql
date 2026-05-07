-- Migración: entidad Notification
-- PostgreSQL (columna "type" citada por ser palabra reservada)

CREATE TYPE notificationtype AS ENUM ('LOAN', 'RESERVATION', 'FINE', 'SYSTEM');

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    "type" notificationtype NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX ix_notifications_user_id ON notifications(user_id);
CREATE INDEX ix_notifications_is_read ON notifications(is_read);
CREATE INDEX ix_notifications_user_read ON notifications(user_id, is_read);

-- Notas:
-- - ON DELETE CASCADE: borrar usuario elimina sus notificaciones
-- - Índice (user_id, is_read) acelera listados de no leídas
