-- Migración: entidad Fine (multas por préstamo)
-- PostgreSQL

CREATE TYPE finestatus AS ENUM ('PENDING', 'PAID', 'CANCELLED');

CREATE TABLE fines (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    loan_id INTEGER NOT NULL REFERENCES loans(id) ON DELETE CASCADE,
    amount NUMERIC(12, 2) NOT NULL,
    reason TEXT NOT NULL,
    status finestatus NOT NULL DEFAULT 'PENDING',
    issued_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    paid_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX ix_fines_user_id ON fines(user_id);
CREATE INDEX ix_fines_loan_id ON fines(loan_id);
CREATE INDEX ix_fines_status ON fines(status);
CREATE INDEX ix_fines_user_status ON fines(user_id, status);

-- Notas:
-- - Sin FK a books: el libro se obtiene vía loan
-- - ON DELETE CASCADE en user_id y loan_id elimina multas al borrar usuario o préstamo
-- - Varias multas por préstamo permitidas (futuro: multas automáticas)
