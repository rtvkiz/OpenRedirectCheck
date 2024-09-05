import requests
import re

## Potential missing scenatio
## Where the url gets redirected to one of its url and then to the payload
## This code might miss it
## We can follow recusrive chain for that

pattern = re.compile(r'(?m)^(?:Location\s*?:\s*?)(?:https?:\/\/|\/\/|\/\\\\|\/\\)?(?:[a-zA-Z0-9\-_\.@]*)evil\.com\/?(\/|[^.].*)?$')

# check if the response status is 301,302,307, and location header belongs to the payload
def check(url):
    try:
        resp=requests.get(url,allow_redirects=False)
        location_header_value = resp.headers.get('Location','')
        location_header=f"Location: {location_header_value}"
        # print(location_header)
        if pattern.match(location_header) and resp.status_code in [301,302,308,307]:
            return True
        
    except requests.RequestException as e:
         print(e)


        # print(url)
def check_redirect(url):
    try:
        resp=requests.get(url,allow_redirects=True)
        # print(resp.history)
        if not resp.history:
            return 
        for r in resp.history:
            # print(r)
            location_header_value = r.headers.get('Location','')
            location_header=f"Location: {location_header_value}"
            if pattern.match(location_header) and r.status_code in [301,302,308,307]:
                return True
    except requests.RequestException as e:
        print(e)
        
    
def main():
    url=input()
    with open('payload.txt') as f:
        lines=f.readlines()
    # print(lines)
    payloads=[]
    vulnerable_endpoints=[]
    for end in lines:
        o_url = url + '/' + end.strip()
        if check_redirect(o_url):
            vulnerable_endpoints.append(o_url)
    print(vulnerable_endpoints)

if __name__=='__main__':
    main()