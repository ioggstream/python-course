# Manage tables

## Inspecting tables



## Loading files 

  - Load files from mysql
 
        SOURCE /tmp/world_innodb.sql
 
  - Or via shell
         
         mysql < /tmp/world_innodb.sql


## Cloning tables
You can clone tables with

        CREATE TABLE t2 LIKE t1;
        SELECT * FROM t1 INTO t2;

And populate them using
        
        INSERT INTO foo SELECT * from bar;  

        
## Check tables
Ensure tables are [fine or upgrade-able](http://dev.mysql.com/doc/mysql/en/table-maintenance-sql.html)

        CHECK TABLE d1.t1 [FOR UPGRADE];
        
Gather statistics on a table:
        
        ANALYZE [LOCAL] TABLE d1.t1; -- use LOCAL to avoid spanning on replicas
        
Optimize a table **locking** it:
        
        OPTIMIZE [LOCAL] TABLE d1.t1;

Or via command line (repair is MyISAM only):
        
        mysqlcheck [--check|--analyze|--optimize|--repair]
     
     
## Restore innodb tables        
Follow the [InnoDB documented steps]()

  - stop mysqld and dump the datadir
        
        cp -rp /var/lib/mysql /backup/datadir-dump-$(date +%s)
        
  - start mysqld increasing `--innodb_force_recovery` value from 1 to 6. The lower the better.
  - carefully check the logs
  - if starts successfully dump the broken table
  
        mysqldump brokendb.brokentable > table.sql
        DROP brokendb.brokentable
        
  - restart mysqld without `--innodb-force-recovery`
  - reimport the table
        
        SOURCE table.sql
        
  