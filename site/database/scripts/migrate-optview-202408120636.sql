ALTER TABLE public.users ADD login_failure_timestamp timestamptz NULL;
ALTER TABLE public.actions ADD executed_timestamp timestamptz NULL;

INSERT INTO public.versions VALUES ('202408120636', '2024-07-12 06:36:00.000000-03');