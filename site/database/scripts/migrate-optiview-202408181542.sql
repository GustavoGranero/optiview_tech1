ALTER TABLE public.users ADD phone_normalized varchar NOT NULL;
ALTER TABLE public.users ADD CONSTRAINT users_phone_normalized_unique UNIQUE (phone_normalized);