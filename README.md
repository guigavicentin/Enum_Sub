# Enum_Sub

🕵️‍♂️ SubEnum - Subdomain Enumeration Script

Ferramenta simples e poderosa para enumeração inicial de subdomínios, ideal para quem quer agilidade na fase de reconhecimento durante um Pentest ou Bug Bounty.

🚀 Por que usar?

O SubEnum automatiza a coleta de subdomínios utilizando várias fontes e ferramentas conhecidas, gerando uma lista consolidada para validação posterior com httpx. Tudo isso com mínima interação e focado em produtividade.

Enquanto ele roda, você pode aproveitar o tempo para analisar outros vetores, preparar payloads ou tomar um café ☕. Ao final, é só validar os resultados e usar a lista com ferramentas como nmap, nuclei, nikto, entre outras.

🔧 Ferramentas utilizadas

amass

subcat

shodanx

crt.sh

web.archive.org

AlienVault OTX

gobuster

httpx

📂 Requisitos

Python 3

Ferramentas instaladas:

amass

httpx

subcat

shodanx

gobuster

jq

curl

Você também precisa da wordlist de subdomínios:

/caminho/diretorio/SecLists/Discovery/DNS/subdomains-top1million-110000.txt

Também ajustar os caminhos das ferramentas, olhe o .py antes de usar.

python3 enum_sub.py

Você será solicitado a inserir o domínio (ex: target.com), e a ferramenta fará todo o trabalho:

Coleta passiva e ativa de subdomínios

Remoção de duplicados

Detecção automática de Wildcard DNS

Validação com httpx nas principais portas web

Ao final, você terá um arquivo com os subdomínios ativos em:

httpx_target_com.txt

📈 Próximos passos com os resultados 

- Podendo escolher em qual .txt quer usar, cada ferramenta salva em um arquivo - Depois junto tudo em um .txt só - E no "httpx_target_com.txt" para o resultado do httpx

Use o arquivo final como base para outras análises, como:

nmap -iL httpx_target_com.txt -Pn -sV -T4 -oA nmap_scan ---- Talvez colocar um "-p-" também...

nuclei -l httpx_target_com.txt -rl 10 -bs 2 -c 2 -as -silent -s critical,high,medium
Combinando com TAGS talvez --- -tags tech,tech-detect (entre outras)

nikto -h httpx_target_com.txt --output nikto_results.txt

🎯 Foco

Essa ferramenta não substitui uma enumeração completa, mas é excelente para ganhar tempo na fase inicial. Ao automatizar tarefas básicas e trazer resultados de múltiplas fontes, permite ao analista focar em outras etapas enquanto ela faz o "trabalho sujo".

⚠️ Aviso

Use com responsabilidade.

Ferramenta desenvolvida para fins educacionais e profissionais com autorização.
