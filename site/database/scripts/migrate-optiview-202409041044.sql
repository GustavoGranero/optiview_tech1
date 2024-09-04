CREATE TABLE public.plan_periods (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"name" varchar NOT NULL,
	"period" interval NOT NULL,
	CONSTRAINT plan_periods_pk PRIMARY KEY (id)
);

INSERT INTO public.plan_periods (id,"name","period") VALUES (1,'Mensal','1 mon'::interval);
INSERT INTO public.plan_periods (id,"name","period") VALUES (2,'Anual','1 year'::interval);

CREATE TABLE currency (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"name" varchar NOT NULL,
	name_plural varchar NOT NULL,
	symbol varchar NOT NULL,
	CONSTRAINT currency_pk PRIMARY KEY (id)
);

INSERT INTO public.currency (id,"name",name_plural,symbol) OVERRIDING SYSTEM VALUE VALUES (1,'Real','Reais','R$');
INSERT INTO public.currency (id,"name",name_plural,symbol) OVERRIDING SYSTEM VALUE VALUES (2,'Dolar','Dólares','US$');

CREATE TABLE plan_prices (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	price money NOT NULL,
	id_currency int8 NOT NULL,
	id_period int8 NULL,
	CONSTRAINT plan_prices_pk PRIMARY KEY (id)
);

ALTER TABLE public.plan_prices ADD CONSTRAINT plan_prices_currency_fk FOREIGN KEY (id_currency) REFERENCES currency(id);
ALTER TABLE public.plan_prices ADD CONSTRAINT plan_prices_plan_periods_fk FOREIGN KEY (id_period) REFERENCES plan_periods(id);

INSERT INTO public.plan_prices (id,price,id_currency,id_period) VALUES (1,R$ 0,00,1,1);
INSERT INTO public.plan_prices (id,price,id_currency,id_period) VALUES (2,R$ 67,90,1,1);
INSERT INTO public.plan_prices (id,price,id_currency,id_period) VALUES (3,R$ 390,90,1,1);
INSERT INTO public.plan_prices (id,price,id_currency,id_period) VALUES (4,R$ 730,90,1,2);
INSERT INTO public.plan_prices (id,price,id_currency,id_period) VALUES (5,R$ 3.982,90,1,2);

ALTER TABLE public."plans" ADD id_price int8 NULL;
ALTER TABLE public."plans" ADD CONSTRAINT plans_plan_prices_fk FOREIGN KEY (id_price) REFERENCES plan_prices(id);

INSERT INTO public."plans" (id,"name",id_price) OVERRIDING SYSTEM VALUE VALUES (1,'Gratuito',1) ON CONFLICT(id) DO UPDATE SET name = EXCLUDED.name, id_price = EXCLUDED.id_price;
INSERT INTO public."plans" (id,"name",id_price) OVERRIDING SYSTEM VALUE VALUES (2,'Individual Mensal',2) ON CONFLICT(id) DO UPDATE SET name = EXCLUDED.name, id_price = EXCLUDED.id_price;
INSERT INTO public."plans" (id,"name",id_price) OVERRIDING SYSTEM VALUE VALUES (3,'Empresarial Mensal',3) ON CONFLICT(id) DO UPDATE SET name = EXCLUDED.name, id_price = EXCLUDED.id_price;
INSERT INTO public."plans" (id,"name",id_price) OVERRIDING SYSTEM VALUE VALUES (4,'Individual Anual',4) ON CONFLICT(id) DO UPDATE SET name = EXCLUDED.name, id_price = EXCLUDED.id_price;
INSERT INTO public."plans" (id,"name",id_price) OVERRIDING SYSTEM VALUE VALUES (5,'Empresarial Anual',5) ON CONFLICT(id) DO UPDATE SET name = EXCLUDED.name, id_price = EXCLUDED.id_price;

ALTER TABLE public."plans" ALTER COLUMN id_price SET NOT NULL;

CREATE TABLE plan_resources (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT plan_resources_pk PRIMARY KEY (id)
);

INSERT INTO public.plan_resources (id,"name") OVERRIDING SYSTEM VALUE VALUES (1,'Usos de IA');
INSERT INTO public.plan_resources (id,"name") OVERRIDING SYSTEM VALUE VALUES (2,'Usuários');
INSERT INTO public.plan_resources (id,"name") OVERRIDING SYSTEM VALUE VALUES (3,'Projetos');

CREATE TABLE plan_resource_limits (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	id_plan int8 NOT NULL,
	id_resource int8 NOT NULL,
	"limit" int8 NULL,
	id_period int8 NULL,
	CONSTRAINT plan_resource_limits_pk PRIMARY KEY (id)
);


ALTER TABLE public.plan_resource_limits ADD CONSTRAINT plan_resource_limits_plan_periods_fk FOREIGN KEY (id_period) REFERENCES plan_periods(id);
ALTER TABLE public.plan_resource_limits ADD CONSTRAINT plan_resource_limits_plan_resources_fk FOREIGN KEY (id_resource) REFERENCES plan_resources(id);
ALTER TABLE public.plan_resource_limits ADD CONSTRAINT plan_resource_limits_plans_fk FOREIGN KEY (id_plan) REFERENCES "plans"(id);

INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (1,1,1,10,1);
INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (2,1,2,1,NULL);
INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (3,1,3,1,NULL);
INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (4,2,1,100,1);
INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (5,2,2,1,NULL);
INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (6,2,3,2,NULL);
INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (7,3,1,500,2);
INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (8,3,2,5,NULL);
INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (9,3,3,NULL,NULL);
INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (10,4,1,1200,2);
INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (11,4,2,1,NULL);
INSERT INTO public.plan_resource_limits (id,id_plan,id_resource,"limit",id_period) OVERRIDING SYSTEM VALUE VALUES (12,4,3,NULL,NULL);


