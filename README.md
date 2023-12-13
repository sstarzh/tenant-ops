# Tenant cloning script for ZTEdge platform
Script is used to quickly mass-clone or remove tenants programmatically. Can be run from any ENV that has python installed

## Usage

### Pre-requisites:

```
git clone https://github.com/sstarzh/tenant-ops.git
cd tenant-ops
pip3 install -r requirements.txt
```

### To clone tenants:

```
python3 lab_tenant.py clone <MSSP name> <MSSP API Key> <Clone from tenantId> <number of demo tenants to create> <Admin username> <Admin password> <class#>
```
Example:

```
python3 lab_tenant.py clone demoMSSP 0000-0000-0000-0000 1111-1111-1111-1111 10 testadmin supersecretpw 1
```
### To delete all tenants named "selabXYZ":

```
python3 lab_tenant.py delete <MSSP name> <MSSP API Key> <class#>
```

Example:

```
python3 lab_tenant.py delete demoMSSP 0000-0000-0000-0000 1111-1111-1111-1111 1
```

