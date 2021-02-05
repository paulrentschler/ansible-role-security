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


### SSH-related variables

Specify the SSH port to use (default: 22 -- not recommended)

    security_sshd_port: 22


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
