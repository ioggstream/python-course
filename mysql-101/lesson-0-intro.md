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


# CAP Theorem
TBD 
    

# CAP Theorem Reloaded

Price is the 4th dimension




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
  
  
