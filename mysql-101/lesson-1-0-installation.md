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

For 5.7 community, install the public repo

    yum -y install https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
    yum -y install mysql-community-server mysql-community-client
    yum -y install mysql-utilities


For 5.7 commercial

    yum -y install  mysql-commercial-server mysql-commercial-client
    yum -y install  mysql-shell-commercial mysql-router-commercial
    yum -y install  meb



## Installing MySQL

Check installed files and users

        rhel$ rpm -qa mysql\* | xargs rpm -ql
        deb $ dpkg -l mysql*
        deb $ dpkg -L mysql
        id mysql
        find /etc/ -name \*mysql\*

Programs

        client                  server               offline
        mysql                   mysqld               innochecksum
        mysqlbinlog*            mysqld_safe          mysql_config_editor
        mysqladmin              mysql_install_db^    mysqlbinlog*
        mysqlimport
        mysqldump



## Installing MySQL

First access

        grep pass /var/log/mysqld.log
        2018-01-08T10:42:22.221149Z 1 [Note] A temporary password is generated for root@localhost: Cewoi.zFp99g
        mysql -u$USER -p$PASSWORD [ -h$HOST -P$PORT ]
        mysql -e "$QUERY"

In old releases, password was there:

        cat /root/.mysql_secret


## Installing MySQL - On Ubuntu/Debian

Copy init script and configuration file

        cd /opt/mysql/server-5.7/
        cp support-files/mysql.server /etc/init.d/mysql  # for non systemd versions.
        cp my.cnf /etc/my.cnf

Create users and directories

        useradd mysql -s /usr/sbin/nologin -d /var/lib/mysql
        chown -R mysql:mysql /var/lib/mysql

Add a profile script

        cat > /etc/profile.d/Z99-mysql.sh <<'EOF'
        export MYSQL_HOME=/opt/mysql/server-5.7/
        export PATH+=:$MYSQL_HOME/bin:$MYSQL_HOME/scripts
        EOF


## Installing MySQL - Basic Configuration
Prepare a minimal configuration file...

        # /etc/my.cnf
        [mysqld]
        ...mysql defaults...
        # System user for mysql
        #  create if not exists.
        user=mysql

        # All data files will go
        #  there.
        datadir=/var/lib/mysql

        # Create the undo tablespace and
        #  reduce disk usage.
        innodb_undo_tablespaces=2
        innodb_log_file_size=5M


## The datadir
Create or recreate the default one (from my.cnf)

        mysqld --initialize

Or create alternative ones (configure selinux/apparmor before!)

        mysqld --initialize --datadir=/data2

A new password is generated each time you initialize the datadir

        grep pass /var/log/mysqld.log
        2018-01-08T10:42:22.221149Z 1 [Note] A temporary password is generated for root@localhost: Cewoi.zFp99g



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
    |-- [mysql    mysql     12M]  undo001
    `-- [mysql    mysql       0]  mysql.sock


  - Application logs
  - DDL definitions .frm and indexes
  - InnoDB log files & tablespaces
  - Binary & Relay Logs (*next lessons)


## Relocating datadir and ports

You should tune security systems when relocating datadirs.

SElinux:

        # Allow mysql on another port.
        semanage port -a -t mysqld_port_t -p tcp 13306 

        # Allow mysql to operate on files in /datadir and beyond.
        semanage fcontext -a -t mysqld_db_t "/datadir(/.*)?"
        restorecon -Rv /datadir

AppArmor:

        # in /etc/apparmor.d/local/usr.sbin.mysqld
        /diskb/data/ r,
        /diskb/data/** rwk,
        /diskb/log/ r,
        /diskb/log/** rwk,
        /diskc/backup/ r,
        /diskc/backup/** rwk,

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

        systemctl [start|stop|status] mysql

Run standalone

        mysqld [$PARAMETERS]

Or wrapped with a [restart-daemon](https://dev.mysql.com/doc/refman/5.7/en/mysqld-safe.html) in [non systemd distros](https://dev.mysql.com/doc/refman/5.7/en/using-systemd.html)

        mysqld_safe

## First login

The first login requires a password change.

Exercise: get the password generated by the mysql initializer.

Exercise: use mysqladmin to change the password

    mysqladmin password -p  # this will prompt for the old and new password.


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
Stop mysql either via

        mysqladmin shutdown

with kill -TERM

        kill -15 $MYSQL_PID

or since 5.7

        SHUTDOWN  -- provided you have the SHUTDOWN privilege.

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


