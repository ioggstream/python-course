# Backup & Replication
## Goal

  - Backup 101
  - What to backup
  - 
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
The `mysqlbackup` user requires at least the [following privileges](http://dev.mysql.com/doc/mysql-enterprise-backup/3.9/en/mysqlbackup.privileges.html)[^http://dev.mysql.com/doc/mysql-enterprise-backup/3.9/en/mysqlbackup.privileges.html ]

        GRANT RELOAD ON *.* TO 'mysqlbackup'@'localhost';
        GRANT CREATE, INSERT, DROP, UPDATE 
            ON mysql.backup_progress TO 'mysqlbackup'@'localhost';
        GRANT CREATE, INSERT, SELECT, DROP, UPDATE 
            ON mysql.backup_history TO 'mysqlbackup'@'localhost';
        GRANT REPLICATION CLIENT 
            ON *.* TO 'mysqlbackup'@'localhost';
        GRANT SUPER 
            ON *.* TO 'mysqlbackup'@'localhost';
        FLUSH PRIVILEGES; 

Create a user with the given privileges copying 
