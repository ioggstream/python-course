-- Initialize mysql with the following file.
-- https://dev.mysql.com/doc/refman/5.7/en/group-replication-user-credentials.html
SET SQL_LOG_BIN=0;
CREATE USER IF NOT EXISTS 'root'@'%';
ALTER USER 'root'@'%' IDENTIFIED BY 'Secret%2017';
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Secret%2017';

CREATE USER  IF NOT EXISTS rpl_user@'%' IDENTIFIED BY 'Secret%2017';
GRANT REPLICATION SLAVE ON *.* TO rpl_user@'%';

FLUSH PRIVILEGES;
SET SQL_LOG_BIN=1;

-- Enable whitelist.
STOP GROUP_REPLICATION;
SET GLOBAL group_replication_ip_whitelist="172.17.0.0/16,127.0.0.1/8";
START GROUP_REPLICATION;

-- Set this stuff.
CHANGE MASTER TO MASTER_USER='rpl_user', MASTER_PASSWORD='password' FOR CHANNEL 'group_replication_recovery';
