ALTER TABLE public.files_processed_types ADD "name" varchar NULL;
ALTER TABLE public.files_processed_types ADD CONSTRAINT files_processed_types_name_unique UNIQUE ("name");

UPDATE files_processed_types SET "name" = 'Imagem extraída' WHERE id = 1
UPDATE files_processed_types SET "name" = 'Planta' WHERE id = 2
UPDATE files_processed_types SET "name" = 'Legenda' WHERE id = 3

ALTER TABLE public.files_processed_types ALTER COLUMN "name" SET NOT NULL;

INSERT INTO public.versions VALUES ('202410090851', '2024-10-09 00:08:51-03');
