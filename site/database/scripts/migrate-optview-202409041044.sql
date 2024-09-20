CREATE TABLE public.plan_periods (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NOT NULL,
	"period" interval NOT NULL,
	name_plural varchar NOT NULL,
	unit_name varchar NOT NULL,
	CONSTRAINT plan_periods_name_plural_unique UNIQUE (name_plural),
	CONSTRAINT plan_periods_name_unique UNIQUE (name),
	CONSTRAINT plan_periods_pk PRIMARY KEY (id),
	CONSTRAINT plan_periods_unit_name_unique UNIQUE (unit_name)
);

INSERT INTO public.plan_periods (id,"name","period",name_plural,unit_name) OVERRIDING SYSTEM VALUE VALUES (1,'Mensal','1 mon'::interval,'Mensais', 'Mês');
INSERT INTO public.plan_periods (id,"name","period",name_plural,unit_name) OVERRIDING SYSTEM VALUE VALUES (2,'Anual','1 year'::interval,'Anuais', 'Ano');

CREATE TABLE public.currencies (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	"name" varchar NOT NULL,
	name_plural varchar NOT NULL,
	symbol varchar NOT NULL,
	CONSTRAINT currencies_pk PRIMARY KEY (id),
	CONSTRAINT currencies_name_unique UNIQUE (name),
	CONSTRAINT currencies_name_plural_unique UNIQUE (name_plural),
	CONSTRAINT currencies_symbol_unique UNIQUE (symbol)
);

INSERT INTO public.currencies (id,"name",name_plural,symbol) OVERRIDING SYSTEM VALUE VALUES (1,'Real','Reais','R$');
INSERT INTO public.currencies (id,"name",name_plural,symbol) OVERRIDING SYSTEM VALUE VALUES (2,'Dólar','Dólares','US$');

CREATE TABLE public.plan_prices (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	price money NOT NULL,
	currency_id int8 NOT NULL,
	period_id int8 NULL,
	CONSTRAINT plan_prices_pk PRIMARY KEY (id)
);

ALTER TABLE public.plan_prices ADD CONSTRAINT plan_prices_currencies_fk FOREIGN KEY (currency_id) REFERENCES currencies(id);
ALTER TABLE public.plan_prices ADD CONSTRAINT plan_prices_plan_periods_fk FOREIGN KEY (period_id) REFERENCES plan_periods(id);

INSERT INTO public.plan_prices (id,price,currency_id,period_id) OVERRIDING SYSTEM VALUE VALUES (1,0.0,1,NULL);
INSERT INTO public.plan_prices (id,price,currency_id,period_id) OVERRIDING SYSTEM VALUE VALUES (2,67.9,1,1);
INSERT INTO public.plan_prices (id,price,currency_id,period_id) OVERRIDING SYSTEM VALUE VALUES (3,390.9,1,1);
INSERT INTO public.plan_prices (id,price,currency_id,period_id) OVERRIDING SYSTEM VALUE VALUES (4,730.9,1,2);
INSERT INTO public.plan_prices (id,price,currency_id,period_id) OVERRIDING SYSTEM VALUE VALUES (5,3982.9,1,2);

ALTER TABLE public."plans" ADD price_id int8 NULL;
ALTER TABLE public."plans" ADD CONSTRAINT plans_plan_prices_fk FOREIGN KEY (price_id) REFERENCES plan_prices(id);

INSERT INTO public."plans" (id,"name",price_id) OVERRIDING SYSTEM VALUE VALUES (1,'Gratuito',1) ON CONFLICT(id) DO UPDATE SET name = EXCLUDED.name, price_id = EXCLUDED.price_id;
INSERT INTO public."plans" (id,"name",price_id) OVERRIDING SYSTEM VALUE VALUES (2,'Individual Mensal',2) ON CONFLICT(id) DO UPDATE SET name = EXCLUDED.name, price_id = EXCLUDED.price_id;
INSERT INTO public."plans" (id,"name",price_id) OVERRIDING SYSTEM VALUE VALUES (3,'Empresarial Mensal',3) ON CONFLICT(id) DO UPDATE SET name = EXCLUDED.name, price_id = EXCLUDED.price_id;
INSERT INTO public."plans" (id,"name",price_id) OVERRIDING SYSTEM VALUE VALUES (4,'Individual Anual',4) ON CONFLICT(id) DO UPDATE SET name = EXCLUDED.name, price_id = EXCLUDED.price_id;
INSERT INTO public."plans" (id,"name",price_id) OVERRIDING SYSTEM VALUE VALUES (5,'Empresarial Anual',5) ON CONFLICT(id) DO UPDATE SET name = EXCLUDED.name, price_id = EXCLUDED.price_id;

