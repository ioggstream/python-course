# Storage engines and temporary tables
## Engines

  - Storage Engines in MySQL Architecture
  - InnoDB
  - Memory
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

$max_tmp_table_size \leq max_heap_table_size$ 

Otherwise `max_tmp_table_size` will *always* be
lowered at `max_heap_table_size` value.

Creating temporary tables. 
Limitations on [BLOB/TEXT and its effects][https://dev.mysql.com/doc/refman/5.6/en/internal-temporary-tables.html].

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
Table format:

  - .frm: table definitions
  - .myd: table data
  - .myi: table indexes for data
  

## InnoDB
Transactions and consistency. Foreign Keys.

InnoDB Log Files. Checkpoint interval.

Buffer Pool. Contention on Buffer Pool. Buffer pool instances.


## Configuring InnoDB
Configuring `innodb_buffer_pool_size`.

Inspecting usage.

Configuring
 
 - `innodb_log_file_size`
 - `innodb_flush_logs_at_trx_commit`
 

## Configuring InnoDB
Tablespaces. 

Configuring and Resizing Tablespaces. AutoExtend.

Ensure innodb_file_per_table=1.

Check innodb datafiles while changing tables.



