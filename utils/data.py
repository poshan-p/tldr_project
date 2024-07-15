import os
import json


def format_results(directory):
    csv = 'Country, 1111, 0000, 0001 TO 1110, IPv4-Good-%, IPv4-Bad-%\n'
    for filename in os.listdir(directory):
        servers = 0
        tlsv1_2 = 0
        misconfigured_tlsv1_2 = 0
        tlsv1_3 = 0
        misconfigured_tlsv1_3 = 0
        if filename.endswith('.json'):
            continue
        if os.path.exists(directory + filename + '/tldr_process_v1.2_results.json') and os.path.exists(directory + filename + '/tldr_process_v1.3_results.json'):
            with open(directory + filename + '/tldr_process_v1.2_results.json') as f:
                data = json.load(f)
                tlsv1_2 = data['total_ip_checked']
                properly_configure_tlsv1_2 = len(data['encoded_ip_addresses']['1111'])
                not_running_tlsv1_2 = len(data['encoded_ip_addresses']['0000'])
                
            with open(directory + filename + '/tldr_process_v1.3_results.json') as f:
                data = json.load(f)
                tlsv1_3 = data['total_ip_checked']
                properly_configure_tlsv1_3 = len(data['encoded_ip_addresses']['1111'])
                not_running_tlsv1_3 = len(data['encoded_ip_addresses']['0000'])
        
            servers = tlsv1_2 + tlsv1_3
            
            misconfigured_tlsv1_2 = tlsv1_2 - properly_configure_tlsv1_2 - not_running_tlsv1_2
            misconfigured_tlsv1_3 = tlsv1_3 - properly_configure_tlsv1_3 - not_running_tlsv1_3
            properly_configured_servers = properly_configure_tlsv1_2 + properly_configure_tlsv1_3
            not_running = not_running_tlsv1_2 + not_running_tlsv1_3
            misconfigured_servers = misconfigured_tlsv1_2 + misconfigured_tlsv1_3
            csv += f'{filename}, {properly_configured_servers}, {not_running}, {misconfigured_servers}, {round((properly_configured_servers)/servers*100, 2)}, {round((misconfigured_servers)/servers*100, 2)}\n'
            
        else:
            print(filename)
    
    with open(directory + 'formatted_results.csv', 'w') as f:
        f.write(csv)
        
format_results('results/')