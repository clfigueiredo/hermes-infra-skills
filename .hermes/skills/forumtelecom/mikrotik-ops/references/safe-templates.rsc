# =============================================================================
# safe-templates.rsc — snippets MikroTik validados
# Sempre revisar antes de aplicar.
# =============================================================================

# 1. FIREWALL — Hardening de borda (RouterOS 7)
/ip firewall filter
add chain=input action=accept connection-state=established,related
add chain=input action=drop connection-state=invalid
add chain=input action=accept protocol=icmp
add chain=input action=accept in-interface-list=LAN
add chain=input action=drop comment="DROP all else"

add chain=forward action=fasttrack-connection connection-state=established,related hw-offload=yes
add chain=forward action=accept connection-state=established,related
add chain=forward action=drop connection-state=invalid
add chain=forward action=drop connection-nat-state=!dstnat in-interface-list=WAN

# 2. INTERFACE LISTS
/interface list
add name=WAN
add name=LAN

/interface list member
add interface=ether1 list=WAN
add interface=bridge1 list=LAN

# 3. PCC LOAD BALANCE — duas WANs
/ip firewall mangle
add chain=prerouting in-interface-list=LAN connection-mark=no-mark \
    action=mark-connection new-connection-mark=WAN1_conn \
    per-connection-classifier=both-addresses-and-ports:2/0
add chain=prerouting in-interface-list=LAN connection-mark=no-mark \
    action=mark-connection new-connection-mark=WAN2_conn \
    per-connection-classifier=both-addresses-and-ports:2/1
add chain=prerouting connection-mark=WAN1_conn in-interface-list=LAN \
    action=mark-routing new-routing-mark=to_WAN1
add chain=prerouting connection-mark=WAN2_conn in-interface-list=LAN \
    action=mark-routing new-routing-mark=to_WAN2

/routing table
add fib name=to_WAN1
add fib name=to_WAN2

/ip route
add gateway=<gw_wan1> routing-table=to_WAN1 check-gateway=ping
add gateway=<gw_wan2> routing-table=to_WAN2 check-gateway=ping

# 4. BGP — Peer com upstream (RouterOS 7)
/routing bgp template
add name=upstream-template as=<seu_ASN> router-id=<seu_router_id> \
    address-families=ip output.filter-chain=upstream-out input.filter-chain=upstream-in

/routing bgp connection
add name=upstream-A remote.address=<peer_ip> remote.as=<peer_asn> template=upstream-template

/routing filter rule
add chain=upstream-in rule="if (dst in 10.0.0.0/8) { reject }"
add chain=upstream-in rule="if (dst in 172.16.0.0/12) { reject }"
add chain=upstream-in rule="if (dst in 192.168.0.0/16) { reject }"
add chain=upstream-in rule="if (bgp-as-path ~ \"<seu_ASN>\") { reject }"
add chain=upstream-in rule="accept"

# 5. CGNAT — NAT44 com pool dedicado
/ip pool
add name=cgnat-pool ranges=200.X.X.0/24

/ip firewall nat
add chain=srcnat src-address=100.64.0.0/10 \
    action=src-nat to-address-list=cgnat-pool \
    comment="CGNAT NAT44 outbound"

# 6. ADDRESS-LIST DINÂMICA — Anti brute force SSH
/ip firewall filter
add chain=input protocol=tcp dst-port=22 connection-state=new \
    src-address-list=ssh_blacklist action=drop
add chain=input protocol=tcp dst-port=22 connection-state=new \
    src-address-list=ssh_stage3 action=add-src-to-address-list \
    address-list=ssh_blacklist address-list-timeout=1d
add chain=input protocol=tcp dst-port=22 connection-state=new \
    src-address-list=ssh_stage2 action=add-src-to-address-list \
    address-list=ssh_stage3 address-list-timeout=1m
add chain=input protocol=tcp dst-port=22 connection-state=new \
    src-address-list=ssh_stage1 action=add-src-to-address-list \
    address-list=ssh_stage2 address-list-timeout=1m
add chain=input protocol=tcp dst-port=22 connection-state=new \
    action=add-src-to-address-list address-list=ssh_stage1 \
    address-list-timeout=1m

# 7. SCHEDULER — Backup diário automático
/system scheduler
add name=daily-backup interval=1d start-time=03:00:00 \
    on-event=":do { /export file=auto-backup-\$([:pick [/system clock get date] 0 11]); \
                    /system backup save name=auto-backup } on-error={ :log error \"backup falhou\" }"

# 8. SCRIPT FAILOVER — Watchdog ping
/system script
add name=ping-watchdog source={
    :local target "8.8.8.8"
    :local iface "ether1"
    :local fails 0
    :for i from=1 to=3 do={
        :do { /ping address=$target count=1 interval=1 } on-error={ :set fails ($fails + 1) }
    }
    :if ($fails >= 3) do={
        :log warning "Watchdog: $iface caiu, reiniciando"
        /interface disable $iface
        :delay 2s
        /interface enable $iface
    }
}

/system scheduler
add name=watchdog-runner interval=1m on-event="/system script run ping-watchdog"
