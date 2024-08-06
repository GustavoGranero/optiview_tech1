\connect optview

ALTER TABLE public.users ADD full_name varchar NOT NULL;

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
	id int8 NOT NULL,
	action_type int8 NOT NULL,
	"user" int8 NOT NULL,
	"token" varchar NOT NULL,
	"timestamp" timestamptz NOT NULL,
	CONSTRAINT actions_pk PRIMARY KEY (id),
	CONSTRAINT actions_action_type_unique UNIQUE (action_type),
	CONSTRAINT actions_token_unique UNIQUE ("token"),
	CONSTRAINT actions_action_types_fk FOREIGN KEY (action_type) REFERENCES public.action_types(id),
	CONSTRAINT actions_users_fk FOREIGN KEY ("user") REFERENCES public.actions(id)
);

ALTER TABLE public.users RENAME COLUMN hash_type TO hash_type_id;

ALTER TABLE public.actions RENAME COLUMN action_type TO action_type_id;

ALTER TABLE public.actions RENAME COLUMN "user" TO user_id;


