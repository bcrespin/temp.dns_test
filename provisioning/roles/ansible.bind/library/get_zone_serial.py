#!/usr/bin/python
# mostly inspired from : https://github.com/mcsrainbow/ansible-playbooks-bind9/blob/master/library/heylinux/myfacts

import json
import commands
import re
import os
import os.path
import re

def get_ansible_dns_file_zone_serial_number(zonefile):
    #print json.dumps(zonefile)
    if os.path.isfile( zonefile ):
      serial_number = -1
      with open(zonefile,'r') as f:
        for line in f:
          line=line.rstrip()
          x = re.findall('(\d+) ; serial', line)
          if len(x) > 0 :
            serial_number = x[0]
            break
      ansible_serial_number = int(serial_number)
    else:
      ansible_serial_number = 0

    return ansible_serial_number

def main():
    global module
    module = AnsibleModule(
        argument_spec = dict(
            get_facts=dict(default="yes", required=False),
            file_zone=dict(required=True),
        ),
        supports_check_mode = True,
    )

    ansible_facts_dict = {
        "changed" : False,
        "ansible_facts": {
                "ansible_dns_file_zone_serial_number": {}
            }
    }

    if module.params['get_facts'] == 'yes':
        if module.params['file_zone']:
           zonefile_list =  module.params['file_zone'].split(",")
           for zonefile in zonefile_list:
             zonefile = zonefile.replace("[" , "")
             zonefile = zonefile.replace("]" , "")
             zonefile = zonefile.replace("'", "")
             zonefile = zonefile.strip()
             ansible_dns_file_zone_serial_number = get_ansible_dns_file_zone_serial_number( zonefile)
             ansible_facts_dict['ansible_facts']['ansible_dns_file_zone_serial_number'][zonefile] = ansible_dns_file_zone_serial_number

    print json.dumps(ansible_facts_dict)

from ansible.module_utils.basic import *
main()
