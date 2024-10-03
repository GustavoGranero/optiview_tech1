CREATE TABLE public.files_processed_types (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	file_processed_type varchar NOT NULL,
	CONSTRAINT files_processed_types_pk PRIMARY KEY (id),
	CONSTRAINT files_processed_types_unique UNIQUE (file_processed_type)
);

INSERT INTO public.files_processed_types (id,file_processed_type) OVERRIDING SYSTEM VALUE VALUES (1,'extracted_image');
INSERT INTO public.files_processed_types (id,file_processed_type) OVERRIDING SYSTEM VALUE VALUES (2,'plan');
INSERT INTO public.files_processed_types (id,file_processed_type) OVERRIDING SYSTEM VALUE VALUES (3,'legend');

CREATE TABLE files_processed (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"uuid" uuid DEFAULT gen_random_uuid() NOT NULL,
	user_id int8 NOT NULL,
	parent_file_id int8 NOT NULL,
	"name" varchar NOT NULL,
	file bytea NOT NULL,
	processed_type_id int8 NOT NULL,
	CONSTRAINT files_processed_pk PRIMARY KEY (id),
	CONSTRAINT files_processed_unique UNIQUE (uuid),
	CONSTRAINT files_processed_parent_file_id_fk FOREIGN KEY (parent_file_id) REFERENCES files(id) ON DELETE CASCADE,
	CONSTRAINT files_processed_type_id FOREIGN KEY (processed_type_id) REFERENCES files_processed_types(id),
	CONSTRAINT files_processed_user_id_fk FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO public.versions VALUES ('202410020013', '2024-10-02 00:13:00-03');
