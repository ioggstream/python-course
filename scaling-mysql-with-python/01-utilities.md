#MySQL \& Replication

##MySQL

  - Single-process, multi-thread.
  - 2-tier architecture: Connection + SQL, Storage Backend.
  - Greatly improved in 5.6, more to come in 5.7 including

 Dynamic Buffers \& Multi\-source replication 
 
 
##MySQL
Many Backends aka Storage Engines:

  - InnoDB[^default]: ACID, MVCC[^MVCC], Redo\|Undo logs;
  - Memory: fast \& volatile;
  - NDB: MySQL Cluster, network distributed, auto-sharded;

Replication based on changelog files (binary logs).

[^MVCC]: Multi Versioning Concurrency Control
[^default]: default


##Administration
Monitor:

  - Database size: Tables, Indexes, Binary Logs
  - Replication inconsistencies
  - Failover

Connect:

  - Native Drivers
  - Orchestrate
  
Keep it simple!
 

#mysql-utilities

##MySQL Utilities
A python package
\columnsbegin
\column{.5\textwidth}

        $ wget http://bit.ly/1CxNuZe -O mysql-utilities-1.6.1.tar.gz
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

*utilities*, *drivers*, *fabric orchestrator*

##MySQL Utilities:
Start with ```mysqluc``` for a single entrypoint

  - entrypoint for all utilities
  - contextual help
  - TAB completion
  
Or access each utility separately.

Server URIs are specified as
 
        user:pass@host[:port]

  
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



#Replication

##Log-based Replication: Master
Replication is $asynchronous$ or $semi-synchronous$.

A Master with a Unique ID
     
  -  produces a changelog named *binary log*;
  -  assign each transaction a GTID;
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

**If binlog have been purged, you need to import the
master database first!**


##Benefits of replication

Availability.

Scaling reads \& indexes.

Backup and data ware-house strategies.


##mysqlreplicate
Configuring replication with one command:

  -  create $replica$ user on the master;
  -  point the slave to the master;
  -  start loading the first available transaction in binlogs;

        mysqlreplicate  --master=$MASTER --slave=$SLAVE \
            --rpl-user=repl:rpass \
            -b --pedantic

        # master on 192.168.1.1: ... connected.
        # slave on 192.168.1.2: ... connected.
        # Checking InnoDB statistics for type and version conflicts.
        # Checking for binary logging on master...
        # Setting up replication...
        # ...done.


##mysqlrplshow X
Discovering replication

        $ mysqlrplshow --master=$MASTER \
            --discover-slaves-login=user:pass
        # master on s-1.docker: ... connected.
        # |Finding slaves| for master: s-1.docker:3306
        # Replication Topology Graph
        s-1.docker:3306 (MASTER)
           |
           +--- s-3.docker:3306 - (SLAVE)
           |
           +--- s-4.docker:3306 - (SLAVE)


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
A replicated infrastructure can be made Highly Available.
\includegraphics[height=4cm]{images/mysql-promote-slave.jpg}


In case of fault you should:
   
   -  $promove$ the most updated slave!
   -  reconfigure the others to point there
   -  disable the master
   -  eventually switch the ip-address or use an HA driver.
 

##mysqlfailover - I
mysqlfailover does everything, and can even discover your
replication topology!

        $ mysqlfailover --master=$MASTER \
            --discover-slaves-login=root:password \
            --candidates=$SLAVE1,$SLAVE2 \
            --exec-before=/pre-fail.sh \
            --exec-after=/post-fail.sh

**mysqlfailover supports a lot of parameters!
    Read them carefully and test thoroughly your
    solution**


##Failover - II XXX
Run mysqlfailover on an existing infrastructure!
        
        $ mysqlfailover --master=$MASTER \
         --discover-slaves-login=root:root
        # Discovering slaves for master at s-1.docker:3306
        # Discovering slave at s-3.docker:3306
        # Found slave: s-3.docker:3306
        # Discovering slave at s-4.docker:3306
        # Found slave: s-4.docker:3306
        # Checking privileges.
        ...



##Failover - III XXX
Run mysqlfailover on an existing infrastructure!

        Master Information
        ------------------
        Binary Log File  Position  Binlog_Do_DB  Binlog_Ignore_DB
        s-1-bin.000009   231
        
        GTID Executed Set
        f01a69cd-df69-11e4-b908-0242ac110009:1-3 [...]
        

        MySQL Replication Failover Utility
        Failover Mode = auto     Next Interval = Sun Apr 12 14:32:40 2015
        ...
        Replication Health Status
        +-------------+-------+---------+--------+------------+---------+
        | host        | port  | role    | state  | gtid_mode  | health  |
        +-------------+-------+---------+--------+------------+---------+
        | s-1.docker  | 3306  | MASTER  | UP     | ON         | OK      |
        | s-3.docker  | 3306  | SLAVE   | UP     | ON         | OK      |
        | s-4.docker  | 3306  | SLAVE   | UP     | ON         | OK      |
        +-------------+-------+---------+--------+------------+---------+

