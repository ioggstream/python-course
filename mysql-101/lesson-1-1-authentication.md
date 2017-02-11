# Basic Authentication and Authorization


## mysql.user table & co
  - Authentication is based on users
  - A user is a **couple** $(user, host)$ 
       
        mysql> SELECT user,host,authentication_string FROM mysql.user;
        +------+--------------+-----------------------+
        | user | host         | authentication_string |
        +------+--------------+-----------------------+
        | root | localhost    |                       |
        | root | a02f12e917b1 |                       |
        | root | 127.0.0.1    |                       |
        | root | ::1          |                       |
        |      | localhost    |                       |
        |      | a02f12e917b1 |                       |
        +------+--------------+-----------------------+
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
  
         mysqladmin -u root password 'new-password'               # may use port 3306
         mysqladmin -u root password -h localhost 'new-password'  # uses socket
         mysqladmin -u root -h a02f12e917b1 password 'new-password'

  
## Securing installation 

  - Once you change the password *check* if you get extra rows.
  
        mysql> SELECT user,host,authentication_string FROM mysql.user;
        +------+--------------+-----------------------+
        | user | host         | authentication_string |
        +------+--------------+-----------------------+
        | root | localhost    | *81F5E21E3...         |
        | root | a02f12e917b1 | *81F5E21E3...         |
        | root | 127.0.0.1    |                       |
        | root | ::1          |                       |
        |      | localhost    |                       |
        |      | a02f12e917b1 |                       |
        +------+--------------+-----------------------+
        6 rows in set (0.00 sec)

  - In that case, it's not secured (anonymous user)!
  
        mysql -u"" -e "SELECT 1;"
  

## Securing installation - 5.6 only

  - secure the installation!
  
        mysql_secure_installation
  
  - and check the outcome
  
        mysql> SELECT user,host,authentication_string FROM mysql.user;
        +------+-----------+-------------------------+
        | user | host      | authentication_string   |
        +------+-----------+-------------------------+
        | root | localhost | *81F5E21E3              |
        | root | 127.0.0.1 | *81F5E21E3              |
        | root | ::1       | *81F5E21E3              |
        +------+-----------+-------------------------+
        3 rows in set (0.00 sec)


## Securing installation - 5.7 

MySQL 5.7 is secure by default:

  - `--initialize` dumps a random password to error-log 
  - you must change this password at first login
  - the password policy plugin is enabled

On Ubuntu|Debian:

  - root user uses the `auth_socket` plugin
  - no access from network, just socket
  - no password required


## Reset root password

Resettin root password requires a restart.

MySQL loads authentication tables in memory and enables them after startup:

Skipping this step allows unauthenticated connections
 
        mysqld --skip-grant-tables \    # don't load authentication
            --skip-networking \         # don't use TCP
            --socket=mysql-$RANDOM.sock # use a non-standard socket!
        
Once you log-in you need to load privilege table to be able to change it.

        STATUS;
        FLUSH PRIVILEGES; -- (re)load grant tables
        ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
        
Now `mysqladmin shutdown` and restart normally.
   
## Reset root password   

  - You can put those instructions in `resetpassword.sql`
and append `--init-file=resetpassword.sql` to `mysqld`.

  - To stop mysql **never** use `SIGKILL`. 
        
        

## Authentication plugins

Customized authentication methods:

  - auth_socket: trust system username and permission to access `mysql.sock`
  - auth_pam: delegate to `PAM` (requires cleartext password communication)
  
Eg. `auth_socket`

        INSTALL PLUGIN 'auth_socket' SONAME 'auth_socket.so';
        CREATE USER 'mysql'@'localhost' IDENTIFIED WITH 'auth_socket';  -- passwords are ignored!
        
Now login with 
 
        sudo -u mysql mysql -umysql  # tada!

This `mysql` user has no special privilege!

        SHOW GRANTS FOR CURRENT_USER();
        FLUSH LOGS;  -- won't work!


        
