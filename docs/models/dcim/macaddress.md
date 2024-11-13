# MAC Addresses

A MAC address object in NetBox comprises a single physical (hardware) address, and represents a MAC address as reported by or assigned to a network interface. MAC addresses can be assigned to [device](../dcim/device.md) and [virtual machine](../virtualization/virtualmachine.md) interfaces. A MAC address can be specified as the "primary" MAC address for a given interface or VM interface.

Most interfaces only have a single MAC address, hard-coded at the factory. However, on some devices (particularly virtual interfaces) it is possible to assign additional MAC addresses or change existing ones. For this reason NetBox allows multiple MACAddress objects to be assigned to a single interface. However, for convenience and backward compatibiility reasons, the value of the `mac_address` field of the primary (or single) MAC address on an interface is reflected as a simple property in the interface detail page.

## Fields

### MAC Address

The 48-bit MAC address, in colon-hexadecimal notation (e.g. `aa:bb:cc:11:22:33`).
