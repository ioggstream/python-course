# Storage engines and temporary tables
## Engines

  - Storage Engines in MySQL Architecture
  - Memory: effects of limits
  - InnoDB:
  - MyISAM


## Memory tables
"Paging" in MySQL and temporary tables.

Memory and [Temporary Tables](https://dev.mysql.com/doc/refman/5.7/en/internal-temporary-tables.html).

        max_heap_table_size
        max_tmp_table_size

Memory tables:

  - don't persist at restatrt
  - dont' support foreign keys
  - don't support `BLOB|TEXT`

## Memory tables
Get raw values via

        SHOW VARIABLES LIKE '%table_size%';

Or format them via

        SELECT VARIABLE_NAME,
            VARIABLE_VALUE>>20
          FROM performance_schema.global_variables
          WHERE VARIABLE_NAME LIKE '%table_size';


## Creating Memory Tables
Create a small memory table...

        USE employees;
        CREATE TABLE _departments
            ENGINE=memory
            SELECT * FROM departments;  -- one statement ;)
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
Features of MyISAM are webapp driven:

  - full-text support
  - geospatioal indexes

Caveats:

  - non transactional
  - no FK
  - table-level locking
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
Transactions and consistency.
Foreign Keys.
System and tmp Tablespace.

  - `ibdataXXX` - unshrinkable!
  - undo: `undo00X` new in 5.7, set at --initialize time, automatically managed since 8.0
  - tmp:  `ibtmp1` new in 5.7, created at server startup, for non-compressed tmp tables

InnoDB Log Files.

  - redo: `ib_logfile{0,2}`

Checkpoint interval.

## InnoDB
Innodb TMP tablespace:

  - created at server startup
  - only for non-compressed tables

Avoids:

  - open()+unlink() on disk for every tmp tables
  - storing and uptading tmp tables metadata in ibdata*

        SELECT * FROM INFORMATION_SCHEMA.FILES
          WHERE TABLESPACE_NAME='innodb_temporary' \G

## InnoDB
Buffer Pool:

  - contention & instances (5.7 works better)

        SHOW VARIABLES LIKE 'innodb%';


## InnoDB

  - MVCC
  - row-locking
  - table-locking only for DDL
  - deadlock detection with timeout
  - unshrinkable system tablespace (reduce `ibdata*` requires `--initialize` or `mysql_install_db`)
  - eventually persistent table stats

## Configuring InnoDB
Configuring `innodb_buffer_pool_size`.

Inspecting usage.

Configuring

 - `innodb_log_file_size` - [consider  `BLOB|TEXT` size on 5.6](https://bugs.mysql.com/bug.php?id=69477).
 - `innodb_flush_logs_at_trx_commit`
 - `innodb_undo_tablespaces` - reduce the system tablespace, deprecated and hardcoded to 2 since MySQL 8.0



## Configuring InnoDB
Tablespaces.

Configuring and Resizing Tablespaces. AutoExtend.

Ensure ```innodb_file_per_table=1```.

Check innodb datafiles while changing tables.

        /var/lib/mysql/employees/
        ├── db.opt
        ├── departments.frm
        ├── departments.ibd
        ...


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

With transportable tablespaces you can copy an .ibd between running servers.

Create a table in the d1 database:

        CREATE TABLE d1.t(c1 INT);
        INSERT INTO d1.t(c1) VALUES (1),(2),(3);

Back it up:

        FLUSH TABLES t FOR EXPORT;
	$ cp -rp /var/lib/mysql/d1/t.{ibd,cfg} /tmp/
        UNLOCK TABLES;


## Transportable tablespaces

Create the table in the target machine

        CREATE TABLE d1.t(c1 INT);
        ALTER TABLE t DISCARD TABLESPACE;

Copy back target files

	$ cp -rp /tmp/t.{idb,cfg} /var/lib/mysql/d1/

        ALTER TABLE t IMPORT TABLESPACE;
