#skeleton for edit_config rpc requests


from ncclient import manager
# import logging

# logging.basicConfig(level=logging.DEBUG)

router = {
    "host": "**",
    "port": "830",
    "username": "admin",
    "password": "***"
}

config_payload = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
  <interface>
    <name>GigabitEthernet1/0/23</name>
    <description>PLSWORK</description>
  </interface>
</interfaces>
</config>
"""

with manager.connect(**router, hostkey_verify=False) as m:
    response = m.edit_config(
        target="running",
        config=config_payload
    )
    
    print(response.xml)
