import subprocess
import os
import random

def print_banner():
    banners = [
        print("""
@@@@@%+..........................................................................+%@@@@@@
@@@@#-...............................:-=+*##*+==:.................................-#@@@@@
@@%=................................+@@@@@@@@@@@@#..................................+%@@@
@#:................................-%@@@@@@@@@@@@@=..................................-#@@
*..................................%@@@@@@@@@@@@@@%....................................#@
..................................=%@@@@@@@@@@@@@@@+....................................#
..........................:-==+**+=---=+*#%%#*+=---=+**+==--.............................
...........................:=*#%@@@@@%%#*+=-+*#%@@@@@@@%*=-..............................
................................-+%@@@@@@@@@@@@@@@@%+-:..................................
..................................:%@@@@@@@@@@@@@@@-.....................................
...................................=@@@@@@@@@@@@@@*......................................
....................................*@@@@@@@@@@@@%.......................................
:-=++=-..............................+%@@@@@@@@%+:...............................-=++=-:.
@@@@@@@%*-.............................-+%@@%*-...............................-*%@@@@@@@#
.......=@@*...............................==................................:#@@@:....%@@
..@@@..=@@@+........................:-...-@@*...--:.........................*@@@@*+:..%@@
..@@@..=@@@#..................:-+*%@@@*...*%...+@@@%#+=-....................%@@@@@@-..%@@
..@@@..=@@@*..............=*#%@@@@@@@@@=..+%..:%@@@@@@@@@%#*=:..............*@@@@@@-..%@@
.......=@@#..............*@@@@@@@@@@@@@%:.#@-.%@@@@@@@@@@@@@@%:.............:%@@@@@-..%@@
%%%%%%%%#=..............*@@@@@@@@@@@@@@@#:%@+#@@@@@@@@@@@@@@@@%:..............=#@@@%%%@@%
-=+**+=:...............=@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@*................:=+**+=-.
....:-................:%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+.................-......
.+-.:%+..............:%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=..............=%+.:+:..
.#@%#%@%-............#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-...........:#@@#%@@:..
.+%@@@@@@#+=-:......*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.......-=+*%@@@@@%*...
...:=#%@@@@@@@@%#*+*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+*##%@@@@@@@@%+-.....
.......=@@@@@@@@@@@@@@@@@@@##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@*:........
.......-@@@@@@@@@@@@@@@@@%+.-@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.=%@@@@@@@@@@@@@@@@@+.........
........:-+*#%@@@@@@@@@@%-...%@@@@@@@@@@@@@@@@@@@@@@@@@@@@%..:*@@@@@@@@@@%%*+=-.........:
..............:-=+*#%%@+.....#@@@@@@@@@@@@@@@@@@@@@@@@@@@@*....=%@%#*+=-:..............:%
%-....................:......+%%%%%%%%%%%%%%%%%%%%%%%%%%%%=...........................-%@
@%+..................................................................................*%@@
"""),
    ]
    print(random.choice(banners))
    print()

def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar: {cmd}\n{e}")

def main():
    print_banner()
    domain = input("Digite o domínio (ex: target.com): ").strip()
    base = domain.replace('.', '_')
    wordlist = "/caminho/diretorio/aqui/SecLists-master/Discovery/DNS/subdomains-top1million-110000.txt"

    # Subdomain enum
    print("\n[+] Executando ferramentas de enumeração...")

    run_command(f"shodanx subdomain -d {domain} -o {base}_shodanx.txt")
    run_command(f"python3 /caminho/diretorio/aqui/subcat/subcat.py -d {domain} -o {base}_subcat.txt")
    run_command(f"amass enum -active -norecursive -noalts -d {domain} -o {base}_amass.txt")

    run_command(f'curl -s "https://otx.alienvault.com/api/v1/indicators/hostname/{domain}/passive_dns" '
                f'| jq -r \'.passive_dns[]?.hostname\' '
                f'| grep -E "[a-zA-Z0-9.-]+\\.{domain}$" | sort -u | tee {base}_alienvault.txt')

    run_command(f'curl -s "http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&collapse=urlkey" '
                f'| jq -r \'.[1:][] | .[2]\' '
                f'| grep -Eo "([a-zA-Z0-9._-]+\\.)?{domain}" | sort -u | tee {base}_webarchive.txt')

    run_command(f'curl -s "https://crt.sh/?q=%.{domain}&output=json" '
                f'| jq -r \'.[].name_value\' | sed \'s/\\*\\.//g\' | sort -u | tee {base}_crtsh.txt')

    # Gobuster - verificar se precisa do --wildcard
    print("\n[+] Verificando wildcard DNS no Gobuster...")
    wildcard_test = subprocess.run(
        f"gobuster dns -d {domain} -w {wordlist} -q -t 5 -n -z 2>&1 | grep 'returned the same IP'",
        shell=True,
        stdout=subprocess.PIPE
    )

    use_wildcard = wildcard_test.returncode == 0

    print(f"[i] Wildcard DNS {'detectado' if use_wildcard else 'não detectado'}.")

    gobuster_cmd = f"gobuster dns -d {domain} -w {wordlist}"
    if use_wildcard:
      gobuster_cmd += " --wildcard"
    gobuster_cmd += f" 2>/dev/null | sed 's/^Found: //' > {base}_gobuster.txt"
    run_command(gobuster_cmd)

    # Combinar resultados
    print("\n[+] Unificando e limpando subdomínios encontrados...")
    files = [f for f in os.listdir('.') if f.startswith(base) and f.endswith('.txt') and not f.startswith("httpx_")]
    with open(f"{base}_todos_subs.txt", "w") as outfile:
        seen = set()
        for fname in files:
            with open(fname) as infile:
                for line in infile:
                    sub = line.strip()
                    if sub and sub not in seen:
                        seen.add(sub)
                        outfile.write(sub + "\n")

    # Validar com httpx
    print("\n[+] Rodando httpx para validar subdomínios...")
    httpx_out = f"httpx_{base}.txt"
    ports = "80,81,3000,3001,8443,10000,9000,9443,443,8080,8000,6885,4443,2075,2076,6443,3868,3366,9091,5900,8081,6000,8181,3306,5000,4000,5432,15672,9999,161,4044,7077"
    run_command(f"httpx -l {base}_todos_subs.txt -ports {ports} -threads 80 -title -sc -ip -o {httpx_out}")

    print(f"\n[✔] Subdomínios ativos salvos em: {httpx_out}")

if __name__ == "__main__":
    main()
