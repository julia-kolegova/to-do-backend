DO $$
BEGIN
    IF NOT EXISTS (SELECT 1
                   FROM pg_type
                   WHERE typname = 'taskstatus'
                     AND typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')) THEN
        CREATE TYPE public."taskstatus" AS ENUM (
            'ACTIV',
            'SOLVED',
            'DELETED',
            'ARCHIVED'
        );
    END IF;
END
$$;