# Server Configuration
## Lesson 2 - Goals

- Configure basic security and logging parameters
- Using profiles
- Get/Set variables
- Set SQL Modes 
- Populate databases
- Application Logging

    
    
## Server Configuration
Show all mysqld **System Variables** (aka parameters)
    
        mysqld --verbose --help
    
    
Read from /etc/my.cnf or via

        mysqld --defaults-file=/etc/my-file.cnf
    
Show running status via

        #mysqladmin variables

Don't explicit default values in the configuration!


## Server Configuration
Always start from an empty file

        cp /usr/my.cnf /etc/

my.cnf is made up of stanzas

        # /etc/my.cnf
        [server]
        # for mysqld, ..
        datadir=/disk2/data
        user=mysql

        [mysqld]
        # only for mysqld
        user=mysql
        datadir=/disk2/data

**mysqld exits in case of**:

  - syntax errors
  - unexistent system variables
    
## Configuration
Show the parameters *to be used*

        my_print_defaults mysqld
        
Show the *actual* values

        mysqladmin variables
        
Show the *actual* values from `mysql`
      
        SHOW [GLOBAL|SESSION] VARIABLES [LIKE ...];
        SHOW VARIABLES LIKE 'innodb_%';
        
## Configuration vs Status

`mysqld` provides `STATUS` insights

        SHOW [GLOBAL|SESSION] STATUS [LIKE ...];

`STATUS` != `VARIABLES`

  - `STATUS`: internal status
  - `VARIABLES`: configuration

  |variable_name|table|note|
  |--|--|--|
  |max_used_connections|GLOBAL_STATUS|effectively used|
  |max_connections|GLOBAL_VARIABLES|server-wide limit| 
  |max_user_connections|GLOBAL_VARIABLES|per-user limit|
  |max_user_connections|SESSION_VARIABLES|current user limit|


**Don't confuse `max_user_connections` and `max_used_connections`**


## Global & Session configuration

Global variables:

  - server wide;
  - apply to every connection;
  - static or dynamic;
  - changed by `SUPER` users
  
        SET @@GLOBAL.max_tmp_table_size=4*(1<<20);  -- eg.
  
Session variables:

  - apply to the current session (connection) only;
  - dynamic.
  
        SET @@SESSION.sql_mode='TRADITIONAL'; -- eg.

Changes to global dynamic variables (eg. max_tmp_table_size) apply to future sessions.

## Configuring consistency
Privilege consistency and security

        [mysqld]
        # sql-mode=STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION <-- in MySQL 5.7 this settings is already configured
        innodb-flush-log-at-trx-commit=1
        innodb-fast-shutdown=0
        myisam-recover-options=FORCE,BACKUP
        explicit_defaults_for_timestamp

timestamp_defaults on 5.6+ are more flexible but you must use the [DEFAULT CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP clauses in column definitions](http://dev.mysql.com/doc/refman/5.6/en/timestamp-initialization.html)
        
## Configuring security
Further security tips for server...

        [mysqld]
        ...
        local-infile=0
        skip-symbolic-links
   
...and client.
   
        [mysql]
        # inhibit unlimited UPDATE, DELETE, SELECT
        # override with --safe-updates=0
        safe-updates
        show-warnings

## Limit resource usage

Limit max connections

        [mysqld]
        ...
        max_connections=100
        
Check used connections

        SHOW STATUS LIKE 'max_used_connections'
        
## Application logging
mysqld does **not** create logs by default.
        
        # configure general and slow query logs
        #  eventually using defaults
        general-log-file[=hostname.log]
        slow-query-log-file[=hostname-slow.log]
        slow-query-log=1
        log-queries-not-using-indexes=on

Log general and slow query on tables using

        log-output=TABLE -- SET GLOBAL log-output='TABLE';

Get (or trash) data with

        SHOW TABLES FROM mysql LIKE '%log%';
        SELECT * FROM [general_log|slow_log];
        TRUNCATE mysql.general_log;
        

## Application logging
If error-log is specified, stdout|err is redirected.

        # set the log file will daemonize
        #  the server
        log-error[=hostname.err]
        
You can use mysqld_safe to eventually restart the server
in case of problems.

Error log should not rely on mysqld: it cannot be saved on tables!


## Application logging
Don't fill your disks with logs!

  - consider separate partitions;
  - rotate logs, checking the actual policy;
  
        cat /etc/logrotate.d/mysql

  - or copy and modify

        fedora#cp /usr/share/mysql/mysql-log-rotate  /etc/logrotate.d/mysql
        ubuntu#cp /opt/mysql/server-5.6/support-files/mysql-log-rotate /etc/logrotate.d/mysql

Inspect /etc/logrotate.d/mysql

## Sql modes

Historically mysql was relaxed on data input:

  - send warnings instead of errors;
  - truncates malformed data without raising issues;
  - accepted malformed dates

Default now is more restrictive:

        SET @@SESSION.SQL_MODE=DEFAULT; -- no quotes!
        SELECT @@SESSION.SQL_MODE;

`SQL_MODE` can be:

        SET @@SESSION.SQL_MODE='';  -- very relaxed or
        SET @@SESSION.SQL_MODE='TRADITIONAL';  -- return errors instead of warnings


## `SQL_MODE`

With

        SET @@SESSION.SQL_MODE='';  -- very relaxed
        CREATE TABLE d1.d1 (d datetime);

We get
        INSERT INTO d1.d1(d) VALUES
            ('00-00-0000'),
            ('13-13-2016');
        SHOW WARNINGS;  -- instead of errors

Malformed data is truncated

        SELECT COUNT(*) FROM d1.d1
            WHERE d='00-00-0000'; -- 2 rows!

## `SQL_MODE`

Exercise: try the previous `INSERT`s separately after

        SET @@SESSION.SQL_MODE='STRICT_TRANS_TABLES';
        TRUNCATE TABLE d1.d1;

What do you get from:

        --  Incorrect datetime value: '13-13-2016'
        SELECT * from d1.d1;


**Replication overrides `@@SESSION.sql_mode`. `@@GLOBAL.sql_mode` doesn't apply during replication**
