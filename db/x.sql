CREATE EXTENSION IF NOT EXISTS citus;
CREATE EXTENSION IF NOT EXISTS citus_columnar;
create table x
(
    id           serial           not null primary key,
    month        date             not null,
    count        integer          not null,
    ratios       double precision not null,
    sample_count integer          not null
) using columnar;;
