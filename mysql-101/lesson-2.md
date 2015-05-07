# Lesson 2 - Goals

- Configure basic security and logging parameters
- Using profiles
- Get/Set variables
- Set SQL Modes 
- Populate databases
- Logging

    
    
# Configuration
Show all mysqld parameters
    
        mysqld --verbose --help
    
    
Read from /etc/my.cnf or via

        mysqld --defaults-file=/etc/my-file.cnf
    
Show running status via

        #mysqladmin variables

Don't explicit default values in the configuration!
     
# Configuration
Always start from an empty file

        bash#cp /usr/my.cnf /etc/

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


For now just avoid typing credentials

        [client]
        # insecurely store clear text credentials
        # for mysql, mysqladmin, mysqldump
        user=root
        password=root
        compress
        
    
# Configuration
Show the parameters *to be used*

        bash#my_print_defaults mysqld
        
Show the actual values

        bash#mysqladmin variables
        
Show the actual values from mysql
      
        sql#SHOW [GLOBAL|SESSION] VARIABLES [LIKE ...];
        sql#SHOW VARIABLES LIKE 'innodb_%';
        

# Configuring consistency
Privilege consistency and security

        [mysqld]
        sql-mode=STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
        innodb-flush-log-at-trx-commit=1
        innodb-fast-shutdown=0
        myisam-recover-options=FORCE,BACKUP
        explicit_defaults_for_timestamp

        
# Configuring security
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

# Configuring security
Store credentials [in the encrypted file][http://dev.mysql.com/doc/refman/5.6/en/mysql-config-editor.html] 
~/.mylogin.cnf using

        #mysql_config_editor set 
            --login-path=client # default used by mysql 
            --host=localhost 
            --user=localuser 
            --password # (prompted)

We can define further servers

        #mysql_config_editor set
            --login-path=master
            --host=m-1.foo.it
            --port=13306
            --user=admin
            --password # (prompted)
        
# Application logging
mysqld does **not** create logs by default.
        
        # configure general and slow query logs
        #  eventually using defaults
        general-log[=hostname.log]
        slow-query-log[=hostname-slow.log]

If error-log is specified, stdout|err is redirected.

        # set the log file will daemonize
        #  the server
        log-error[=hostname.err]
        
You can use mysqld_safe to eventually restart the server
in case of problems.

Error log should not rely on mysqld: it cannot be saved on tables!


# Application logging
Don't fill your disks with logs!

  - consider separate partitions;
  - rotate logs, checking the actual policy;
  
        cat /etc/logrotate.d/mysql

  - or copy and modify

        fedora#cp /usr/share/mysql/mysql-log-rotate  /etc/logrotate.d/mysql
        ubuntu#cp /opt/mysql/server-5.6/support-files/mysql-log-rotate /etc/logrotate.d/mysql

      
# Populating a database
While monitoring system status with
 
         dstat -cgmprsy 5
    
we'll import the [Employees database](http://bit.ly/1HMHCBf)

        bash#wget http://bit.ly/1HMHCBf    
        bash#tar xf employee*
        bash#cd employee*
        bash#mysql < $DBFILE
        
Repeat enabling/disabling autocommit.


# Populating a database
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
        

        
# Upgrading MySQL

  - Stop
  - Backup
  - Upgrade software
  - Check upgrade
    
        #mysql_upgrade
        #mysqlcheck

     
     
        
