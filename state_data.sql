
CREATE SCHEMA IF NOT EXISTS summersalt;

CREATE TABLE IF NOT EXISTS summersalt.state_data(
    id serial NOT NULL PRIMARY KEY,
    state TEXT NOT NULL,
    year TEXT NOT NULL,
    total_grads NUMERIC NOT NULL,
    total_grads_engineer NUMERIC NOT NULL,
    percentage_grads_engineer TEXT NOT NULL,
    total_wage_estimate NUMERIC NOT NULL,
    total_wage_estimate_engineer NUMERIC NOT NULL,
    percentage_wage_engineer TEXT
);