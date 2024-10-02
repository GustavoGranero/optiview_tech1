CREATE TABLE files_processed (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"uuid" uuid DEFAULT gen_random_uuid() NOT NULL,
	user_id int8 NOT NULL,
	parent_file_id int8 NOT NULL,
	"name" varchar NOT NULL,
	file bytea NOT NULL,
	CONSTRAINT files_processed_pk PRIMARY KEY (id),
	CONSTRAINT files_processed_unique UNIQUE (uuid),
	CONSTRAINT files_processed_parent_file_id_fk FOREIGN KEY (parent_file_id) REFERENCES files(id),
	CONSTRAINT files_processed_user_id_fk FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO public.versions VALUES ('202410020013', '2024-10-02 00:13:00-03');
