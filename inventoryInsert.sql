use hotel_database;
create table inventory (
  id varchar(7) PRIMARY KEY,
  name varchar(20) unique,
  quantity float,
  ppq float
);
describe inventory;
-- drop table inventory;
/* INSERT CONTENTS INTO INVENTORY */
-- insert into
--   inventory
-- values('VG1', 'Potato', 3, 10);
-- insert into
--   inventory
-- values('VG2', 'Cucumber', 2, 15);
-- insert into
--   inventory
-- values('VG3', 'Tomato', 2, 10);
-- insert into
--   inventory
-- values('VG4', 'Onion', 3, 20);
-- insert into
--   inventory
-- values('VG5', 'Capsicum', 2, 15);
-- insert into
--   inventory
-- values('VG6', 'Mushroom', 6, 20);
-- insert into
--   inventory
-- values('ML1', 'Cheese', 1, 20);
-- insert into
--   inventory
-- values('ML2', 'Paneer', 1, 25);
-- insert into
--   inventory
-- values('NVG1', 'Chicken', 1, 300);
-- insert into
--   inventory
-- values('NVG2', 'Mutton', 2, 450);
-- insert into
--   inventory
-- values('TP1', 'Tomato Ketchup', 4, 10);
-- insert into
--   inventory
-- values('TP2', 'Mayonaise', 5, 19);
-- insert into
--   inventory
-- values('BD1', 'Bread', 2, 5);
-- insert into
--   inventory
-- values('BD2', 'Pizza Base Bread', 3, 11);
-- insert into
--   inventory
-- values('BD3', 'Pav', 4, 6);
/* SHOW INVENTORY */
-- run excelInsert.py to insert values in the table
select
  *
from
  inventory;