ALTER TABLE public."plans" ALTER COLUMN price_id SET NOT NULL;

CREATE TABLE public.plan_resources (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NOT NULL,
	name_singular varchar NOT NULL,
	CONSTRAINT plan_resources_name_singular_unique UNIQUE (name_singular),
	CONSTRAINT plan_resources_name_unique UNIQUE (name),
	CONSTRAINT plan_resources_pk PRIMARY KEY (id)
);

INSERT INTO public.plan_resources (id,"name",name_singular) OVERRIDING SYSTEM VALUE VALUES (1,'Usos de IA','Uso de IA');
INSERT INTO public.plan_resources (id,"name",name_singular) OVERRIDING SYSTEM VALUE VALUES (2,'Usuários','Usuário');
INSERT INTO public.plan_resources (id,"name",name_singular) OVERRIDING SYSTEM VALUE VALUES (3,'Projetos','Projeto');

CREATE TABLE public.plan_resource_limits (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	plan_id int8 NOT NULL,
	resource_id int8 NOT NULL,
	"limit" int8 NULL,
	period_id int8 NULL,
	CONSTRAINT plan_resource_limits_pk PRIMARY KEY (id)
);

ALTER TABLE public.plan_resource_limits ADD CONSTRAINT plan_resource_limits_plan_periods_fk FOREIGN KEY (period_id) REFERENCES plan_periods(id);
ALTER TABLE public.plan_resource_limits ADD CONSTRAINT plan_resource_limits_plan_resources_fk FOREIGN KEY (resource_id) REFERENCES plan_resources(id);
ALTER TABLE public.plan_resource_limits ADD CONSTRAINT plan_resource_limits_plans_fk FOREIGN KEY (plan_id) REFERENCES "plans"(id);

INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (1,1,1,10,NULL);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (2,1,2,1,NULL);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (3,1,3,1,NULL);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (4,2,1,100,1);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (5,2,2,1,NULL);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (6,2,3,NULL,NULL);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (7,3,1,500,1);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (8,3,2,5,NULL);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (9,3,3,NULL,NULL);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (10,4,1,1200,2);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (11,4,2,1,NULL);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (12,4,3,NULL,NULL);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (13,5,1,6000,2);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (14,5,2,NULL,NULL);
INSERT INTO public.plan_resource_limits (id,plan_id,resource_id,"limit",period_id) OVERRIDING SYSTEM VALUE VALUES (15,5,3,NULL,NULL);

CREATE VIEW public.view_plan_periods AS
 SELECT p.id,
    p.name AS plan_name,
    per.name AS period_name,
    pr.price
   FROM ((public.plans p
     JOIN public.plan_prices pr ON ((p.price_id = pr.id)))
     JOIN public.plan_periods per ON ((pr.period_id = per.id)));


CREATE VIEW public.view_resources_limits AS
 SELECT rl.id,
    p.name AS plan_name,
    p_pri_per.name AS plan_period,
    pr.name AS resource_name,
    rl."limit",
    per.name AS period_name
   FROM (((((public.plan_resource_limits rl
     JOIN public.plans p ON ((rl.plan_id = p.id)))
     JOIN public.plan_prices pri ON ((p.price_id = pri.id)))
     LEFT JOIN public.plan_periods p_pri_per ON ((pri.period_id = p_pri_per.id)))
     JOIN public.plan_resources pr ON ((rl.resource_id = pr.id)))
     LEFT JOIN public.plan_periods per ON ((rl.period_id = per.id)))
  ORDER BY p.id;

INSERT INTO public.versions VALUES ('202409041044', '2024-09-04 10:44:00-03');