import os
import platform
import subprocess
import sys

def install_linux():
    print("[*] Sistema detectado: Linux")

    subprocess.run("pip install argparse", shell=True)

    print("[*] Atualizando pacotes e instalando dependências...")
    subprocess.run("sudo apt update && sudo apt install curl jq gobuster amass snapd -y", shell=True)

    print("[*] Instalando Go...")
    result = subprocess.run("sudo snap install go --classic", shell=True)
    if result.returncode != 0:
        print("[!] Snap falhou, tentando via apt...")
        subprocess.run("sudo apt install golang -y", shell=True)

    print("[*] Instalando shodanx...")
    subprocess.run("go install github.com/clevcode/shodanx@latest", shell=True)

    print("[*] Adicionando Go ao PATH temporariamente...")
    gopath = os.path.expanduser("~/go/bin")
    os.environ["PATH"] += f":{gopath}"

    print("[*] Instalando httpx via Go...")
    subprocess.run("go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest", shell=True)

    print(f"\n[*] Se httpx não for reconhecido, adicione isso ao seu ~/.bashrc ou ~/.zshrc:")
    print(f'export PATH="$PATH:{gopath}"')

def main():
    if platform.system().lower() != "linux":
        print("[!] Esse script é só pra Linux no momento")
        sys.exit(1)

    install_linux()
    print("\n✅ Instalação concluída! Fecha e abre o terminal ou dá um 'source ~/.bashrc' pra garantir.")

if __name__ == "__main__":
    main()
