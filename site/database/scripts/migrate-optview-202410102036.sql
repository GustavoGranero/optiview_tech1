ALTER TABLE public.files_processed ADD folder_id int8 NOT NULL;
ALTER TABLE public.files_processed ADD CONSTRAINT files_processed_folder_id_fk FOREIGN KEY (folder_id) REFERENCES public.folders(id);

INSERT INTO public.versions VALUES ('202410102036', '2024-10-10 20:36:00-03');