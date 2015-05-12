# Basic Database Usage & datatypes
## Creating tables
Create databases/tables with

        CREATE DATABASE IF NOT EXISTS d1;
        SHOW DATABASES;
         
Check what happens in /var/lib/mysql, then

        CREATE TABLE d1.t1(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
            ip INT UNSIGNED NOT NULL,
            name CHAR(32) CHARACTER SET utf8 DEFAULT 'Jon'
        );

Which data types are we using? Why?

## Creating tables
Verify that MySQL created exactly what we asked.

        DESCRIBE d1.t1;
        SHOW CREATE TABLE d1.t1 \G



## Creating tables
Check the content of the table

        SELECT * from d1.t1;
        
We can set the currently used database with

        USE d1;
        SELECT * from t1 \G        

Notice the difference between `;` and `\G`.


## Adding entries
Add some entries and check the results.

        INSERT INTO t1(id, ip, name) VALUES (1, 1, 'Sam');
        INSERT INTO t1(id, ip) VALUES (2, 2);
        INSERT INTO t1(ip) VALUES (3);
       
Now test the followings:       
       
        INSERT INTO t1(id) VALUES (4);
        INSERT INTO t1(id) VALUES (1);


## Adding entries
Speed up your work adding entries using the embedded editor

       \e -- opens vi

Type QUERIES

       INSERT INTO d1.t1(ip) VALUES 
            (inet_aton("10.0.0.1")),
            (inet_aton("10.0.0.2")),
            (inet_aton("10.0.0.3"))
       ;
       
Save in a file and execute, exiting from vi
 and typing `;`
       
       <ESC>:w /tmp/sample.sql
       <ESC>:q
       ;

## Adding entries
Show the new entries

        SELECT id, INET_NTOA(ip) FROM d1.t1;


Reload a previous file and add further entries

        <ESC>!!cat /tmp/sample.sql
        

# Authorization reloaded
## Granting permissions
Grant permissions on tables

        GRANT ALL ON *.* TO 'network' IDENTIFIED BY 'secret';

OOOPS: we have NO_AUTOCREATE_USER!

        CREATE USER 'network' IDENTIFIED BY 'secret';
        GRANT ALL ON *.* TO 'network';
        
        
        
## Granting permissions         
  - Re-authenticate with 
  
        mysql -unetwork
  
  - Remove table and database with:

        DROP TABLE d1.t1;
        DROP DATABASE d1;
        
      
# Copy tables
## Copy tables

        CREATE TABLE t2 LIKE t1;
        SELECT * FROM t1 INTO t2;
        
## Loading files
        
        SOURCE /tmp/world_innodb.sql
        mysql < /tmp/world_innodb.sql
        
# information_schema
## Table informations
MySQL stores schema infos in the mysql databases.

The `SHOW` command is used to get those information.
 
        SHOW TABLE STATUS [FROM db_name] [like_or_where]
        SHOW [FULL] TABLES [FROM db_name] [like_or_where]
        SHOW [FULL] COLUMNS FROM tbl_name [FROM db_name] [like_or_where]

The [information_schema][http://dev.mysql.com/doc/refman/5.6/en/information-schema.html] is a read-only set of VIEWS
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

        
## Using information_schema
Listing databases with SQL.

        SELECT * FROM information_schema.schemata;

Tables        

        SELECT table_name, table_type, engine
            FROM information_schema.tables
            WHERE table_schema = 'd1'
            ORDER BY table_name;
        
And Columns

        SELECT table_name, column_name, column_default, 
                ordinal_position, column_key, privileges 
        FROM columns 
        WHERE  table_schema='d1';


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
             Sub_part: NULL
               Packed: NULL
                 Null: 
           Index_type: BTREE
              Comment: 
        Index_comment: 
        1 row in set (0.00 sec)

