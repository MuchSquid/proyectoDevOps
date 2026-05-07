-- Migraciones para agregar la entidad Reservation al sistema de biblioteca
-- Ejecutar en orden secuencial en PostgreSQL

-- 1. Crear enum ReservationStatus
CREATE TYPE reservationstatus AS ENUM ('ACTIVE', 'COMPLETED', 'CANCELLED', 'EXPIRED');

-- 2. Crear tabla reservations
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    reservation_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    expiration_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW() + INTERVAL '3 days',
    status reservationstatus NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- 3. Crear índices para reservations
CREATE INDEX ix_reservations_user_id ON reservations(user_id);
CREATE INDEX ix_reservations_book_id ON reservations(book_id);
CREATE INDEX ix_reservations_status ON reservations(status);

-- 4. Crear índice compuesto para queries comunes
CREATE INDEX ix_reservations_user_status ON reservations(user_id, status);
CREATE INDEX ix_reservations_book_status ON reservations(book_id, status);

-- 5. Crear unique constraint para evitar reservas duplicadas activas del mismo libro por usuario
CREATE UNIQUE INDEX ux_reservations_user_book_active 
ON reservations(user_id, book_id) 
WHERE status = 'ACTIVE';

-- Notas:
-- - Los FKs tienen ON DELETE CASCADE para eliminar reservas cuando se elimina usuario o libro
-- - expiration_date se calcula automáticamente como reservation_date + 3 días
-- - El unique constraint evita que un usuario tenga múltiples reservas ACTIVE del mismo libro
-- - Los índices optimizan queries de reservas por usuario, libro y estado
