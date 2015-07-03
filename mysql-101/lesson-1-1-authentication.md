# Basic Authentication and Authorization


## mysql.user table & co
  - Authentication is based on users
  - A user is a **couple** $(user, host)$ 
       
        mysql> SELECT user,host,password FROM mysql.user;
        +------+--------------+----------+
        | user | host         | password |
        +------+--------------+----------+
        | root | localhost    |          |
        | root | a02f12e917b1 |          |
        | root | 127.0.0.1    |          |
        | root | ::1          |          |
        |      | localhost    |          |
        |      | a02f12e917b1 |          |
        +------+--------------+----------+
        6 rows in set (0.00 sec)


  - Skip calling DNS during authentication with ```--skip-name-resolve```


## mysql.user table & co
If you have performance_schema enabled

        SHOW VARIABLES LIKE 'performance_schema';
        USE performance_schema;

you can:

        SELECT * FROM accounts;
        SELECT * FROM users;
        SELECT * FROM hosts;


## mysql.user table & co
  - Create a user and show its privileges. By default host is '%'
  
        CREATE USER admin IDENTIFIED BY 'admin';
        SHOW GRANTS FOR 'admin' \G     
        HELP CREATE USER -- read carefully!
 
  - Show `root` privileges, and remember **users are couples**
  
        SHOW GRANTS; -- explain grants
        SHOW GRANTS FOR 'root'; -- does it work? Why?
        SHOW GRANTS FOR 'root'@'localhost'; 
        
  - We can change the password with
  
         /usr/bin/mysqladmin -u root password 'new-password'
         /usr/bin/mysqladmin -u root -h a02f12e917b1 password 'new-password'

  
## Securing installation

  - Once you change the password you get
  
        mysql> SELECT user,host,password FROM mysql.user;
        +------+--------------+---------------+
        | user | host         | password      |
        +------+--------------+---------------+
        | root | localhost    | *81F5E21E3... |
        | root | a02f12e917b1 | *81F5E21E3... |
        | root | 127.0.0.1    |               |
        | root | ::1          |               |
        |      | localhost    |               |
        |      | a02f12e917b1 |               |
        +------+--------------+---------------+
        6 rows in set (0.00 sec)

  - It's not secured (anonymous user)!
  
        mysql -u"" -e "SELECT 1;"
  

## Securing installation
  - secure the installation!
  
        mysql_secure_installation
  
  - and check the outcome
  
        mysql> SELECT user,host,password FROM mysql.user;                                                                                                                                                       mysql> SELECT user,host,password from mysql.user;
        +------+-----------+------------+
        | user | host      | password   |
        +------+-----------+------------+
        | root | localhost | *81F5E21E3 |
        | root | 127.0.0.1 | *81F5E21E3 |
        | root | ::1       | *81F5E21E3 |
        +------+-----------+------------+
        3 rows in set (0.00 sec)




## Change root password


## Reset root password

  - resetting root password requires a restart
  - create the following init.sql
    
        -- Burn after running!
        -- And don't replicate this instruction.
        SET PASSWORD FOR 'root'@'localhost' = PASSWORD('MyNewPass');

  - stop mysql eg. with kill -TERM (NEVER use SIGKILL)
  - start with 
  
        mysqld --init-file=init.sql
        

## Reset root password

MySQL loads authentication tables in memory and enables them after startup.

 
Skipping this step allows unauthenticated connections
 
        mysqld --skip-grant-tables \    # don't load authentication
            --skip-networking \         # don't use TCP
            --socket=mysql-$RANDOM.sock # use a non-standard socket!
        
Once you log-in you need to load privilege table to be able to change it.

        STATUS;
        FLUSH PRIVILEGES; -- (re)load grant tables
        SET PASSWORD FOR 'root'@'localhost' = PASSWORD('new_password');
        
Now `mysqladmin shutdown` and restart normally.
   
   
   