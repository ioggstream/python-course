# MySQL 101

Goal:

  - Implementing an ACID database
  - Installing and Upgrading on Linux, minimal configuration
  - Basic Administration: start/stop, reset password, privileges
  - 




# Come funziona un database - 1
## Aggiungere dati

  - Aggiungere dati
  - Durability
  - Caching, Buffering
  - Performance impact


# Come funziona un database - 2
## Leggere dati

  - Isolation
  - Consistency
  - Atomicity
  - Transazioni


# MySQL Overview - 1
## HLA

  - v. image SG1§49
  - Connection (TCP, Unix, Threads, Authentication) 
    
        --skip-name-resolve || --host-cache-size to grow internal cache

  - SQL Parser / Optimizer (Caches, Authorization)

    - Query exec / cache / logging

  - Storage Engines (Disk, Memory, Network)


# MySQL Overview - 2
## Storage Engines

  - Enable persistency
  - Transactional: InnoDB, NDB
  - Non Transactional: MyISAM, Memory,


# Installing MySQL
## Debian & derivates

    #dpkg -i mysql*deb

## Fedora & derivates

    yum -y install mysql-repo.rpm
    yum -y install MySQL-*
    yum -y install mysql-utilities

## Configuration 

  - Relocate MySQL with 

        --datadir
    
  - or specifying the following options
    
        --port, --socket
        --log, --pid-file
        --tmpdir


# Installing MySQL - 1

  - checking installed files
  
        #dpkg -L mysql-*
        #id mysql
        #find /etc/ -name \*mysql\*
          
        
  - first access
  
        #cat /root/.mysql_secret
        #mysql -u$USER -p$PASSWORD [ -h$HOST ]
        
  
# Installing MySQL - 2
    
  - the mysql service
  
        #service mysql [start|stop|status]


# mysql.user table
  - Authentication is based on users
  - A user is a couple (user, host)
          
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

  - We can change the password with
  
         /usr/bin/mysqladmin -u root password 'new-password'
         /usr/bin/mysqladmin -u root -h a02f12e917b1 password 'new-password'

# mysql.user table

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
        
  - secure the installation!
  
        #mysql_secure_installation
    
        mysql> select user,host,password from mysql.user;                                                                                                                                                       mysql> select user,host,password from mysql.user;
        +------+-----------+------------+
        | user | host      | password   |
        +------+-----------+------------+
        | root | localhost | *81F5E21E3 |
        | root | 127.0.0.1 | *81F5E21E3 |
        | root | ::1       | *81F5E21E3 |
        +------+-----------+------------+
        3 rows in set (0.00 sec)


# Reset root password

  - resetting root password requires a restart
  - create the following init.sql
    
        -- burn after running!
        SET PASSWORD FOR 'root'@'localhost' = PASSWORD('MyNewPass');

  - stop mysql eg. with kill -TERM (NEVER use SIGKILL)
  - start with 
  
        #qmysqld --init-file=init.sql
        

# Installing MySQL
## Datadir content

    #ls /var/lib/mysql
     
  - application logs
  - DDL definitions .frm and indexes
  - InnoDB log files 
  - InnoDB tablespace
  - Binary & Relay Logs

# Installing MySQL
## Recreating datadir

  - Create alternative datadirs
  - Or recreate an existing one
  
    #mysql_install_db --user=mysql --datadir=/var/
    
    
# Upgrading MySQL

  - Stop
  - Backup
  - Upgrade software
  - Check upgrade
    
        #mysql_upgrade
        #mysqlcheck