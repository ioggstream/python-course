# Manage tables

## Inspecting tables


## Cloning tables
You can clone tables with

        sql> CREATE TABLE foo LIKE bar;

And populate them using
        
        sql> INSERT INTO foo SELECT * from bar;  