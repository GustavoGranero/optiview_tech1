CREATE TABLE public.folders (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"uuid" uuid DEFAULT gen_random_uuid() NOT NULL,
	user_id int8 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT folders_name_unique UNIQUE (name),
	CONSTRAINT folders_pk PRIMARY KEY (id),
	CONSTRAINT folders_uuid_unique UNIQUE (uuid),
	CONSTRAINT folders_users_fk FOREIGN KEY (user_id) REFERENCES public.users(id)
);

INSERT INTO public.versions VALUES ('202409161614', '2024-09-16 16:14:00.000000-03');