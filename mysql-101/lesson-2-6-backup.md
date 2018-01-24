# Backup
## Goal

  - Backup 101
  - What to backup
  - Use mysqldump and mysqlbackup
  
## Backup 
Importance of backups. Differences between:

  - Backup 
  - High Availability 
  - Disaster Recovery

Measure and Test backup: 

  - Mean Time Between Failures;
  - Meat Time To Recovery;
  - Recovery Point Objective;
  
  
## Backup
Database backups:
 
 - hot vs cold 
 - logical vs physical
 - full vs incremental
 - transactions
 - importance of binary logs
 
Impacts of backup.



## mysqldump
Show parameters from

        mysqldump --verbose --help |& less

Create a logical backup:

        mysqldump --master-data=1 --all-databases |
            gzip > /backup/backup-$(date -I).sql.gz
            
## mysqldump
Exercise: 

  - drop *one* table from your DB;
  - create a new mysqld instance with  `--datadir=/backup/`;
  - restore your backup there;
  - restore the dropped table on the main DB;


## mysqldump solution
Create a versioned datadir:
        
        BACKUPDIR=/backup/$(date -I)
        mkdir -p $BACKUPDIR
        chown -R mysql:mysql /backup
        
Create a new instance without network:
         
        mysqld --socket=/backup/mysql.sock  \
            --skip-networking               \ 
            --skip-grant-tables             \
            --datadir=/backup/$(date -I) &

Restore your db

        gunzip -c /backup/backup-$(date -I).sql.gz | 
            mysql --socket=/backup/mysql.sock 
        

## mysqldump solution

Dump the dropped table from your restore and
pass it to the master instance.

        mysqldump --socket=/backup/mysql.sock   \
            --master-data=2                     \
            --tables $DATABASE $TABLE | mysql $DATABASE


## mysqlbackup
With mysqlbackup you can make physical backups:

  - copy datafiles
  - apply innodb logs
  - save binary logs
  
Configure in /etc/my.cnf

        [mysqlbackup]
        user=mysqlbackup
        backup_dir=/backup/full
        incremental_backup_dir=/backup/incremental
        with_timestamp
        socket=/var/lib/mysql/mysql.sock

## mysqlbackup
The `mysqlbackup` user requires at least the 
[following privileges](http://dev.mysql.com/doc/mysql-enterprise-backup/3.9/en/mysqlbackup.privileges.html)

        GRANT RELOAD ON *.* TO 'mysqlbackup'@'localhost';
        GRANT CREATE, INSERT, DROP, UPDATE 
            ON mysql.backup_progress TO 'mysqlbackup'@'localhost';
        GRANT CREATE, INSERT, SELECT, DROP, UPDATE 
            ON mysql.backup_history TO 'mysqlbackup'@'localhost';
        GRANT REPLICATION CLIENT ON *.* TO 'mysqlbackup'@'localhost';
        GRANT SUPER ON *.* TO 'mysqlbackup'@'localhost';
        FLUSH PRIVILEGES; 

Create a user with the given privileges copying data from mysql documentation[^mysqlbackup]

[^mysqlbackup]: http://dev.mysql.com/doc/mysql-enterprise-backup/3.9/en/mysqlbackup.privileges.html 

## mysqlbackup

Linux tip ;) 

  - install Mysql Enterprise Backup via rpm
  - list files in the `meb` package with:

        rpm --query --list meb

## mysqlbackup
To create a consistent backup:
 
  - create a ```--login-path=mysqlbackup``` 
  - run the following command
  
        mysqlbackup --login-path=mysqlbackup backup
        
  - you can apply ib_logs too with     
    
        mysqlbackup --login-path=mysqlbackup backup-and-apply-log


## mysqlbackup
Incremental backups require a starting point.

  - a history entry

        mysqlbackup --login-path=mysqlbackup        \
            --incremental                           \
            --incremental-base=history:last_backup  \
            backup
            
  - or a directory
  
        FULLDIR=/backup/full/2015-05-18_16-14-18/
        mysqlbackup --login-path=mysqlbackup    \
            --incremental                       \  
            --incremental-base=dir:$FULLDIR     \
            backup            


## mysqlbackup
Inspect the backup directories.

Data and metadata in backup dirs.

Applying ib_logs and incremental backup.

Incremental backups require a starting point

        mysqlbackup --backup-dir=$FULLDIR \
            apply-log   # only if not applied
        mysqlbackup --backup-dir=$FULLDIR \
            --incremental-backup-dir=$INCRDIR \
            apply-incremental-backup


## mysqlbackup
The command to restore a database is

        mysqlbackup [--datadir=...] \
            --backup-dir=$FULLDIR \
            copy-back

Exercises: 

 - which are the steps to validate a database backup?
 - validate the backup restoring the db in another place.
 
 
## Point in Time Recovery

Use `binlog` to execute a PITR.

  - restore a backup and get the last restored transaction;
  - identify the transactions you want to recover in binlogs;

Use mysqlbinlog:

        mysqlbinlog host-bin.000* \                             # get the right files
                --exclude-gtids="$UUID:1-975;$UUID:1034" \      # identify applied transactions
                --skip-gtids \                                  # eventually skip old gtids if you aren't doing a full restore
                | mysql                                         # apply all to mysql

** Always process all binlogs with the same command to avoid consistency issues **
