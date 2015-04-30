# Effects of logging
Setup a database with the provided configuration.

        [mysqld]
        innodb_log_file_size=1M
        innodb_buffer_pool_size=16M
        

# Effects of logging 
Logging impacts on performance and stability

- general (text, table)
- slow-query (text, table)
- error (text)


# Binary Logging
Binary logs trace every change requested to the database.

[Binary Logging][./files/mysql-binary-logging.png]

  - archived on filesystem

        ls /var/lib/mysql/*-bin.*


  - managed  via mysql and mysqladmin
  - accessed with mysqlbinlog


# Managing Binary Logs
Binary logs are written in the following files:

        mysql> show binary logs; 
        | Log_name          | File_size |
        | fabric-bin.000001 |     69414 |
        | fabric-bin.000002 |   1268759 |
  
You can show their content with 

        mysql> SHOW BINLOG EVENTS;

  
        mysql> PURGE BINARY LOGS BEFORE now();
    

# 
  

  