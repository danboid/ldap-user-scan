# ldap-user-scan.py by Dan MacDonald

# Requires python3-ldap and python3-numpy.

# Usage example:

# python3 ldap-user-scan.py users.txt

# Where users.txt is a text file with one user name per line.
# It will print the users in the file missing from the LDAP server.

import ldap, sys
import numpy as np

l=ldap.initialize('ldap://INSERTLDAPSERVERADDRESS')
l.set_option(ldap.OPT_REFERRALS, 0)
l.simple_bind_s('LDAPUSER', 'LDAPUSERPASSWORD')
base_dn='dc=YOUR,dc=DOMAIN,dc=HERE'

users = np.loadtxt(sys.argv[1], dtype='str')

for user in users:
    user_filter = '(&(objectClass=person)(sAMAccountName={user}))'.format(user=user)
    user_data=l.search_ext_s(base_dn, ldap.SCOPE_SUBTREE, user_filter)
    # If there is no user data in the returned tuple, print the user name
    if len(user_data) < 4:
        print (user)

l.unbind()
