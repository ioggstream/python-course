## Effects of logging
Setup a database with the provided configuration.

        [mysqld]
        innodb_log_file_size=1M
        innodb_buffer_pool_size=16M
        

## Effects of logging 
Logging impacts on performance and stability

- general (text, table)
- slow-query (text, table)
- error (text)


## Binary Logging
Binary logs trace every change requested to the database.

[Binary Logging][./files/mysql-binary-logging.png]

  - archived on filesystem

        ls /var/lib/mysql/*-bin.*


  - managed  via mysql and mysqladmin
  - accessed with mysqlbinlog


## Managing Binary Logs
Binary logs are written in the following files:

        mysql> show binary logs; 
        | Log_name          | File_size |
        | fabric-bin.000001 |     69414 |
        | fabric-bin.000002 |   1268759 |
  
You can show their content with 

        mysql> SHOW BINLOG EVENTS;

or purge them
  
        mysql> PURGE BINARY LOGS BEFORE now();
    

## Using Binary Logs
Inspect binary logs with mysqlbinlog

        mysqlbinlog /var/log/mysql/hostname-bin.000001
        ...
        SET @@SESSION.GTID_NEXT= '4dc24b1f-ed7d-11e4-94d2-0242ac110035:500'/*!*/;
        create database test
        ...
        SET @@SESSION.GTID_NEXT= '4dc24b1f-ed7d-11e4-94d2-0242ac110035:501'/*!*/;
        create table test.t(i int)

And replay them on another server for:
 
  - PITR 
  - replay load
  - backup.
  