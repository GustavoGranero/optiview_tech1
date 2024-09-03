\connect optview

ALTER TABLE public.users ADD full_name varchar NOT NULL;

ALTER TABLE public.users RENAME COLUMN hash_type TO hash_type_id;

CREATE TABLE public.action_types (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"action_type" varchar NOT NULL,
	CONSTRAINT action_types_pk PRIMARY KEY (id)
);

INSERT INTO public.action_types ("action_type") VALUES
	 ('confirm_email'),
	 ('confirm_password_reset'),
	 ('confirm_email_change_original'),
	 ('confirm_email_change_new');


CREATE TABLE public.actions (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	action_type_id int8 NOT NULL,
	user_id int8 NOT NULL,
	"token" varchar NOT NULL,
	"timestamp" timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT actions_pk PRIMARY KEY (id),
	CONSTRAINT actions_token_unique UNIQUE (token),
	CONSTRAINT actions_action_types_fk FOREIGN KEY (action_type_id) REFERENCES public.action_types(id),
	CONSTRAINT actions_users_fk FOREIGN KEY (user_id) REFERENCES public.users(id)
);

INSERT INTO public.versions VALUES ('202408060938', '2024-08-06 09:38:00.000000-03');
