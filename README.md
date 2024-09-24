# rotstift-functions
Python Functions App for Rotstift

## Setup
To run Functions App in Codespaces: 
```bash
# Update local.settings.json
pwsh -c "Invoke-RestMethod https://aka.ms/azfunc-openapi/add-codespaces.ps1 | Invoke-Expression"
```


## Test locally (with Github Codespaces)
devcontainer should have all extensions and features, otherwise consider installing function core tools like this:

```bash
# Install Azure Function Core Tools
wget -q https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb

sudo apt-get update
sudo apt-get install azure-functions-core-tools-4

```

```bash
pip install -r requirements.txt
az func start
```