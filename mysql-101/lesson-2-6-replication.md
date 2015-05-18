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
            
Exercise: create a new instance in the `/backup` datadir 
and restore there the backup.


## mysqldump solution
Create a versioned datadir:
        
        BACKUPDIR=/backup/$(date -I)
        mkdir -p $BACKUPDIR
        chown -R mysql:mysql /backup
        
Create a new instance without network:
         
        mysqld --socket=/backup/mysql.sock \
            --skip-networking \ 
            --skip-grant-tables \
            --datadir=/backup/$(date -I) &

Restore your db

        gunzip /backup/backup-$(date -I).sql.gz | 
            mysql --socket=/backup/mysql.sock 
        

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
[following privileges](http://dev.mysql.com/doc/mysql-enterprise-backup/3.9/en/mysqlbackup.privileges.html)[^mysqlbackup]

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
To create a consistent backup:
 
  - create a ```--login-path=mysqlbackup``` 
  - run the following command
  
        mysqlbackup --login-path=mysqlbackup backup
        
  - you can apply ib_logs too with     
    
        mysqlbackup --login-path=mysqlbackup backup-and-apply-log


## mysqlbackup
Incremental backups require a starting point.

  - a history entry

        mysqlbackup --login-path=mysqlbackup \
            --incremental  
            --incremental-base=history:last_backup
            backup-and-apply-blog
            
  - or a directory
  
        FULLDIR=/backup/full/2015-05-18_16-14-18/
        mysqlbackup --login-path=mysqlbackup \
            --incremental  
            --incremental-base=dir:$FULLDIR
            backup-and-apply-blog            


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
 
 
# Replication, Scalability and Partitioning
## CAP Theorem
 Partitioning: Synchronization reloaded.

You cannot have the same level of:
 
 - Consistency 
 - Atomicity
 - Partition
 
Instead you have to favor something respect to the other.


## CAP Theorem Reloaded

You can pay for having more!

  - faster network
  - faster cpu
  - faster storage
 
Price is the 4th dimension.


## Replication

Advantges of replication. Use cases.

Synchronous, asynchronous and semi-synchronous replication.

Replication in MySQL. Topologies and GTID.

## 