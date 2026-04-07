BEGIN TRANSACTION;
ALTER TABLE pacientes ADD COLUMN fecha_ultimo_control TEXT;
UPDATE pacientes SET fecha_ultimo_control = '2026-03-01' WHERE fecha_ultimo_control IS NULL;
COMMIT;
