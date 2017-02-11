# Basic Database Usage & datatypes

## Data Types

Data is stored using 4 [macro-types](http://dev.mysql.com/doc/mysql/en/data-types.html):

  - temporal    TIMESTAMP, DATE, DATETIME, YEAR
  - numeric     BIT, *INT*, FLOAT, DOUBLE, DECIMAL
  - byte        BLOB, *BINARY
  - character   *CHAR, TEXT, ENUM, SET
  
MySQL 5.7 changes temporal data logic. Check the documentation!

## Data Types

Use the same data-types for `JOIN` columns!

Joining on different data-types causes an IMPLICIT CONVERSION of data.


## Data Types

Some data-types have similarities:
  
   - `BINARY` and `CHAR`
   - `TEXT` and `BLOB`

                       max size in bit 
                   TINY      -   MEDIUM  LONG
        BLOB,TEXT  8        16     24     32

TEXT|BLOB fields:

  - can't be used as partitioning fields
  - can't be used with `ENGINE=MEMORY`
  - impact on temporary tables performance

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

Exercise: explain the differences between the `DESCRIBE` and the `SHOW CREATE`.


## Creating tables
Check the content of the table

        SELECT * FROM d1.t1;
        
We can set the currently used database with 
nstutute
        USE d1;
        SELECT * 
         t1 \G        

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
    
        
        \e  -- open vi
        <ESC>!!cat /tmp/sample.sql


# Authorization reloaded
## Granting permissions
Grant permissions on tables

        GRANT ALL ON d1.* TO 'network';
        SHOW ERRORS;
        +-------+------+-----------------------------------------------+
        | Level | Code | Message                                       |
        +-------+------+-----------------------------------------------+
        | Error | 1133 | Can't find any matching row in the user table |
        +-------+------+-----------------------------------------------+

OOOPS, we have `NO_AUTO_CREATE_USER`: specify a password please!

        GRANT ALL ON d1.* TO 'network' IDENTIFIED BY 'secret';
        
        CREATE USER 'network' IDENTIFIED BY 'secret';
        GRANT ALL ON d1.* TO 'network';
        

## Creating administrative users
To grant administrative privileges use

        GRANT ALL ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;

Now create a small VIEW to query user privileges without typing all the fields

        CREATE VIEW mysql.user_view AS 
            SELECT USER,HOST,AUTHENTICATION_STRING
                FROM mysql.user;


## Granting with limits

You can limit user resources using

        GRANT ... WITH    
              MAX_QUERIES_PER_HOUR count   
              MAX_UPDATES_PER_HOUR count
              MAX_CONNECTIONS_PER_HOUR count
              MAX_USER_CONNECTIONS count

Zero means **unlimited** 

Try now

        GRANT ALL on d2.* to 'network' WITH
              MAX_USER_CONNECTIONS 1;
  
        
## Granting permissions         
  - Re-authenticate with 
  
        mysql -unetwork

  - Authenticate again in another session

        mysql -unetwork  # again
        ERROR 1226 (42000): User 'network' has exceeded the 'max_user_connections' resource (current value: 1)

  
  - Remove table and database with:

        DROP TABLE d1.t1;
        \! tree /var/lib/mysql
        
        DROP DATABASE d1;
        \! tree /var/lib/mysql

        CREATE DATABASE d1; -- again

## Revoking permissions
Explain privileges.

 - Revoking privileges. What happened? 

        SHOW GRANTS FOR 'network';
        REVOKE DROP ON d1.* FROM 'network';
  
GRANT supports 

  - resource quotas. 
  - punctual privileges (eg. ```GRANT SELECT (id) ON d1.t1 TO ...```)
    
        HELP [GRANT|REVOKE]; 

 
## Removing users

 - Revoke all privileges without removing the user;
 
        REVOKE ALL ON *.* FROM 'network';
        SELECT * FROM mysql.user_view; -- the view defined above.
 
 - Remove the user;
 
        DROP USER 'network';
   
Remember: **users are couples** !

        CREATE USER 'a';
        CREATE USER 'a'@'localhost';
        DROP USER 'a';
        
Which is the expected output of: 
        
        SELECT * FROM mysql.user_view;
