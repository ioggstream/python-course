# Storage engines and temporary tables
## Engines

  - Storage Engines in MySQL Architecture
  - Memory: effects of limits
  - InnoDB: 
  - MyISAM
  

## Memory tables
Paging in MySQL and temporary tables.

Memory and (Temporary Tables)[https://dev.mysql.com/doc/refman/5.6/en/internal-temporary-tables.html].

        max_heap_table_size
        max_tmp_table_size


## Memory tables
Get raw values via

        SHOW VARIABLES LIKE '%table_size%';

Or format them via

        SELECT VARIABLE_NAME, 
            VARIABLE_VALUE>>20 
        FROM GLOBAL_VARIABLES 
        WHERE VARIABLE_NAME LIKE '%table_size';


## Creating Memory Tables
Create a small memory table...

        USE employees;
        CREATE TABLE _departments 
            ENGINE=memory
            SELECT * FROM departments;
        SHOW CREATE TABLE _departments;

...and a big one (with more than `max_heap_table_size`).

        CREATE TABLE _titles 
            ENGINE=memory
            SELECT * FROM titles;
        SHOW CREATE TABLE _titles;


## Memory
Remember that


$max\_tmp\_table\_size \leq max\_heap\_table\_size$ 


Otherwise `max_tmp_table_size` will *always* be
lowered at `max_heap_table_size` value.

Creating temporary tables. 
Limitations on [BLOB/TEXT and its effects](https://dev.mysql.com/doc/refman/5.6/en/internal-temporary-tables.html).

Inspecting temporary tables on disks.

        SHOW GLOBAL STATUS LIKE '%tmp%tables';


## MyISAM
Features of MyISAM:

  - full-text support
  
Caveats:

  - non transactional
  - no FK
  - hard to recover


## MyISAM
Create MyISAM table

        CREATE TABLE _my_departments
            ENGINE=MyISAM
            SELECT * FROM departments;
        SHOW CREATE TABLE _my_departments;

Table format:

        \! tree /var/lib/mysql/employees
        
  - .frm: table definitions
  - .myd: table data
  - .myi: table indexes for data
  
  

## InnoDB
Transactions and consistency. Foreign Keys.

InnoDB Log Files. Checkpoint interval.

Buffer Pool. Contention on Buffer Pool. Buffer pool instances.

        SHOW VARIABLES LIKE 'innodb%';
        
## Configuring InnoDB
Configuring `innodb_buffer_pool_size`.

Inspecting usage.

Configuring
 
 - `innodb_log_file_size`
 - `innodb_flush_logs_at_trx_commit`
 

## Configuring InnoDB
Tablespaces. 

Configuring and Resizing Tablespaces. AutoExtend.

Ensure ```innodb_file_per_table=1```.

Check innodb datafiles while changing tables.


## Configuring InnoDB
Setup a database with the provided configuration.

        [mysqld]
        innodb_log_file_size=4M
        innodb_buffer_pool_size=16M
        
Re-import employees and get stats via dstat and time.

Retry adding
 
        innodb_flush_log_at_trx_commit=1

## Configuring InnoDB
Test further effects of the following parameters:

        innodb_buffer_pool_size
        innodb_log_file_size
        innodb_log_files_in_group
        

## Check InnoDB Status
To access InnoDB statistics you can use:

        SHOW ENGINE INNODB STATUS \G # which may impact performance

or pick selected infos from

        SELECT ... FROM INFORMATION_SCHEMA.INNODB_*


## Transportable tablespaces

TODO