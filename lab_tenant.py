import requests
import json
import uuid, sys, time

base_url = "https://cloud-demo-ztadmin.ericomcloud.net/api/v1/"
def get_jwt(tenant, key):
    url = base_url + "auth"

    payload = json.dumps({
      "mssp": tenant,
      "key": key
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
 
    jwt = response.json()['JWT']
    cookie = response.cookies['route']
    return jwt, cookie

def logout(jwt):
    url = base_url + "auth"
    headers = {
      'Content-Type': 'application/json',
      'Authorization': (f'Bearer {jwt}')
    }

    response = requests.request("DELETE", url, headers=headers)
    return response

def get_tenants(jwt,cookie):
    url = base_url + "mssp/tenants"
    payload = {}
    headers = {
      'Authorization': 'Bearer {0}'.format(str(jwt)),
      'Cookie': 'route={0}'.format(str(cookie))
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response

def delete_tenant(tenant_id,jwt,cookie):
    url = base_url + "tenants/{tenant_id}".format(tenant_id=str(tenant_id))
    payload = {}
    headers = {
      'Authorization': 'Bearer {0}'.format(str(jwt)),
      'Cookie': 'route={0}'.format(str(cookie))
    }
    response = requests.request("DELETE", url, headers=headers, data=payload)
    return response

def add_license(jwt,cookie,tenant_id):
    url = base_url + "license/{tenant_id}".format(tenant_id=str(tenant_id))
    payload = json.dumps({
        "type": "Named Users (Full)",
        "expiration": "2024-12-31",
        "number": 20
      }
      )
    headers = {
      'Content-Type': 'application/json',
      'Authorization': (f'Bearer {jwt}'),
      'Cookie': 'route={0}'.format(str(cookie))
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    return response

def clone_tenant(rand_id,auth_tenant,orig_tenant,tenant_id,jwt,cookie):
    url = base_url + "tenants/clone"

    payload = json.dumps({
      "name": "summit" + str(classNum)+ "group" + str(rand_id),
      "id": str(tenant_id),
      "active": True,
      "partner": auth_tenant,
      "comment": "SE tenant - " + str(rand_id),
      "builtinIdPUsername": admin_user,
      "builtinIdPPassword": admin_pw,
      "clone": {
        "from": str(orig_tenant),
        "cloneAuthentication": True,
        "cloneSettings": True,
        "cloneProfilesPoliciesAndApps": True,
        "cloneZTNA": True
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': (f'Bearer {jwt}'),
      'Cookie': 'route={0}'.format(str(cookie))
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response

def usage():
    print("Usage: python3 lab_tenant.py <operation: clone|delete> <MSSP name> <MSSP API Key> <class #>")
    print("If cloning tenants additional required params are: <Clone from tenantId> <number of demo tenants to create> <Admin username> <Admin password> <class #>")

if __name__ == "__main__":
    
    try:
        op = sys.argv[1]
    except:
        print("Operation is missing")
        usage()
        exit(1)
    try:
        auth_tenant = sys.argv[2]
    except:
        print("MSSP name missing")
        usage()
        exit(1)
    try:
        key = sys.argv[3]
    except:
        print("API Key missing")
        usage()
        exit(1)
    try:
        classNum = sys.argv[4]
    except:
        print("Class # is missing")
        usage()
        exit(1)
    
    if op == "clone":
        try:
            orig_tenant = sys.argv[4]
        except:
            print("Clone from tenantId missing")
            usage()
            exit(1)
        try:
            number_tenants = sys.argv[5]
        except:
            print("Number of demo tenants to create is missing")
            usage()
            exit(1)
        try:
            admin_user = sys.argv[6]
        except:
            print("Admin username is missing")
            usage()
            exit(1)
        try:
            admin_pw = sys.argv[7]
        except:
            print("Admin password is missing")
            usage()
            exit(1)
        try:
            classNum = sys.argv[8]
        except:
            print("Class # is missing")
            usage()
            exit(1)
    jwt, cookie = get_jwt(auth_tenant, key)

    if (( op != "clone") & ( op != "delete")):
        print("Unknown operation")
        exit(1)
    if op == "delete":
        print("Deleting demo tenants")
        tenants = get_tenants(jwt,cookie)
 
        for tenant in tenants.json():
            if tenant["name"].startswith("summit" + str(classNum)+ "group"):
                print("Deleting tenant: " + tenant["name"])
                resp = delete_tenant(tenant["id"],jwt,cookie)
                if resp.status_code!= 204:
                    print("Error deleting tenant " + str(tenant["name"]))
                    print("Response:" + str(resp.status_code))
                    print("Response:" + str(resp.text))
                    exit(1)
                print("Done")
                time.sleep(3)
        print("Finished deleting demo tenants")
        exit(0)

    if op == "clone":
        print("Cloning demo tenants")
        for demo_n in range (1,int(number_tenants)+1):
            tenant_id = uuid.uuid4()
            resp = clone_tenant(demo_n,auth_tenant,orig_tenant,tenant_id,jwt,cookie)
            if resp.status_code!= 204:
                print("Error cloning tenant " + str(demo_n))
                print("Response:" + str(resp.status_code))
                print("Response:" + str(resp.text))
                exit(1)
            add_license(jwt,cookie,tenant_id)
            print("Cloned tenant: " + str(demo_n) + " Tenant ID: " + str(tenant_id))
            time.sleep(6)
        print("Finished cloning demo tenants")
    logout(jwt)

