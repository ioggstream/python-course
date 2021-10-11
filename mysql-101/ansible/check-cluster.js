try {
    cluster = dba.getCluster('prod');
    exit(0);
} catch (err) {
    // cluster does not exist.
}

uri = 'root@localhost:3306'
dba.verbose = 8
ret = dba.checkInstanceConfiguration(uri, {"password": "Secret%2017"})

if (ret["status"] != "ok") {
    exit(1);
}

ret_config = dba.configureLocalInstance(uri, {
    "password": "Secret%2017",
    "mycnfPath": "/etc/my.cnf",
    "clusterAdmin": "'icroot'@'%'",
    "clusterAdminPassword": "Secret%2017",
    "clearReadOnly": true}
    )

if (ret_config["status"] != "ok") {
    exit(1);
}
