# Replication, Scalability and Partitioning
## CAP Theorem
 Partitioning: Synchronization reloaded.

You cannot have the same level of:
 
 - Consistency 
 - Atomicity
 - Partition
 
Instead you have to favor something respect to the other.


## CAP Theorem Reloaded

You can pay to get faster

  - network
  - cpu
  - storage
 
Price is the 4th dimension.


## Replication

Advantges of replication. Use cases.

Synchronous, asynchronous and semi-synchronous replication.

Replication in MySQL. Topologies and GTID.


## Replication

Replication is $asynchronous$ and the agreements are configured on the slave only.

\includegraphics[height=6cm]{images/mysql-replica-hla.jpg}


## Configuring replication
Master
     
  -  produces a changelog named binlog;
  -  grants access to a $replica$ user;
  -  may track slave-updates.

Slave

  -  connects to the master with the $replica$ user
  -  retrieves the binlog and applies the changes;
  -  ```START SLAVE;```
    

## Configuring replication
Enable replication in two or more configuration files like my-3306.cnf, my-3307.cnf.

        [mysqld]
        server-id=3306
        
        log-bin=3306-bin
        # Relay logs are downloaded in
        #  the relay-logs from the Slave I/O
        #  thread
        relay-log=3306-relay

        port=3306
        datadir=/var/lib/3306
        socket=/var/lib/3306/mysql.sock


## Configuring replication

Configure a ```--login-path``` for each instance and validate the connection

        mysql --login-path=3306 -e "show variables like 'port';"

        mysql --login-path=3306 -e "SHOW MASTER STATUS;"

        

##Replication 2.0
MySQL 5.6+ replication is based on Global Transaction ID
  

  -  each server has a unique UUID 
   
        eg: 3E11FA47-71CA-11E1-9E33-C80AA9429562

  -  every TransactionID becomes global

        eg: 3E11FA47-71CA-11E1-9E33-C80AA9429562:32


\includegraphics[height=3cm]{images/mysql-propagate-gtid.jpg}

**If binlog have been purged, you need to import the
master database first!**



## Configuring replication
mysqlreplicate takes care of
  

  -  provisioning the replica user on the master;
  -  configure the slave to point to the master;
  -  start loading the first available transaction in bin-logs;

        mysqlreplicate  --master=$MASTER --slave=$SLAVE \
                --rpl-user=repl:rpass \
                -b
        
  - or provision your user
  
        GRANT REPLICATION CLIENT TO 'repl' INDENTIFIED BY 'repl';



## Configuring replication
mysqldbexport can be used to provision a new slave!
  
  -  check that replica user is provisioned on the master;
  -  issue a ```RESET MASTER;``` to clean up previous settings;

        mysqldbexport > data.sql \
         --server=$MASTER        \ # user:pass@host[:port]
         --export=both           \ # store both schema and data
         --rpl=master            \ # add replication statement
         --rpl-user=repl:rpass   \ #  using the given credentials
         --all

Logical backup and flush table.


## Configuring replication

By default:

  - [Cascade replication](https://dev.mysql.com/doc/refman/5.7/en/replication-options-slave.html) is *OFF* by default.

        # Enable binlog forwarding 
        #  in my.cnf
        log_slave_updates=yes

  - relay logs are deleted asap.

  - relay log size is `1G`

        max_relay_log_size=0  # 0 means the default: 1G ;)
        
  - relay logs are not recovered at startup

        # For crash-safe replication set
        relay_log_recovery=1

## Slave initialization
Clean up old replica configuration before initializing!

        # pre-import.sql
        -- ignore previous changes
        -- and trust the backup
        STOP SLAVE;
        RESET SLAVE ALL;
        RESET MASTER;


## Slave initialization
Large databases can be initialized from disk backups.

        mysqlbackup backup-and-apply-log

Restore with

        mysqlbackup --defaults-file=/etc/my-3307.cnf \ 
            --backup-dir $BACKUP_DIR    \
            --force                     \
            copy-back
                
Get position for old-style replication with 

        grep -r binlog $BACKUP_DIR/meta


## Discovering replication

        mysqlrplshow --master=$MASTER \
            --discover-slaves-login=root:root
        # master on s-1.docker: ... connected.
        # |Finding slaves| for master: s-1.docker:3306
        # Replication Topology Graph
        s-1.docker:3306 (MASTER)
           |
           +--- s-3.docker:3306 - (SLAVE)
           |
           +--- s-4.docker:3306 - (SLAVE)


## Troubleshooting GTID replication

The slave can't apply binary logs due to:

  - slave inconsistencies
  - binlog errors (including file permissions, ...)
  - much more (see docs)
  
To skip some binlog entries, just insert empty transactions instead.

## Troubleshooting GTID replication

The variables governing GTIDs are *note the scope*:

     select @@global.gtid_executed as applied, @@session.gtid_next as next \G
     applied: e311dd97-e9fe-11e6-b4d7-0242ac110005:1-4
     next: automatic
     
To inject an empty transaction:

    STOP SLAVE;
    SET SESSION GTID_NEXT=e311dd97-e9fe-11e6-b4d7-0242ac110005:5;
    BEGIN; COMMIT; -- this is the empty transaction
    SET SESSION GTID_NEXT=automatic;
    START SLAVE;

# Failover
## Failover Basics
A replicated infrastructure can be made Highly Available.
\includegraphics[height=4cm]{images/mysql-promote-slave.jpg}


In case of fault you should:
   
   -  $promove$ your slave!
   -  reconfigure the others to point there
   -  disable the master
   -  eventually switch the ip-address
 

## Failover - I
mysqlfailover takes care of that, and can even discover your
replication topology!

        mysqlfailover --master=$MASTER \
            --discover-slaves-login=root:password \
            --candidates=$SLAVE1,$SLAVE2 \
            --exec-before=/pre-fail.sh \
            --exec-after=/post-fail.sh

**mysqlfailover supports a lot of parameters!
    Read them carefully and test thoroughly your
    solution**


##Failover - II
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



##Failover - III
Run mysqlfailover on an existing infrastructure!

        Master Information
        ------------------
        Binary Log File  Position  Binlog_Do_DB  Binlog_Ignore_DB
        s-1-bin.000009   231
        
        GTID Executed Set
        f01a69cd-df69-11e4-b908-0242ac110009:1-3 [...]
        
---

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



