
# Import/Export

## Goal

  - Importing and Exporting data
  - AUTOCOMMIT
  - Cloning tables
  - Effects of logging on imports


## Populating a database
While monitoring system status with
 
         dstat -cgmprsy 5
    
import the [Employees database](http://bit.ly/1qEutCs) 

        wget http://bit.ly/1qEutCs -O employees.tar.gz
        tar xf employees.tar.gz -C /opt
        cd /opt/employee*
        mysql < employees.sql

Exercise: how does `employees.sql` work?

## Populating a database

Dump a table in a file once `secure-file-priv` is enabled.

        SELECT * 
            INTO OUTFILE '/var/lib/mysql-files/path.tsv'
            FROM departments;
        CREATE TABLE _departments LIKE departments;
        LOAD DATA INFILE 'path.tsv' INTO TABLE _departments;


## Populating a database
Show database structure 

        STATUS;
        SELECT DATABASE();
        USE employee
        SELECT DATABASE();
        SHOW TABLE STATUS \G
        
Table size in $MiB$ $2^{20}$ bytes

        USE information_schema;
            SELECT TABLE_NAME, DATA_LENGTH>>20, INDEX_LENGTH>>20 
        FROM TABLES
        WHERE TABLE_SCHEMA='employees';
        

## Exporting data
Export  `employee` with the following parameter

     mysqldump employees --tables salaries   \
        --skip-extended-insert  | 
            gzip  > salaries.sql.gz
        
Import and monitor with `dstat` using: 
        
        SET AUTOCOMMIT=1
        SELECT @@AUTOCOMMIT;
        
Exercise: explain the server behavior.


## Autocommit

`AUTOCOMMIT` is true by default.

In transactions, AUTOCOMMIT is disabled, unless you issue:

  - DDL
  - GRANT, REVOKE
  - {UN,}LOCK TABLES

This is called **implicit commit**

## Autocommit

Prepare a new table to experiment with:

  - transactions
  - autocommit


        CREATE TABLE d1.t5 (
           id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
           name VARCHAR(12) DEFAULT "def"
        );
        INSERT INTO d1.t5(id) VALUES (1), (2), (3); 


## Autocommit

Exercise: 

        BEGIN; 
        INSERT INTO d1.t5(name) VALUES('implicit'); 
        CREATE TABLE d1.deleteme(b BINARY);   -- the first time try without adding this line.
        ROLLBACK; 
        SELECT * FROM t5;

## Autocommit

Exercise: 

        BEGIN; 
        INSERT INTO d1.t5(name) VALUES('implicit'); 
        DROP TABLE d1.deleteme;   
        INSERT INTO d1.t5(name) VALUES('rollback');  -- check this now!
        ROLLBACK; 
        SELECT * FROM t5;


## Autocommit

Remember:

  - avoid mixing DDL and DML

  - check [the docs of your actual mysql version](https://dev.mysql.com/doc/refman/5.7/en/implicit-commit.html)

## Autocommit

Exercise: which is the expected output of this commands? Which will end first? And last?

        
        mysql -e 'BEGIN; UPDATE d1.t1 SET name="i1" WHERE id="1"; SELECT SLEEP(10) as 'one'; COMMIT' &
        sleep .1
        mysql -e 'BEGIN; UPDATE d1.t1 SET name="i2" WHERE id="1"; SELECT SLEEP(2) as 'two'; COMMIT'  &
        sleep .1
        mysql -e 'BEGIN; UPDATE d1.t1 SET name="i3" WHERE id="3"; SELECT SLEEP(2) as 'three'; COMMIT'  &

Rememeber: 

  - InnoDB locks selected rows in every transaction by default!
  - Other engines require SELECT ... LOCK IN SHARE MODE
     
     
        
