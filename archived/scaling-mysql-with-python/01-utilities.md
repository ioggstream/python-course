#MySQL

##MySQL

  - Single-process, multi-thread
  - 2-tier architecture
    *  Connection + SQL
    *  Storage Backend
  - Greatly improved in 5.6
  - More to come in 5.7: Dynamic Buffers \& Multi\-source replication


##MySQL
Many Backends aka Storage Engines:

  - InnoDB[^default]: ACID, MVCC[^MVCC], Redo\|Undo logs;
  - Memory: fast \& volatile;
  - NDB: MySQL Cluster, network distributed, auto-sharded;

Replication based on changelog files (binary logs).

[^MVCC]: Multi Versioning Concurrency Control
[^default]: default


##Manage \& Use a database
\columnsbegin

\column[t]{.5\textwidth}
Monitor:

  - Database size: Tables, Indexes,
        Binary Logs

  - Replication inconsistencies

  - Failover

\column[t]{.5\textwidth}
Connect:

  - Native Drivers

    * for Python 2.6, 2.7 and 3.3
    * SSL \& compression

  - Orchestrate

\columnsend


~~Download scripts from some blog, add random queries from docs.mysql.com, Shake.~~



#Python Utilities

##MySQL Utilities
A python package with **utilities, drivers, fabric orchestrator**

\columnsbegin
\column{.5\textwidth}

        $ wget http://bit.ly/1CxNuZe
        $ tar xf mysql-utilities-1.6.1.tar.gz
        $ cd mysql-utilities-1.6.1
        $ python setup.py install


\column{.5\textwidth}

         mysql-utilities-1.6.1
           |-- mysql
           |-- connector
           |   |-- django
           |   `-- fabric
           |-- fabric
           |   |-- protocols
           |   |-- providers
           |   `-- services
           `-- utilities

\columnsend


##MySQL Utilities:
Start with ```mysqluc``` for a single entrypoint

  - entrypoint for all utilities
  - contextual help
  - TAB completion

Or access each utility separately.

Specify server URIs as `user:pass@host[:port]`.


##MySQL Utilities


        mysqluc> help utilities

          Utility            Description
        -----------------  --------------------------------------------------------
        mysqlauditadmin    audit log maintenance utility
        mysqlauditgrep     audit log search utility
        ...
        mysqldbcompare     compare databases for consistency
        ...
        mysqldiskusage     show disk usage for databases
        mysqlfailover      automatic replication health monitoring and failover


##Disk Usage
A single command to show all disk usage infos (excluded system logs)


        $ mysqldiskusage --all --server=$SERVER
        ...
        | db_name             |     total  |
        | akonadi             | 969150919  |
        ...
        Total database disk usage = 971233529 bytes or 926,24 MB
        ...
        | ib_logfile0  | 67108864  |
        | ib_logfile1  | 67108864  |
        | ibdata1      | 44040192  |
        Total size of InnoDB files = 178257920 bytes or 170,00 MB


# Connectors

## Connectors

        from django.db.backends import BaseDatabaseValidation

        if django.VERSION < (1, 7):
            from django.db import models
        else:
            from django.core import checks
            from django.db import connection


        class DatabaseValidation(BaseDatabaseValidation):
            if django.VERSION < (1, 7):


#Replication

##Log-based Replication: Master
Replication is $asynchronous$ or $semi-synchronous$.

A Master with a Unique Server ID

  -  produces a changelog named **binary log**;
  -  assign each transaction a Global Transaction ID;
  -  grants access to a $replica$ user;

Optionally:

  -  stores replication infos in ACID tables;
  -  may track slave-updates;
  -  waits for one slave ack on $semi-synchronous$ replication;


##Log-based Replication: Slave
\columnsbegin
\column{.7\textwidth}
Slave

  -  connects to the master as the $replica$ user;
  -  retrieves the binlog;
  -  applies the changes;
  -  $\forall$ slave $\exists !$ master;

Optionally

  - forbids local changes from non-root users;

\column{.3\textwidth}

\includegraphics[height=6cm]{images/mysql-replica-1.png}

\columnsend

\centering If binlogs have been purged, you need to import the
master database first!


##Benefits of replication
\columnsbegin
\column[t]{.5\textwidth}

  * Availability.

  * Scaling reads with R/W split.

  * Scaling reads differencing indexes.

  * Backup and data warehouse strategies.

\column[t]{.5\textwidth}

        # mysqlrplshow output
        #
        # Replication Topology Graph
        s-1.docker:3306 (MASTER)
           |
           +--- s-3.docker:3306 - (SLAVE)
           |
           +--- s-4.docker:3306 - (SLAVE)

\columnsend

##mysqlreplicate
Configuring replication with one command:

        mysqlreplicate  -b --pedantic \
            --master=$MASTER --slave=$SLAVE --rpl-user=repl:rpass

\columnsbegin
\column[t]{.5\textwidth}

        # master uuid = 2cda700...
        #  slave uuid = 7520cf0...
        # Checking for binary logging on master...
        # Granting replication access to
        #   replication user...
        # Connecting slave to master...
        # CHANGE MASTER TO MASTER_HOST = '172.17.0.5',...

\column[t]{.5\textwidth}

  -  preliminary checks;
  -  create $replica$ user on the master;
  -  point the slave to the master;
  -  start loading the first available transaction in binlogs;

\columnsend


##Initialize new slaves
Beware!

  1. Avoid replicating user provisioning and other host-related setup!

        @SESSION.SQL_LOG_BIN=0;

  2. Binlogs are usually retained for a fixed period - eg 15days.

To provision new slave after that period you must:

 - start from a backup or a snapshot;
 - apply the binlogs.

        mysqldbexport >> data.sql --server=root:pass@master --rpl-user=repl:rpass \
            --export=both --rpl=master --all
        mysqldbimport --server=root:pass@slave data.sql


#Failover

##Failover Basics
From replication to high availability, automagically discovering slaves.

\columnsbegin

\column[t]{.5\textwidth}

  -  $promote$ the most updated slave
  -  reconfigure the others
  -  disable the master
  -  eventually fix ip-address

\includegraphics[width=3.5cm]{images/mysql-failover-1.png}

\column[t]{.5\textwidth}

    # Read carefully the docs of
    #  mysqlfailover and of all
    #  the supported parameters!
    mysqlfailover --master=$MASTER \
    --discover-slaves-login=root:password \
    --candidates=$SLAVE1,$SLAVE2 \
    --exec-before=/pre-fail.sh \
    --exec-after=/post-fail.sh

\columnsend
