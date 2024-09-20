CREATE TABLE public.files (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"uuid" uuid DEFAULT gen_random_uuid() NOT NULL,
	user_id int8 NOT NULL,
	folder_id int8 NOT NULL,
	"name" varchar NOT NULL,
	file bytea NOT NULL,
	CONSTRAINT files_pk PRIMARY KEY (id),
	CONSTRAINT files_uuid_unique UNIQUE ("uuid"),
	CONSTRAINT files_users_fk FOREIGN KEY (user_id) REFERENCES public.users(id),
	CONSTRAINT files_folders_fk FOREIGN KEY (folder_id) REFERENCES public.folders(id)
);

INSERT INTO public.versions VALUES ('202409191606', '2024-09-19 16:06:00-03');