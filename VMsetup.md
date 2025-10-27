sudo apt update && sudo apt upgrade -y

sudo apt install -y snapd openvpn
sudo apt install -y net-tools curl wget git unzip jq python3-pip dnsutils traceroute 
sudo apt install -y nmap htop tmux tree

# PowerShell
sudo snap install powershell --classic
pwsh

# Docker
sudo apt install docker.io -y
sudo systemctl enable docker --now
sudo apt install docker-compose -y

# Azure
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# AzureHound
## Deploy with Docker
https://bloodhound.specterops.io/collect-data/ce-collection/azurehound
curl -L https://ghst.ly/getbhce -o bloodhound.yml
sudo docker-compose -f bloodhound.yml up -d

## Get initial password
docker logs $(docker ps --filter "name=bloodhound" -q) 2>&1 | grep "Initial Password Set To:"
### with sudo if permission denied
sudo sh -c 'docker logs $(docker ps --filter "name=bloodhound" -q) 2>&1 | grep "Initial Password Set To:"'

## Access BloodHound UI
### port forwarding configuration
Local Port: 8080 
Bind Address: 127.0.0.1 
Intermediate Host: Linux VM 
Destination Address: localhost 
Destination Port: 8080
ssh -f -N -L 127.0.0.1:8080:localhost:8080 user@VM_IP -i path/to/private/key 

### Access URL
http://localhost:8080/ui/login
user: admin

Download AzureHound collector
sudo curl -L login.microsoftonline.com/megabigtech.com/.well-known/openid-configuration | jq

# Get Device Code for AzureHound
$body = @{
    "client_id" =     "1950a258-227b-4e31-a9cf-717495945fc2"
    "resource" =      "https://graph.microsoft.com"
}
$UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
$Headers=@{}
$Headers["User-Agent"] = $UserAgent
$authResponse = Invoke-RestMethod `
    -UseBasicParsing `
    -Method Post `
    -Uri "https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0" `
    -Headers $Headers `
    -Body $body
$authResponse

## Enter code on https://microsoft.com/devicelogin
## return to terminal 

$body=@{
   "client_id" =  "1950a258-227b-4e31-a9cf-717495945fc2"
   "grant_type" = "urn:ietf:params:oauth:grant-type:device_code"
   "code" =       $authResponse.device_code
}
$Tokens = Invoke-RestMethod `
   -UseBasicParsing `
   -Method Post `
   -Uri "https://login.microsoftonline.com/Common/oauth2/token?api-version=1.0" `
   -Headers $Headers `
   -Body $body
$Tokens

## Unpack AzureHound ZIP File
unzip azurehound.zip
cd AzureHound_v2.7.1_linux_amd64

./azurehound -r $Tokens.refresh_token list --tenant "2590ccef-687d-493b-ae8d-441cbab63a72" -o output.json

# AWS

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# GCP
sudo snap install google-cloud-cli --classic
echo 'export PATH="$PATH:/snap/bin"' >> ~/.bashrc
source ~/.bashrc

# VPN Connection
mv "name2.ovpn" name.ovpn

## as a background service
sudo openvpn --config name.ovpn --daemon
