paulrentschler.security
=======================

[![MIT licensed][mit-badge]][mit-link]

Apply good security practices to Ubuntu Linux machines.

Requirements
------------

None.


Role Variables
--------------

The following variables are available with defaults defined in `defaults/main.yml`:

### auditd-related variables

Specify a larger than normal buffer to handle more messages.

    security_auditd_buffer_size: 8192

Set the failure mode to `panic`.

    security_auditd_failure_mode: 2

Enable Kerberos 5 for authentication and encryption.

    security_auditd_enable_kerberos: no


### login-related variables

Specify the number of concurrent logins for each user.

    security_maxlogins: 10

Specify the number of seconds of inactivity before a user is logged out (default: 1 hour = 3600 seconds).

    security_login_timeout: 3600


### password-related variables

Set the maximum number of days a password may be used before a change is required. (-1 will disable this restriction)

    security_password_max_days: -1

Set the minumum number of days allowed between password changes. (-1 will disable this restriction)

    security_password_min_days: 1

Set the maximum number of login retries.

    security_password_max_retries: 3

Set the maximum amount of time in seconds for the login.

    security_password_login_timeout: 60

Set the number of seconds before being allowed another attempt after a login failure.

    security_password_fail_delay: 4


### PAM-related variables

PAM is an extremely flexible but complicated tool and small changes can have drastic consequences, as such this role does little to MODIFY any existing PAM configuration but rather backs up and REPLACES the configuration with new files.

If you have a custom PAM configuration that cannot be met with the settings provided below, you should probably opt to set `security_pam_harden` to `no` which will skip any tasks related to configuring PAM.


Skip the PAM security configuration steps completely by setting this to `no`.

    security_pam_harden: yes

Define the minimum uid used for non-local accounts.

    security_pam_minimum_uid: 1000

Number of passwords to remember to avoid frequent password alternation.

    security_pam_password_history_count: 5

Enable account lockouts for too many failed login attempts.

    security_pam_account_lockouts: yes

Number of failed attempts before the account is locked.

    security_pam_failed_attempts_max: 25

Number of seconds to wait before automatically unlocking an account.

    security_pam_account_unlock_time: 900


#### PAM-authentication options

Allow successful login credentials to be cached in case of network issues.

    security_pam_cache_credentials: yes

Allow access restrictions based on host, domain, IP address, etc. to be specified in `/etc/security/access.conf` by setting this to `yes`.

    security_pam_use_login_access_restrictions: no

Authenticate against a Kerberos server.

    security_pam_use_krb5: no

Lookup users/groups in an LDAP server.

    security_pam_use_ldap: no

Configure second-factor authentication with Duo (install Duo with the *paulrentschler.duo* role).

    security_pam_use_duo: no

Use Duo 2FA for local unix accounts (by default, used for external accounts in Kerberose or LDAP only).

    security_pam_duo_local_users: no

Path to the Duo PAM module.

    security_pam_duo_module_path: /lib64/security/pam_duo.so


### SSH-related variables

Specify the SSH port to use (default: 22 -- not recommended)

    security_sshd_port: 22

Specify the users allowed to SSH into the server.

Each entry must have a "name" attribute that specifies the username

Each entry can have an optional "host" attribute

Example:
```yaml
security_ssh_users:
  - tom:
      name: tom
      host: 192.168.0.*
  - user2:
      name: jane
  - {name: joan, host: 192.168.0.150}
```

    security_ssh_users: []

Specify the groups allowed to SSH into the server.

Each entry must have a "name" attribute that specifies the group name

Each entry can have an optional "host" attribute

    security_ssh_groups: []

Specify the users with specific (and limited) SFTP access.

Each entry must have a "name" attribute that specifies the username

The following optional attributes (with their default values) are supported:

  * 'chroot' -- specify the chroot jail directory (default: %h/public_html)
  * 'x11forwarding' -- is X11 forwarding permitted? (default: no)
  * 'allowagentforwarding' -- is ssh-agent forwarding permitted? (default: no)
  * 'allowtcpforwarding' -- is TCP forwarding permitted? (default: no)

        security_sftp_users: []


### sudo-related variables

Prevent users from being granted sudo rights without needing a password by changing this value to `yes`.

    security_block_passwordless_sudo: no

**NOTE**: This only prevents **the role** from adding entries to the `sudoers` file that would grant users password-less sudo rights. It does not prevent password-less sudo if the file is manually edited.

List of specific usernames that are allowed unrestricted sudo use.

    security_sudo_users: []

List of specific usernames that are allowed unrestricted sudo use **WITH NO PASSWORD!** (this should be used VERY sparingly)

    security_sudo_nopasswd_users: []

List of specific groups that are allowed unrestricted sudo use. (this is discouraged for a more secure system)

    security_sudo_groups: []


Dependencies
------------

None.


Example Playbook
----------------

Simple version:

    - hosts: all
      roles:
        - paulrentschler.security


With customizations:

    - hosts: all
      roles:
        - { role: paulrentschler.security,
            security_sshd_port: 2222,
            security_sudo_users: ["fred", "jane"],
            }


License
-------

[MIT][mit-link]


Author Information
------------------

Created by Paul Rentschler in 2021.


[mit-badge]: https://img.shields.io/badge/license-MIT-blue.svg
[mit-link]: https://github.com/paulrentschler/ansible-role-security/blob/master/LICENSE
