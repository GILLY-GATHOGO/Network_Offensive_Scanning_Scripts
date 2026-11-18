from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity

def snmp_get(target, community, oid):
    """
    Perform an SNMP GET request.

    :param target: IP address of the SNMP agent (e.g., "196.207.24.206")
    :param community: SNMP community string (e.g., "public")
    :param oid: The OID to query (e.g., "1.3.6.1.2.1.1.1.0" for sysDescr)
    :return: The response from the SNMP agent.
    """
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=0),  # For SNMPv1; use mpModel=1 for SNMPv2c
            UdpTransportTarget((target, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
    )

    if errorIndication:
        print("Error:", errorIndication)
    elif errorStatus:
        print("Error:", errorStatus.prettyPrint())
    else:
        for varBind in varBinds:
            return f'{varBind[0]} = {varBind[1]}'

if __name__ == '__main__':
    target_ip = "197.254.107.166"  # Replace with your target's IP address
    community_string = "public"   # Replace with your SNMP community string
    oid_to_query = "1.3.6.1.2.1.1.1.0"  # sysDescr OID

    result = snmp_get(target_ip, community_string, oid_to_query)
    if result:
        print("SNMP GET Response:", result)
    else:
        print("No response received.")
