package main

# Do Not store secrets in ENV variables
secrets_env = [
    "passwd",
    "password",
    "pass",
    "secret",
    "key",
    "access",
    "api_key",
    "apikey",
    "token",
    "tkn"
]

deny[msg] {
    input[i].Cmd == "env"
    val := input[i].Value
    contains(lower(val[_]), secrets_env[_])
    msg = sprintf("Line %d: Potential secret in ENV key found: %s", [i, val])
}

# Only use base images from trusted registries
trusted_registries = [
    "registry.access.redhat.com",
    "ghcr.io/par-tec",
    "docker.io/python",
]
deny_untrusted_base_image[msg] {
    input[i].Cmd == "from"
    val := split(input[i].Value[0], " ")
    trusted_registries_re = concat("|", trusted_registries)
    ret := regex.match(trusted_registries_re, lower(val[0]))
    not ret
    msg = sprintf("Line %d: use trusted, FQDN base image: %s", [i, ret])
}

# Do not use 'latest' tag for base imagedeny[msg] {
deny[msg] {
    input[i].Cmd == "from"
    val := split(input[i].Value[0], ":")
    contains(lower(val[1]), "latest")
    msg = sprintf("Line %d: do not use 'latest' tag for base images", [i])
}

# Avoid curl bashing
deny_curl_bashing[msg] {
    input[i].Cmd == "run"
    val := concat(" ", input[i].Value)
    matches := regex.find_n("(curl|wget)[^|^>]*[|>]", lower(val), -1)
    count(matches) > 0
    msg = sprintf("Line %d: Avoid curl bashing", [i])
}

# Do not upgrade your system packages
upgrade_commands = [
    "dist-upgrade",
]

deny[msg] {
    input[i].Cmd == "run"
    val := concat(" ", input[i].Value)
    contains(val, upgrade_commands[_])
    msg = sprintf("Line: %d: Do not upgrade your distribution", [i])
}

# Do not use ADD if possible
deny[msg] {
    input[i].Cmd == "add"
    msg = sprintf("Line %d: Use COPY instead of ADD", [i])
}

# Do not root
any_user {
    input[i].Cmd == "user"
 }

deny_root_user[msg] {
    not any_user
    msg = "Do not run as root, use USER instead"
}

# Do not sudo
deny[msg] {
    input[i].Cmd == "run"
    val := concat(" ", input[i].Value)
    contains(lower(val), "sudo")
    msg = sprintf("Line %d: Do not use 'sudo' command", [i])
}

exception[rules] {
  input[i].Cmd == "from"
  input[i].Value[0] == "maven:3.8.7-eclipse-temurin-11"

  rules := ["untrusted_base_image"]
}
