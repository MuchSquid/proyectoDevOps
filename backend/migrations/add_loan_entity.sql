-- Migraciones para agregar la entidad Loan al sistema de biblioteca
-- Ejecutar en orden secuencial en PostgreSQL

-- 1. Agregar campo available_copies a la tabla books
ALTER TABLE books ADD COLUMN available_copies INTEGER NOT NULL DEFAULT 1;

-- 2. Crear índice para available_copies
CREATE INDEX ix_books_available_copies ON books(available_copies);

-- 3. Crear enum LoanStatus
CREATE TYPE loanstatus AS ENUM ('ACTIVE', 'RETURNED', 'OVERDUE', 'CANCELLED');

-- 4. Crear tabla loans
CREATE TABLE loans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    loan_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    due_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW() + INTERVAL '14 days',
    returned_at TIMESTAMP WITH TIME ZONE,
    status loanstatus NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- 5. Crear índices para loans
CREATE INDEX ix_loans_user_id ON loans(user_id);
CREATE INDEX ix_loans_book_id ON loans(book_id);
CREATE INDEX ix_loans_status ON loans(status);

-- 6. Crear índice compuesto para queries comunes (opcional, para optimización)
CREATE INDEX ix_loans_user_status ON loans(user_id, status);
CREATE INDEX ix_loans_book_status ON loans(book_id, status);

-- Notas:
-- - Los FKs tienen ON DELETE CASCADE para eliminar préstamos cuando se elimina usuario o libro
-- - due_date se calcula automáticamente como loan_date + 14 días
-- - El campo available_copies en books tiene default=1 para compatibilidad con datos existentes
-- - Los índices optimizan queries de préstamos por usuario, libro y estado
