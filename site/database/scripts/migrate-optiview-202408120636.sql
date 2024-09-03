ALTER TABLE public.users ADD login_failure_timestamp timestamptz NULL;

ALTER TABLE public.actions ADD executed_timestamp timestamptz NULL;