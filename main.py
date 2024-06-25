from configurations.ip_validator import start_resume_ip_validator
from configurations.ip_collector import start_resume_retrieve_asn_details, ip_prefix_to_list
from configurations.tls_filterer import start_resume_tls_filterer

from configurations.tldr_anomaly_detector import resume_tldr_process
import json

# list_of_country = [
#     "Rwanda",
# ]

# for country, asn_details in asn_details_grouped_by_country.items():
#     if country in list_of_country:
#         ip_addresses = []
#         for asn_detail in asn_details:
#             ip_prefixes = asn_detail["inetnums"]
#             netname = asn_detail["netname"]
#             for ip_prefix in ip_prefixes:
#                 ip_addresses.extend(ip_prefix_to_list(ip_prefix, netname))
#         ip_addresses = list({'ip_address': _ip[0], 'netname': _ip[1]} for _ip in set((ip['ip_address'], ip['netname']) for ip in ip_addresses))
#         print(f"Processing {country}, {len(ip_addresses)} IP Addresses")

#         valid_ip_addresses = start_resume_ip_validator(ip_addresses, num_of_threads=512, country_name=country, asn_details=asn_details)
#         tlsv1_3, tlsv1_2, tlsvOld = start_resume_tls_filterer(valid_ip_addresses, num_of_threads=512, country_name=country, asn_details=asn_details)

# asn_details_grouped_by_country = start_resume_retrieve_asn_details()

# list_of_country = [
#     "Tunisia"
# ]

# for country, asn_details in asn_details_grouped_by_country.items():
#     if country in list_of_country:
#         ip_addresses = get_ip_addresses(asn_details=asn_details)
#         print(f"Processing {country}, {len(ip_addresses)} IP Addresses")

#         start_resume_ip_validator(ip_addresses, num_of_threads=512, country_name=country)    


        


# #reading from validate_ip_address the .json file created

# f=open('ValidIPs.json')

# data = json.load(f)
# f.close()

# for ips in ["8.8.8.8","157.240.192.24"]:
#     ipLists= ips
#     validportnum= "443"

#     try:
#         ipversion=tls_version_check(ips,validportnum)  
#         print(ipversion)
        
#         with open(f"ipaddresses_with_{ipversion}.json","a") as jsonfile:
#             json.dump(ips,jsonfile)        
#     except (RuntimeError):  
#         with open("/IPAddress_with_oldertls.json",'w') as jsonfile:
#             json.dump(ips,jsonfile)
#             print ("success 3")


countrylist = ['Algeria']

for country in countrylist:
    with open(f"results/{country}/ip_validator_results.json", 'r') as f:
        filehandle = json.load(f)
        list_ip = filehandle["valid_ip_addresses"]
        ip_address = [list(ip.values())[0] for ip in list_ip]
        f.close()
    
    resume_tldr_process(ip_address=ip_address, num_of_threads=2048, chunk_size=10, countryname=country)

