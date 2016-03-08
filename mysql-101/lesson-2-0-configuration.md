# Server Configuration
## Lesson 2 - Goals

- Configure basic security and logging parameters
- Using profiles
- Get/Set variables
- Set SQL Modes 
- Populate databases
- Application Logging

    
    
## Server Configuration
Show all mysqld parameters
    
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

    
## Configuration
Show the parameters *to be used*

        my_print_defaults mysqld
        
Show the actual values

        mysqladmin variables
        
Show the actual values from mysql
      
        SHOW [GLOBAL|SESSION] VARIABLES [LIKE ...];
        SHOW VARIABLES LIKE 'innodb_%';
        

## Configuring consistency
Privilege consistency and security

        [mysqld]
        # sql-mode=STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION <-- in MySQL 5.7 this settings is already configured
        innodb-flush-log-at-trx-commit=1
        innodb-fast-shutdown=0
        myisam-recover-options=FORCE,BACKUP
        explicit_defaults_for_timestamp

        
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


        
## Application logging
mysqld does **not** create logs by default.
        
        # configure general and slow query logs
        #  eventually using defaults
        general-log-file[=hostname.log]
        slow-query-log[=hostname-slow.log]

Log general and slow query on tables using

        log-output=TABLE -- SET GLOBAL log-output='TABLE';

Get data with

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

