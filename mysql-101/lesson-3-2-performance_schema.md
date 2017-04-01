# Performance Schema

## `use performance_schema`

  - Engine that gathers server statistics

  - data exposed under  `performance_schema`

  - metrics can be enabled or disabled

  - variable memory and CPU overhead

  - 5.7 provides summary tables

        USE sys;  -- another database


## `use performance_schema`

I/O

  - accessed files
  - threads in disk wait 
  - table scans
  - connections attributes
  - 

CPU

  - timings of query phases / exercited mysql code
  - issues in ordering and sorting
  - slow joins
  - locked innodb rows

MEMORY

  - cache effectiveness
  - uneffective indexes


## setup_instruments

Instrumenting is costly. You can be picky:

        SELECT  * FROM setup_instruments;
        ...

Or `USE sys` and just check overviews.

Use `information_schema` to find instruments & co:

        SELECT table_name,column_name FROM information_schema.columns 
            WHERE column_name LIKE '%lock%' 
                AND table_schema LIKE 'perf%';     
