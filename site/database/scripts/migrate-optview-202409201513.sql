-- To alter a colummn typ it must not be referenced on a view
DROP VIEW public.view_plan_periods

ALTER TABLE public.plan_prices ALTER COLUMN price TYPE numeric USING price::numeric;

-- recreating the view
CREATE VIEW public.view_plan_periods AS
 SELECT p.id,
    p.name AS plan_name,
    per.name AS period_name,
    pr.price
   FROM ((public.plans p
     JOIN public.plan_prices pr ON ((p.price_id = pr.id)))
     JOIN public.plan_periods per ON ((pr.period_id = per.id)));

INSERT INTO public.versions VALUES ('202409201513', '2024-09-20 15:13:00-03');