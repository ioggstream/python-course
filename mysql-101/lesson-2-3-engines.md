## Engines

  - Present Storage Engines
  - InnoDB
  - Memory
  - MyISAM
  
#Memory
## Memory
Paging in MySQL: temporary tables.

Memory and Temporary Tables.

        max_heap_table_size
        max_tmp_table_size
        
## Memory
Creating and managing memory and temporary tables.

Crossing the limits.

#MyISAM
## MyISAM
Features of MyISAM:

  - full-text support
  
Caveats:

  - non transactional
  - no FK
  - hard to recover


## MyISAM
Table format:

  - .frm: table definitions
  - .myd: table data
  - .myi: table indexes for data
  
# InnoDB  
## InnoDB
Transactions and consistency. Foreign Keys.

InnoDB Log Files. Checkpoint interval.

Buffer Pool. Contention on Buffer Pool. Buffer pool instances.

## Configuring InnoDB
Configuring `innodb_buffer_pool_size`.

Inspecting usage.

Configuring `innodb_log_file_size`

## Configuring InnoDB
Tablespaces. 

Configuring and Resizing Tablespaces. AutoExtend.

Ensure innodb_file_per_table=1.

Check innodb datafiles while changing tables.



