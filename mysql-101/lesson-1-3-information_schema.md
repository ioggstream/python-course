# information_schema

## Internal databases

  | db | action | scope | 
  |--|--|--|
  | `mysql` | rw |configuration, logs, replication, user privileges| 
  | `information_schema`| ro | DDL, Privileges, Server status & conf|
  | `performance_schema`| rw | general runtime data |
  | `sys`| rw | wrapper on performance_schema|
  
## Table informations
MySQL stores schema infos in many mysql databases.

The `SHOW` command is used to get those information.
 
        SHOW TABLE STATUS [FROM db_name] [like_or_where]
        SHOW [FULL] TABLES [FROM db_name] [like_or_where]
        SHOW [FULL] COLUMNS FROM tbl_name [FROM db_name] [like_or_where]

`SHOW` provides server status too

        SHOW [FULL] PROCESSLIST
        SHOW OPEN TABLES

The [information_schema](http://dev.mysql.com/doc/refman/5.6/en/information-schema.html) is a read-only set of VIEWS
 provinding SQL access to metadata.


## Table informations
Listing columns from a table:

        DESCRIBE t1;
        SHOW COLUMNS FROM t1;
        +-------+------------------+------+-----+---------+----------------+
        | Field | Type             | Null | Key | Default | Extra          |
        +-------+------------------+------+-----+---------+----------------+
        | id    | int(11)          | NO   | PRI | NULL    | auto_increment |
        | ip    | int(10) unsigned | NO   |     | NULL    |                |
        | name  | char(32)         | YES  |     | Jon     |                |
        +-------+------------------+------+-----+---------+----------------+
        3 rows in set (0.01 sec)


## Describe columns
More informations

        mysql> SHOW FULL COLUMNS FROM d1.t1;
        +-------+------------------+-----------------+------+-----+---------+----------------+---------------------------------+---------+
        | Field | Type             | Collation       | Null | Key | Default | Extra          | Privileges                      | Comment |
        +-------+------------------+-----------------+------+-----+---------+----------------+---------------------------------+---------+
        | id    | int(11)          | NULL            | NO   | PRI | NULL    | auto_increment | select,insert,update,references |         |
        | ip    | int(10) unsigned | NULL            | NO   |     | NULL    |                | select,insert,update,references |         |
        | name  | char(32)         | utf8_general_ci | YES  |     | Jon     |                | select,insert,update,references |         |
        +-------+------------------+-----------------+------+-----+---------+----------------+---------------------------------+---------+
        3 rows in set (0.00 sec)

        
## USE information_schema;
Listing databases with SQL.

        SELECT * FROM information_schema.schemata;

Tables        

        SELECT table_name, table_type, engine
            FROM information_schema.tables
            WHERE table_schema = 'd1'
            ORDER BY table_name;


## USE information_schema;
More on tables

        SELECT table_name, 
            -- format numbers with 0 decimals
            FORMAT(table_rows,0),
            -- bitwise shift (10 for KB, 20 for MB, 30 for GB) 
            data_length >> 20   
        FROM tables 
        WHERE table_schema = 'employees';

And Columns

        SELECT table_name, column_name, column_default, 
                ordinal_position, column_key, privileges 
        FROM columns 
        WHERE  table_schema='d1';

## USE information_schema;

Or Views (treated like tables)

        SELECT table_name, definer
        FROM views
        WHERE table_schema not in ('mysql', 'sys');
        
Or routines

        SELECT routine_name, definer
        FROM routines
        WHERE routine_schema not in ('mysql', 'sys');


## Indexes
Indexes can be inspected with:

        SHOW INDEX FROM t1 \G
        *************************** 1. row ***************************
        Table: t1
           Non_unique: 0
             Key_name: PRIMARY
         Seq_in_index: 1
          Column_name: id
            Collation: A
          Cardinality: 3
                 ...
        1 row in set (0.00 sec)

