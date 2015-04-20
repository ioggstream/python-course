# Lesson 2 - Agenda
    
- Configuration
- Loading Databases


# Goals

- Configure main parameters
- Get/Set variables
- Set SQL Modes 
- Logging
    - Server
    - Binary | Relay
    - Audit
    
    
# Configuration
Show all mysqld parameters
    
        mysqld --verbose --help
    
    
Read from /etc/my.cnf or via

        mysqld --defaults-file=/etc/my-file.cnf
    
Show running status via

        #mysqladmin variables

Don't explicit default values in the configuration!
     
# Configuration
Configuration file is made up of stanzas

        [client]
        # for mysql, mysqladmin, ...
        
        [server]
        # for mysqld, ..
        
        [mysqld]
        # only for mysqld
        