
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

        bash#wget http://bit.ly/1qEutCs -O employees.tar.gz     
        bash#tar xf employee*
        bash#cd employee*
        bash#mysql < employees.sql

Exercise: how does `employees.sql` work?

        SELECT * INTO OUTFILE 'path.tsv' FROM departments;
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

     mysqldump -proot employees \
        --table salaries   \
        --skip-extended-insert  | 
            gzip  > salaries.sql   
        
Import and monitor with `dstat` using: 
        
        SET AUTOCOMMIT=1
        SELECT @@AUTOCOMMIT;
        
Exercise: explain the server behavior.


     
     
        
