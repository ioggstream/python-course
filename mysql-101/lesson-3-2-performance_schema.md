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

CPU

  - timings of query phases
  - issues in ordering and sorting
  - slow joins


MEMORY

  - cache effectiveness
  - uneffective indexes


