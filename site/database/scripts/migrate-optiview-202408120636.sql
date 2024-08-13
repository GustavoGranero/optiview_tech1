ALTER TABLE public.users ADD last_login_failure_timestamp timestamptz NULL;

ALTER TABLE public.actions ADD executed_timestamp timestamptz NULL;