# Author: Jim Li
# Date: 21 May 2021
# Converts /var/log/auth.log (SSH Log) into separate logs, each
# with distinct categories.

grep sshd.\*Accepted /var/log/auth.log > acceptances.txt
grep sshd.\Failed /var/log/auth.log > failures.txt
