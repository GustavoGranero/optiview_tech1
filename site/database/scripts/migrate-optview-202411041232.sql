INSERT INTO public.files_processed_types (id,file_processed_type,"name") OVERRIDING SYSTEM VALUE VALUES (4,'result','Resultado');

CREATE TABLE files_processed_results (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	plan_file_id int8 NOT NULL,
	code varchar NOT NULL,
	description varchar NULL,
	image_plan bytea NOT NULL,
	image_plan_box json NOT NULL,
	image_table_line bytea NULL,
	image_table_line_box json NULL,
	CONSTRAINT files_processed_results_pk PRIMARY KEY (id)
);

ALTER TABLE public.files_processed_results ADD CONSTRAINT files_processed_results_files_processed_fk FOREIGN KEY (plan_file_id) REFERENCES public.files_processed(id) ON DELETE CASCADE;


INSERT INTO public.versions VALUES ('202411041232', '2024-11-04 12:32:00-03');