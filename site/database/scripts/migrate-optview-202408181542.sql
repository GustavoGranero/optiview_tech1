ALTER TABLE public.users ADD phone_normalized varchar NOT NULL;
ALTER TABLE public.users ADD CONSTRAINT users_phone_normalized_unique UNIQUE (phone_normalized);

INSERT INTO public.versions VALUES ('202408181542', '2024-08-18 15:42:00.000000-03');