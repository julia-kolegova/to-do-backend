DO $$
BEGIN
    IF NOT EXISTS (SELECT 1
                   FROM pg_type
                   WHERE typname = 'priority'
                     AND typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')) THEN
        CREATE TYPE public."priority" AS ENUM (
            'HIGH',
            'MEDIUM',
            'LOW',
            'NAN'
        );
    END IF;
END
$$;