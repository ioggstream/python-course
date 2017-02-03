## Monitoring 

  - Enterprise Monitor:  java web application to be used with or without agent
  - Agents: java daemon gathering infos from one or more mysqld

  
## Setup Monitoring
Download from the website:

  - mem installer
  - agent installer

There's no rpm/deb!


## Installing MEM

Prepare the configuration file

        # ./mem.sh --help > mem-setup.rsp
        
Modify and backup setup.rsp

        # vi mem-setup.rsp
        
Install

        #./mem.sh --answer-file mem-setup.rsp ...
        
Remember to configure logrotate!
        
        
## Using MEM

Connect to the webapp and provide the first credentials.

Start monitoring some servers without agents.


## Installing Agents

Prepare the configuration file collecting data for:

  - `root` user access to the monitored instances 
  - `agent`, `general`, `limited` user

        # ./agent.sh --help > mem-setup.rsp
        
Modify and backup setup.rsp

        # vi mem-setup.rsp
        
Install

        #./mem.sh --answer-file mem-setup.rsp ...


## Attaching Agents
Monitor servers via mysql-agents


## Auditing

Install the audit plugin, producing an external log file.

        INSTALL PLUGIN audit_log SONAME 'audit_log.so';
        
Enable audit at startup so that you can't disable it online. 

        [mysqld]
        plugin-load=audit_log.so
        audit-log=FORCE_PLUS_PERMANENT
        
## Audit
Check audit logs.

Errors if you try to remove it.
