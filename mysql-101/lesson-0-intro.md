# MySQL 101

Goal:

  - What is a database
  - ACID and non-ACID database
  - The CAP Theorem
  - MySQL HLA
    - Connections
    - Processing
    - Archiving
  - Memory & Disk usage




# What is a database

  - Adding data: a single-connection in-memory database.
  
  - Durability: making data persistent. Checkpoints. Memory vs Storage speed. I/O bound.
    
  - Buffering: serving requests during checkpoints. 
  
  - Performance impacts of durability.


# What is a database

  - Isolation: serving multiple connections. Synchronization. CPU bound.
  
  - Reading data: finding data. Indexes. Indexes are not a free ride. 
    
  - Caching: Memory vs Storage speed. Index memory. Memory is not $\infty$

  - SQL: adding a language layer. Overhead of SQL. 


# What is a database

  - Consistency
  - Atomicity
  - Transactions


# What is a database

  - Partitioning: Synchronization reloaded.


# CAP Theorem
You cannot have the same level of:
 
 - Consistency 
 - Atomicity
 - Partition
 
Instead you have to favor something respect to the other.


    

# CAP Theorem Reloaded

But you can pay for having more!
 
Price is the 4th dimension.




# MySQL Overview - 
## HLA

  - v. image SG1§49
  - Connection (TCP, Unix, Threads, Authentication) 
    
        --skip-name-resolve || --host-cache-size to grow internal cache

  - SQL Parser / Optimizer (Caches, Authorization)

  - Query exec / cache / logging

  - Storage Engines (Disk, Memory, Network)

# MySQL Overview - 
## Memory usage
  - Connections
  - Internal Buffer/Caches
  - OS Buffer/Caches

# MySQL Overview - 
## Storage Engines

  - Enable persistency
  - Transactional: InnoDB, NDB
  - Non Transactional: MyISAM, Memory,
  
  
