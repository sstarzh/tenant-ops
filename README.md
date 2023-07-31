# Tenant cloning script for ZTEdge platform
Script is used to quickly mass-clone or remove tenants programmatically. Can be run from any ENV that has python installed

## Usage

### Pre-requisites:

```
git clone
pip3 install -r requirements.txt
```

# To clone tenants:

```
python3 lab_tenant.py clone <MSSP name> <MSSP API Key> <Clone from tenantId> <number of demo tenants to create> <Admin username> <Admin password>
```
Example:

```
python3 lab_tenant.py clone demoMSSP 0000-0000-0000-0000 1111-1111-1111-1111 10 testadmin supersecretpw
```
# To delete all tenants named "selabXYZ":

```
python3 lab_tenant.py delete <MSSP name> <MSSP API Key>
```

Example:

```
python3 lab_tenant.py delete demoMSSP 0000-0000-0000-0000 1111-1111-1111-1111
```

