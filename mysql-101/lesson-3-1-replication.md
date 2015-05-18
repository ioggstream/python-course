##Configuring replication

Replication is $asynchronous$ and the agreements are configured on the slave only.

\includegraphics[height=6cm]{images/mysql-replica-hla.jpg}


## Configuring replication
Master
     
  -  produces a changelog named binlog;
  -  grants access to a $replica$ user;
  -  may track slave-updates.

Slave

  -  connects to the master with the $replica$ user
  -  retireves the binlog and applies the changes;
  -  ```START SLAVE;```
    


##Replication 2.0
MySQL 5.6+ replication is based on Global Transaction ID
  

  -  each server has a unique UUID 
   
        eg: 3E11FA47-71CA-11E1-9E33-C80AA9429562

  -  every TransactionID becomes global

        eg: 3E11FA47-71CA-11E1-9E33-C80AA9429562:32


\includegraphics[height=3cm]{images/mysql-propagate-gtid.jpg}

**If binlog have been purged, you need to import the
master database first!**



##Configuring replication
mysqlreplicate takes care of
  

  -  provisioning the replica user on the master;
  -  configure the slave to point to the master;
  -  start loading the first available transaction in bin-logs;


        mysqlreplicate  --master=$MASTER --slave=$SLAVE \
                --rpl-user=repl:rpass \
                -b
    
        # master on 192.168.1.1: ... connected.
        # slave on 192.168.1.2: ... connected.
        # Checking for binary logging on master...
        # Setting up replication...
        # ...done.




##Configuring replication - II
mysqldbexport can be used to provision a new slave!
  

  -  check that replica user is provisioned on the master;
  -  issue a ```RESET MASTER;``` to cleannup previous settings;
  -  add ```--rpl=master``` to create replica infos in the sql;
  -  add ```--export=both``` to store both schema and data;


        # pre-import.sql
        -- ignore previous changes
        -- and trust the backup
        STOP SLAVE;
        RESET MASTER;


        mysqldbexport > data.sql \
         --server=$MASTER \
         --rpl-user=repl:rpass \
         --export=both \
         --rpl=master --all


##Discovering replication

        $ mysqlrplshow --master=$MASTER \
            --discover-slaves-login=root:root
        # master on s-1.docker: ... connected.
        # |Finding slaves| for master: s-1.docker:3306
        # Replication Topology Graph
        s-1.docker:3306 (MASTER)
           |
           +--- s-3.docker:3306 - (SLAVE)
           |
           +--- s-4.docker:3306 - (SLAVE)


%
% Failover
%

# Failover
## Failover Basics
A replicated infrastructure can be made Higly Available.
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



