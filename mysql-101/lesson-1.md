# MySQL 101

Goal:

  - Implementing an ACID database
  - Installing and Upgrading on Linux, minimal configuration
  - Basic Administration: start/stop, reset password, privileges


# Test Slide
Sample line

* star
- dash

        tabquote







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

# Course setup

Install the following packages via yum or apt-get

    tree dstat vim hostname


# Installing MySQL
## Debian & derivates

    #dpkg -i mysql*deb

## Fedora & derivates

    yum -y install mysql-repo.rpm
    yum -y install MySQL-*
    yum -y install mysql-utilities




# Installing MySQL - 1

Check installed files
  
        #dpkg -L mysql-*
        #id mysql
        #find /etc/ -name \*mysql\*
          
First access
          
        #cat /root/.mysql_secret
        #mysql -u$USER -p$PASSWORD [ -h$HOST -P$PORT ]
        #mysql -e "$QUERY"
  
# Installing MySQL - 2
On Ubuntu/Debian
        
        # cd /opt/mysql/server-5.6/
        # cp support-files/mysql.server /etc/init.d/mysql
        # cp my.cnf /etc/my.cnf
        # useradd mysql -s /usr/sbin/nologin -d /var/lib/mysql
        # chown -R mysql:mysql /var/lib/mysql
        # cat > /etc/profile.d/mysql.sh <<'EOF'
        export MYSQL_HOME=/opt/mysql/server-5.6/
        export PATH+=:$MYSQL_HOME/bin:$MYSQL_HOME/scripts
        EOF

            
Manage mysql service
  
        #service mysql [start|stop|status]
        
        
        
# Installing MySQL - 3
Prepare a minimal configuration file...

        # /etc/my.cnf
        [mysqld]
        ...mysql defaults...
        user=mysql
        datadir=/var/lib/mysql
        
...and the datadir

        # mysql_install_db
        
# Installing MySQL - 4
Further parameters

        # /etc/my.cnf
        [mysqld]
        ...mysql defaults...
        port=13306
        socket=/data2/mysql.sock
        pid-file=/data2/hostname.pid
        tmpdir=/tmp/data2
        log=/data2/hostname.log
     

# Connecting 
Client programs:

- mysql, mysqladmin, mysqlbackup

- full help

        #mysql ... [--help [--verbose]] 
        
- connect via socket or forcing TCP

        #mysql --socket=/var/lib/mysql/mysql.sock
        #mysql --protocol tcp


# mysql.user table
  - Authentication is based on users
  - A user is a couple $(user, host)$ 
       
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

  - Create a user and show its privileges. By default host is '%'
  
        CREATE USER admin identified by 'admin';
        SHOW GRANTS FOR 'admin';   


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
    
        -- Burn after running!
        SET PASSWORD FOR 'root'@'localhost' = PASSWORD('MyNewPass');

  - stop mysql eg. with kill -TERM (NEVER use SIGKILL)
  - start with 
  
        #mysqld --init-file=init.sql
        

# Installing MySQL
## The datadir

Content of 

    /var/lib/mysql/
    |-- [mysql    mysql      19]  foo/
    |-- [mysql    mysql    4.0K]  mysql/
    |-- [mysql    mysql    4.0K]  performance_schema/
    |-- [mysql    mysql       3]  a02f12e917b1.pid
    |-- [mysql    mysql      56]  auto.cnf
    |-- [mysql    mysql     48M]  ib_logfile0
    |-- [mysql    mysql     48M]  ib_logfile1
    |-- [mysql    mysql     12M]  ibdata1
    `-- [mysql    mysql       0]  mysql.sock

     
  - application logs
  - DDL definitions .frm and indexes
  - InnoDB log files 
  - InnoDB tablespace
  - Binary & Relay Logs


# Installing MySQL
## The datadir

  - Create alternative datadirs
  
        #mysql_install_db --datadir=/data2
        
  - Or recreate the default one (from my.cnf)
  
        #mysql_install_db 


# Managing databases - 1
Create databases/tables with

        CREATE DATABASE IF NOT EXISTS d1;
        CREATE TABLE d1.t1(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
            ip INT NOT NULL 
        );
        SHOW CREATE TABLE d1.t1;


# Managing databases - 2
Add entries using the embedded editor

       \e -- opens vi

Type QUERIES

       INSERT INTO d1.t1(ip) VALUES 
            (inet_aton("10.0.0.1")),
            (inet_aton("10.0.0.2")),
            (inet_aton("10.0.0.3"))
       ;
       
Save in a file and execute, exiting from vi
 and typing ";"
       
       <ESC>:w /tmp/sample.sql
       <ESC>:q
       ;

Show them

        SELECT id, INET_NTOA(ip) FROM d1.t1;

        
# Manage databases - 3
Grant permissions on tables

        GRANT ALL ON *.* TO 'network' IDENTIFIED BY 'secret';

OOOPS: we have NO_AUTOCREATE_USER!

        CREATE USER 'network' IDENTIFIED BY 'secret';
        GRANT ALL ON *.* TO 'network';
        
        
        
# Manage databases - 4         
  - Re-authenticate with *network* 
  - Remove table and database with:

        DROP TABLE d1.t1;
        DROP DATABASE d1;
        
      