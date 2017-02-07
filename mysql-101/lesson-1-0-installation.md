# Installation and basic usage

## Goal

  - Installing on Linux (debian, fedora)
  - Structure of the data directory
  - Basic Administration: start/stop, reset password, privileges, secure installation
  - Connecting to the database
  - Basic Usage: create/query/drop databases and tables
  - Basic configuration


## Course setup

Install the following packages via yum or apt-get

    tree dstat vim hostname
    
Download all of the MySQL packages via yum or from MySQL website.

Unpack the Employee and Sakila databases

        bash#wget  http://bit.ly/1qEutCs -O employees.tar.gz     
        bash#tar xf employee*


## Installing MySQL
### Debian & derivates
Use either
 
    dpkg -i mysql*deb
or

    gdebi -n mysql*.deb # installs one package at a time
    
    
### Fedora & derivates

    yum -y install mysql-repo.rpm
    yum -y install MySQL-*
    yum -y install mysql-utilities




## Installing MySQL

Check installed files and users
  
        dpkg -l mysql*
        dpkg -L mysql
        id mysql
        find /etc/ -name \*mysql\*

Programs

        client                  server              offline
        mysql                   mysqld              innochecksum
        mysqlbinlog*            mysqld_safe         mysql_config_editor 
        mysqladmin              mysql_install_db    mysqlbinlog*
        mysqlimport
        mysqldump
        


## Installing MySQL
First access
          
        cat /root/.mysql_secret
        mysql -u$USER -p$PASSWORD [ -h$HOST -P$PORT ]
        mysql -e "$QUERY"
  
  
## Installing MySQL - On Ubuntu/Debian
Copy init script and configuration file
        
        cd /opt/mysql/server-5.6/
        cp support-files/mysql.server /etc/init.d/mysql
        cp my.cnf /etc/my.cnf

Create users and directories
        
        useradd mysql -s /usr/sbin/nologin -d /var/lib/mysql
        chown -R mysql:mysql /var/lib/mysql
        
Add a profile script

        cat > /etc/profile.d/Z99-mysql.sh <<'EOF'
        export MYSQL_HOME=/opt/mysql/server-5.6/
        export PATH+=:$MYSQL_HOME/bin:$MYSQL_HOME/scripts
        EOF
        
        
## Installing MySQL - Basic Configuration
Prepare a minimal configuration file...

        # /etc/my.cnf
        [mysqld]
        ...mysql defaults...
        # System user for mysql
        #  create if not exists
        user=mysql
        
        # All data files will go
        #  there
        datadir=/var/lib/mysql
        

## The datadir
Create or recreate the default one (from my.cnf)
  
        mysqld --initialize 

Or create alternative ones
  
        mysqld --initialize --datadir=/data2
        

## The datadir

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

     
  - Application logs
  - DDL definitions .frm and indexes
  - InnoDB log files & tablespaces
  - Binary & Relay Logs (*next lessons)


        
## Installing MySQL
Use different values to run many instances on the same host.

        # /etc/my-1.cnf
        [mysqld]
        ...mysql defaults...
        port=13306
        socket=/data2/mysql.sock
        pid-file=/data2/hostname.pid
        tmpdir=/tmp/data2
        general-log=1
        general-log-file=/data2/hostname.log

Exercise: run the following, check the logs and fix the errors.

        mysqld --defaults-file=/etc/my-1.cnf


# MySQL Service    
## The MySQL Service
Manage as a service
  
        service mysql [start|stop|status]
         
Run standalone

        mysqld [$PARAMETERS]
        
Or wrapped with a restart-daemon
        
        mysqld_safe        


## The MySQL Service
Check the server status at various levels with
     
     mysqladmin ping
     mysqladmin status
     mysqladmin extended-status
     mysqladmin processlist

Using commands

    pgrep -fa mysql         # man pgrep
    ss -tlnp |grep mysql    # ss replaces netstat


## The MySQL Service
Stop mysql via

        mysqladmin shutdown

Or with kill -TERM

        kill -15 $MYSQL_PID

*NEVER kill -9*: this will corrupt your database!

Exercise: what happens if you

  - kill -9 mysql
  - restart with mysqld?  


## Connecting 
Client programs:

- mysql, mysqladmin, mysqlbackup

- full help

        mysql ... [--help [--verbose]] 
        
- connect via socket or forcing TCP

        mysql --socket=/var/lib/mysql/mysql.sock
        mysql --protocol tcp
        
        SHOW DATABASES;

## Connecting - Storing credentials
Store credentials [in the encrypted file](http://dev.mysql.com/doc/refman/5.6/en/mysql-config-editor.html) 
~/.mylogin.cnf using

        mysql_config_editor set 
            --login-path=client # default used by mysql 
            --host=localhost 
            --user=localuser 
            --password # (prompted)

We can define further servers

        mysql_config_editor set
            --login-path=master
            --host=m-1.foo.it
            --port=13306
            --user=admin
            --password # (prompted)


## Connecting
You can log your session in a file with

        mysql --tee=/tmp/history.out
        -- or after login
        TEE /tmp/history.out
        
Dump the output in HTML

        mysql --html
        

