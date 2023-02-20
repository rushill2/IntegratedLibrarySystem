import paramiko, socket
hostname = socket.gethostname()
myip = socket.gethostbyname(hostname)
ip='103.90.163.100'
import urllib.request

external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

print(external_ip)
port=22
username='root'
password='Thehighground@773'

cmd='some useful command'

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,port,username,password)

stdin,stdout,stderr=ssh.exec_command('ls -l')
outlines=stdout.readlines()
resp=''.join(outlines)
ufwallow = 'sudo ufw allow from ' + str(external_ip)
stdin,stdout,stderr=ssh.exec_command(ufwallow)
outlines=stdout.readlines()
resp=''.join(outlines)
print(resp)