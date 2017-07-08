[defaults]
inventory = ../exercise-04/inventory-docker-solution.py
private_key_file = ../exercise-01/id_ansible
retry_files_enabled = no
host_key_checking = no

[ssh_connection]
ssh_args = -o StrictHostKeyChecking=no  -o UserKnownHostsFile=/dev/null
