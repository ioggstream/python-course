# Manage tables

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
Ensure tables are [fine or upgrade-able](http://dev.mysql.com/doc/mysql/en/table-maintenance-sql.html) stopping on errors:

        CHECK TABLE d1.t1 [FOR UPGRADE];  -- implies 
        
Update statistics on a table **read-locking** it:
        
        ANALYZE [LOCAL] TABLE d1.t1; -- use LOCAL to avoid spanning on replicas
        
Optimize a table **locking** it:
        
        OPTIMIZE [LOCAL] TABLE d1.t1;

Or via command line (**repair is MyISAM only**):
        
        mysqlcheck [--check|--analyze|--optimize|--repair]

`--repair` may corrupt a table: **always backup before**


     
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
        
  

## Altering tables

Tables can be *altered*:

        ALTER TABLE d1.t1 
            ADD COLUMN newcol timestamp default current_timestamp(),
            MODIFY COLUMN name varchar(4),
            DROP COLUMN ip;  

Where possible, mysql takes care of reshaping data.
             
             
## Partitioning

Altering includes partitioning too:

        ALTER TABLE d1.t1
            PARTITION BY RANGE(id) ( 
                PARTITION p1 VALUES LESS THAN (10), 
                PARTITION p2 VALUES LESS THAN (20), 
                PARTITION p3 VALUES LESS THAN (30)
            );

You can partition by:

  - HASH, KEY: dynamic, with some limitations
    - support `LINEAR` hashing
  - RANGE, LIST: static, less limitation
    - support multiple `COLUMN` 
  


## Partitioning

A RANGE partition accepts only allowed values.
 
        INSERT INTO d1.t1 (id, name) VALUES
            (15, "nooo"),       -- stops at the first error
            (4, "neither");

Fix and add partitions

        ALTER TABLE d1.t1 ADD PARTITION (   
            PARTITION p4 VALUES LESS THAN (10000),
            PARTITION p_max VALUES LESS THAN (MAXVALUE)  -- MAXVALUE is a keyword!
        );
            
Populate the table:

        INSERT INTO d1.t1 (id, name) VALUES
            (1), (11), (21), (101);
            
## Partitioning - recap

Like columns:
 
   - partitions can be added or dropped;

    ALTER TABLE d1.t1 DROP PARTITION (p1, p4);

   - dropping partitions alters table definition;

    SHOW CREATE TABLE d1.t1;

   - data is dropped too.

    SELECT * from d1.t1;


## Partitioning - recap

You can:

  - REORGANIZE PARTITIONS (eg. split them) as you can't add further partitions after `MAXVALUE`
  
        ALTER TABLE d1.t1 
            REORGANIZE PARTITION p_max INTO (  
                PARTITION p5 VALUES LESS THAN (20000),
                PARTITION p_max VALUES LESS THAN (MAXVALUE)
            )

  - TRUNCATE PARTITION without ALTERING DDL 
   
        ALTER TABLE .. TRUNCATE PARTITION p1, p3;


## Partitioning - syntax

The followings are **lists**. 
They are always enclosed by `()` even when list length is 1.

  - partition definitions 
  
        .. ADD PARTITION ( 
            PARTITION p1 ...,
            PARTITION p2 ...,
             )
  
  - partition boundaries 
  
        .. PARTITION p4 VALUES LESS THAN (5) .. -- just one item
        -- OR
        .. PARTITION p4 VALUES LESS THAN (5,1,1) .. -- more items
   

[See doc for further info](https://dev.mysql.com/doc/refman/5.7/en/partitioning-columns-range.html) 


## Partition by HASH

Re-partition by hash with 4 partition is just

        ALTER TABLE d1.t1 PARTITION BY HASH(id) PARTITIONS 4;
        
Check the outcome:
      
        SELECT * FROM INFORMATION_SCHEMA.PARTITIONS 
            WHERE TABLE_NAME='t1' LIMIT 1 \G

Exercise: 

  - repartition by hash with 10 partitions.
  - try to drop an hash-partition.


## Partition variants

You can hash-partition using a UDF or just use a table's key.

          CREATE TABLE plhk1 (id int not null auto_increment primary key,
             PARTITION BY LINEAR KEY (id) PARTITIONS 4);

Or with multiple columns 

        CREATE TABLE prc1 (id int not null, name varchar(4), 
            PARTITION BY RANGE COLUMNS(id,name)
        );


Columns and UDF arguments must be `UNIQUE`.

## Maintaining partitions

Partitioning simplifies table maintenance.

Just recreate/rework a single partition

        ALTER TABLE t1 OPTIMIZE PARTITION p0, p1;

        ALTER TABLE t1 ANALYZE PARTITION p3;


## Partitioning limitations 

Each partition is actually a separate innodb table:

  - more open files
  - indexes are per-partition
    - no foreign keys 
    - no `FULLTEXT` 


[see doc for further limitations](https://dev.mysql.com/doc/refman/5.7/en/partitioning-limitations.html)


