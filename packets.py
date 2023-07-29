import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


def ip_address(filepath):
    with open(filepath) as file:
        data = json.load(file)
        ip_set = set()
        ip_list = ["ip.src", "ip.host"]
        for e in data:
            try:
                if "ip" not in e["_source"]["layers"]:
                    continue
                ip = e["_source"]["layers"]["ip"]
                for e in ip_list:
                    if e in ip:
                        ip_set.add(ip[e])
            except:
                pass
        ip_list = list(ip_set)
        return ip_list


def mac_address(filepath):
    with open(filepath) as file:
        data = json.load(file)
        mac_set = set()
        mac_list = ["eth.src", "eth.dst"]

        for e in data:
            try:
                if "eth" not in e["_source"]["layers"]:
                    continue
                mac = e["_source"]["layers"]["eth"]
                for e in mac_list:
                    if e in mac:
                        mac_set.add(mac[e])
            except:
                pass
        mac_list = list(mac_set)
        return mac_list


def udp_ports(filepath):
    with open(filepath) as file:
        data = json.load(file)
        udp_set = set()
        udp_list = ["udp.srcport", "udp.dstport"]
        for e in data:
            try:
                if "udp" not in e["_source"]["layers"]:
                    continue
                udp = e["_source"]["layers"]["udp"]
                for e in udp_list:
                    if e in udp:
                        udp_set.add(udp[e])
            except:
                pass
        udp_list = list(udp_set)
        return udp_list


def tcp_ports(filepath):
    with open(filepath) as file:
        data = json.load(file)
        tcp_set = set()
        tcp_list = ["tcp.srcport", "tcp.dstport"]
        try:
            for e in data:
                if "tcp" not in e["_source"]["layers"]:
                    continue
                tcp = e["_source"]["layers"]["tcp"]
                for e in tcp_list:
                    if e in tcp:
                        tcp_set.add(tcp[e])
        except:
            pass
        tcp_list = list(tcp_set)
        return tcp_list


def http(filepath):
    with open(filepath) as file:
        data = json.load(file)
        http_set = set()
        http_list = [
            "http.host",
            "http.request.full_uri",
            "http.request.method",
            "http.user_agent",
        ]
        try:
            for e in data:
                if "http" not in e["_source"]["layers"]:
                    continue
                http = e["_source"]["layers"]["http"]
                for h in http_list:
                    if h in http:
                        http_set.add(http[h])
        except:
            pass
        http_list = list(http_set)
        return http_list


def ssdp(filepath):
    with open(filepath) as file:
        data = json.load(file)
        ssdp_set = set()
        ssdp_list = ["http.location", "http.server", "http.response.code"]
        try:
            for e in data:
                if "ssdp" not in e["_source"]["layers"]:
                    continue
                ssdp = e["_source"]["layers"]["ssdp"]
                for s in ssdp_list:
                    if s in ssdp:
                        ssdp_set.add(ssdp[s])
        except:
            pass
        ssdp_list = list(ssdp_set)
        return ssdp_list


def slsk(filepath):
    with open(filepath) as file:
        data = json.load(file)
        slsk_username = []
        slsk_search_text = []
        try:
            for e in data:
                if "slsk" not in e["_source"]["layers"]:
                    continue
                slsk = e["_source"]["layers"]["slsk"]
                if "slsk.username" not in slsk:
                    continue
                slsk_username.append(slsk["slsk.username"])
                if "slsk.search.text" not in slsk:
                    continue
                slsk_search_text.append(slsk["slsk.search.text"])
        except:
            pass
        return slsk_username, slsk_search_text


def ip_details(filepath):
    def get_ip_details(ip):
        baseURL = "https://api.ip2location.io/"
        apiKey = api_key
        format = "json"
        url = f"{baseURL}?key={apiKey}&ip={ip}&format={format}"
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    with open(filepath) as file:
        data = json.load(file)
        ip_details_set = set()
        ip_details_list = ["ip.src", "ip.dst"]
        try:
            for e in data:
                if "ip" not in e["_source"]["layers"]:
                    continue
                ip = e["_source"]["layers"]["ip"]
                for ip in ip_details_list:
                    if ip in e["_source"]["layers"]["ip"]:
                        ip_details_set.add(e["_source"]["layers"]["ip"][ip])
        except:
            pass
        ip_list = list(ip_details_set)
        ip_details = []
        for ip in ip_list:
            details = get_ip_details(ip)
            if details is not None:
                ip_details.append(details)
        return ip_details


def get_packets(filepath):
    ip = ip_address(filepath)
    mac = mac_address(filepath)
    udp = udp_ports(filepath)
    tcp = tcp_ports(filepath)
    http_requests = http(filepath)
    ssdp_requests = ssdp(filepath)
    slsk_username, slsk_search_text = slsk(filepath)
    iplocation = ip_details(filepath)

    results = {
        "ip": ip,
        "mac": mac,
        "udp": udp,
        "tcp": tcp,
        "http_requests": http_requests,
        "ssdp_requests": ssdp_requests,
        "slsk_username": slsk_username,
        "slsk_search_text": slsk_search_text,
        "iplocation": iplocation,
    }
    return results
