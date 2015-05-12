# Basic Authentication and Authorization


## mysql.user table
  - Authentication is based on users
  - A user is a **couple** $(user, host)$ 
       
        mysql> select user,host,password from mysql.user;
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


## mysql.user table
  - Create a user and show its privileges. By default host is '%'
  
        CREATE USER admin identified by 'admin';
        SHOW GRANTS FOR 'admin' \G   

  - We can change the password with
  
         /usr/bin/mysqladmin -u root password 'new-password'
         /usr/bin/mysqladmin -u root -h a02f12e917b1 password 'new-password'


## Securing installation

  - Once you change the password you get
  
        mysql> select user,host,password from mysql.user;
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
  
        #mysql_secure_installation
  
  - and check the outcome
  
        mysql> select user,host,password from mysql.user;                                                                                                                                                       mysql> select user,host,password from mysql.user;
        +------+-----------+------------+
        | user | host      | password   |
        +------+-----------+------------+
        | root | localhost | *81F5E21E3 |
        | root | 127.0.0.1 | *81F5E21E3 |
        | root | ::1       | *81F5E21E3 |
        +------+-----------+------------+
        3 rows in set (0.00 sec)


## Reset root password

  - resetting root password requires a restart
  - create the following init.sql
    
        -- Burn after running!
        SET PASSWORD FOR 'root'@'localhost' = PASSWORD('MyNewPass');

  - stop mysql eg. with kill -TERM (NEVER use SIGKILL)
  - start with 
  
        #mysqld --init-file=init.sql
        

