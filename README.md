# Enum_Sub

🕵️‍♂️ SubEnum - Subdomain Enumeration Script

Ferramenta simples e poderosa para enumeração inicial de subdomínios, ideal para quem quer agilidade na fase de reconhecimento durante um Pentest ou Bug Bounty.<br>
🚀 Por que usar?

O SubEnum automatiza a coleta de subdomínios utilizando várias fontes e ferramentas conhecidas, gerando uma lista consolidada para validação posterior com httpx. Tudo isso com mínima interação e focado em produtividade.

Enquanto ele roda, você pode aproveitar o tempo para analisar outros vetores, preparar payloads ou tomar um café ☕. Ao final, é só validar os resultados e usar a lista com ferramentas como nmap, nuclei, nikto, entre outras.

<b>🔧 Ferramentas utilizadas</b>

amass<br>
subcat<br>
shodanx<br>
crt.sh<br>
web.archive.org<br>
AlienVault OTX<br>
gobuster<br>
httpx<br>

<b>📂 Requisitos<br></b>
Python 3

<b>Ferramentas instaladas:<br></b>
httpx<br>
subcat<br>
jq<br>
curl<br>

<b>Ver comandos:<br></b>
python enum_sub.py -h
```bash
python enum_sub.py -d domain.com -w /path-to-wordlist
```
Caso não tenha uma Wordlist, não use "-w", será usada a padrão deste repositório.

<b>A Ferramenta executará:<br></b>
Coleta passiva e ativa de subdomínios<br>
Remoção de duplicados<br>
Detecção automática de Wildcard DNS<br>
Validação com httpx nas principais portas web<br>

Ao final, você terá um arquivo com os subdomínios ativos em:<br>
httpx_domain_com.txt

🎯 Foco
Essa ferramenta não substitui uma enumeração completa, mas é excelente para ganhar tempo na fase inicial. Ao automatizar tarefas básicas e trazer resultados de múltiplas fontes, permite ao analista focar em outras etapas enquanto ela faz o "trabalho sujo".

