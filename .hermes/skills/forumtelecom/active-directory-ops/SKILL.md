---
name: active-directory-ops
description: "Senior Microsoft Active Directory and Windows File Server engineer. Use when the user asks to automate or troubleshoot AD DS tasks: create users, OUs, groups, group membership, password reset, account enable/disable, home folders, SMB shares, NTFS permissions, GPO-linked onboarding, audit/export, and safe PowerShell automation."
version: 1.0.0
author: Hermes Agent / Forum Telecom
license: MIT
metadata:
  hermes:
    tags: [active-directory, windows-server, powershell, users, groups, file-server, ntfs, smb, gpo]
    related_skills: [hyper-v-ops, vmware-ops, zabbix-ops]
    source_research:
      - https://learn.microsoft.com/en-us/powershell/module/activedirectory/new-aduser
      - https://learn.microsoft.com/en-us/powershell/module/activedirectory/add-adgroupmember
      - https://learn.microsoft.com/en-us/powershell/module/smbshare/new-smbshare
      - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-acl
      - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls
---
# Active Directory / Windows File Server — Operação e Automação

Skill para administrar e automatizar rotinas de Microsoft Active Directory Domain Services e file server Windows com PowerShell, em português brasileiro e com postura segura para ambiente corporativo/ISP/MSP.

## Contrato operacional

Use esta skill para:
- criar usuários, grupos e OUs;
- liberar ou remover acesso a pastas;
- provisionar pasta home ou pasta departamental;
- resetar senha, desbloquear conta e habilitar/desabilitar usuário;
- consultar auditoria básica de usuários/grupos;
- criar scripts PowerShell idempotentes e seguros;
- orientar integração do Hermes com AD usando WinRM/SSH/PowerShell remoto.

Não use esta skill para burlar senha, contornar política de segurança, extrair hashes, fazer ataque, persistência ou movimentação lateral.

## Segurança obrigatória

1. **Leitura primeiro**: antes de alterar AD ou permissões, coletar estado atual com `Get-ADUser`, `Get-ADGroup`, `Get-Acl` e/ou `Get-SmbShare`.
2. **Confirmação para mudança**: criação, exclusão, reset de senha, alteração de grupo e alteração de ACL em produção exigem confirmação clara do escopo.
3. **Nunca expor segredo**: não publicar senha, token, usuário privilegiado, dump completo de AD, SID sensível ou lista completa de funcionários no grupo.
4. **Menor privilégio**: criar usuário de automação com permissões delegadas só nas OUs e shares necessárias.
5. **Evitar Domain Admin**: usar Domain Admin apenas para setup inicial/delegação; operação diária deve ser delegada.
6. **Testar com `-WhatIf` quando disponível**: principalmente remoção, movimentação e alteração em massa.
7. **Logar o que mudou**: registrar usuário alvo, grupo/share alterado, horário e operador, sem registrar senha.

## Pré-requisitos no servidor/estação administrativa

Executar em Windows Server, RSAT ou host com módulo ActiveDirectory:

```powershell
# Windows Server
Install-WindowsFeature RSAT-AD-PowerShell

# Windows 10/11 com RSAT já habilitado via Optional Features
Get-Module -ListAvailable ActiveDirectory
Import-Module ActiveDirectory

# Validar domínio
Get-ADDomain
Get-ADForest
```

Para file server:

```powershell
Import-Module SmbShare
Get-Command New-SmbShare, Grant-SmbShareAccess, Revoke-SmbShareAccess
```

## Variáveis de ambiente recomendadas para Hermes

Não colar credenciais no chat. Usar `.env`, cofre local ou secret manager.

```bash
AD_DOMAIN="empresa.local"
AD_DC="dc01.empresa.local"
AD_BASE_DN="DC=empresa,DC=local"
AD_USERS_OU="OU=Usuarios,DC=empresa,DC=local"
AD_GROUPS_OU="OU=Grupos,DC=empresa,DC=local"
AD_FILESERVER="fs01.empresa.local"
AD_AUTOMATION_USER="EMPRESA\\svc-hermes-ad"
# senha/chave deve ficar em cofre, não no grupo
```

Se usar WinRM a partir do Linux/Hermes:

```bash
# Exemplo de ferramentas possíveis; escolha conforme ambiente
python3 -m venv ~/.venvs/ad-ops
source ~/.venvs/ad-ops/bin/activate
pip install pypsrp pywinrm
```

## Descoberta segura antes de agir

```powershell
# Quem sou e onde estou
whoami
$env:USERDNSDOMAIN
Get-ADDomain | Select DNSRoot, NetBIOSName, PDCEmulator

# Verificar usuário
Get-ADUser -Identity j.silva -Properties DisplayName,Enabled,LockedOut,PasswordLastSet,MemberOf |
  Select SamAccountName,DisplayName,Enabled,LockedOut,PasswordLastSet

# Ver grupos do usuário
Get-ADPrincipalGroupMembership j.silva | Select Name,GroupCategory,GroupScope

# Ver grupo e membros
Get-ADGroup -Identity "TI-Compartilhado-RW" -Properties Description
Get-ADGroupMember "TI-Compartilhado-RW" | Select Name,SamAccountName,ObjectClass

# Ver ACL de pasta
Get-Acl "D:\Dados\TI" | Select -ExpandProperty Access |
  Select IdentityReference,FileSystemRights,AccessControlType,IsInherited

# Ver share SMB
Get-SmbShare -Name "TI$" | Select Name,Path,Description
Get-SmbShareAccess -Name "TI$"
```

## Criar usuário com padrão seguro

Preferir criar desabilitado, inserir grupos, criar pasta, depois habilitar.

```powershell
Import-Module ActiveDirectory

$User = "j.silva"
$Name = "João Silva"
$GivenName = "João"
$Surname = "Silva"
$UPN = "$User@empresa.local"
$OU = "OU=Usuarios,DC=empresa,DC=local"
$TempPassword = Read-Host "Senha temporária" -AsSecureString

New-ADUser `
  -SamAccountName $User `
  -UserPrincipalName $UPN `
  -Name $Name `
  -GivenName $GivenName `
  -Surname $Surname `
  -DisplayName $Name `
  -Path $OU `
  -AccountPassword $TempPassword `
  -ChangePasswordAtLogon $true `
  -Enabled $false

Get-ADUser $User | Select SamAccountName,Enabled,DistinguishedName
```

Adicionar grupos:

```powershell
$Groups = @("GG-Funcionarios", "TI-Compartilhado-RW")
foreach ($g in $Groups) {
  Add-ADGroupMember -Identity $g -Members $User
}

Get-ADPrincipalGroupMembership $User | Select Name
```

Habilitar após validação:

```powershell
Enable-ADAccount -Identity $User
Get-ADUser $User -Properties Enabled | Select SamAccountName,Enabled
```

## Criar usuário em massa via CSV

CSV exemplo (`usuarios.csv`):

```csv
SamAccountName,Nome,Sobrenome,DisplayName,OU,Groups
j.silva,João,Silva,João Silva,"OU=Usuarios,DC=empresa,DC=local","GG-Funcionarios;TI-Compartilhado-RW"
```

Script seguro:

```powershell
Import-Module ActiveDirectory
$Users = Import-Csv .\usuarios.csv

foreach ($u in $Users) {
  $exists = Get-ADUser -Filter "SamAccountName -eq '$($u.SamAccountName)'" -ErrorAction SilentlyContinue
  if ($exists) {
    Write-Warning "Já existe: $($u.SamAccountName)"
    continue
  }

  $pwd = Read-Host "Senha temporária para $($u.SamAccountName)" -AsSecureString
  New-ADUser `
    -SamAccountName $u.SamAccountName `
    -UserPrincipalName "$($u.SamAccountName)@empresa.local" `
    -GivenName $u.Nome `
    -Surname $u.Sobrenome `
    -Name $u.DisplayName `
    -DisplayName $u.DisplayName `
    -Path $u.OU `
    -AccountPassword $pwd `
    -ChangePasswordAtLogon $true `
    -Enabled $false

  foreach ($g in ($u.Groups -split ';')) {
    if ($g.Trim()) { Add-ADGroupMember -Identity $g.Trim() -Members $u.SamAccountName }
  }

  Enable-ADAccount -Identity $u.SamAccountName
  Write-Host "Criado: $($u.SamAccountName)"
}
```

## Resetar senha, desbloquear e desabilitar

```powershell
# Desbloquear
Unlock-ADAccount -Identity j.silva

# Resetar senha sem imprimir segredo
$NewPassword = Read-Host "Nova senha temporária" -AsSecureString
Set-ADAccountPassword -Identity j.silva -Reset -NewPassword $NewPassword
Set-ADUser -Identity j.silva -ChangePasswordAtLogon $true

# Desabilitar no desligamento
Disable-ADAccount -Identity j.silva
Set-ADUser -Identity j.silva -Description "Desligado em $(Get-Date -Format yyyy-MM-dd)"
```

## Liberação de pasta: modelo recomendado

Modelo simples e auditável:

- criar grupo global ou domain local por pasta e nível;
- colocar usuários no grupo;
- aplicar ACL NTFS no grupo, não em usuário individual;
- share SMB com permissão ampla controlada por NTFS ou com grupos equivalentes;
- documentar padrão de nomes.

Exemplo de padrão:

- `DL-FS-TI-R` leitura;
- `DL-FS-TI-RW` alteração;
- `DL-FS-FINANCEIRO-R` leitura;
- `DL-FS-FINANCEIRO-RW` alteração.

Criar grupos:

```powershell
New-ADGroup -Name "DL-FS-TI-R"  -GroupScope DomainLocal -GroupCategory Security -Path "OU=Grupos,DC=empresa,DC=local"
New-ADGroup -Name "DL-FS-TI-RW" -GroupScope DomainLocal -GroupCategory Security -Path "OU=Grupos,DC=empresa,DC=local"
```

Criar pasta e aplicar NTFS com `icacls`:

```powershell
$Path = "D:\Dados\TI"
New-Item -ItemType Directory -Path $Path -Force

# Remover herança copiando permissões atuais; revisar antes em produção
icacls $Path /inheritance:d

# Conceder leitura e alteração aos grupos
icacls $Path /grant "EMPRESA\DL-FS-TI-R:(OI)(CI)(RX)"
icacls $Path /grant "EMPRESA\DL-FS-TI-RW:(OI)(CI)(M)"

# Validar
icacls $Path
```

Criar share:

```powershell
New-SmbShare -Name "TI$" -Path "D:\Dados\TI" -Description "Pasta TI" -FullAccess "EMPRESA\Administradores de Domínio"
Grant-SmbShareAccess -Name "TI$" -AccountName "EMPRESA\DL-FS-TI-R" -AccessRight Read -Force
Grant-SmbShareAccess -Name "TI$" -AccountName "EMPRESA\DL-FS-TI-RW" -AccessRight Change -Force
Get-SmbShareAccess -Name "TI$"
```

Adicionar usuário ao grupo de acesso:

```powershell
Add-ADGroupMember -Identity "DL-FS-TI-RW" -Members "j.silva"
Get-ADPrincipalGroupMembership j.silva | Where-Object Name -like 'DL-FS-*' | Select Name
```

## Pasta home por usuário

```powershell
$User = "j.silva"
$HomeRoot = "D:\Homes"
$HomePath = Join-Path $HomeRoot $User
$ShareName = "$User$"

New-Item -ItemType Directory -Path $HomePath -Force
icacls $HomePath /inheritance:r
icacls $HomePath /grant "EMPRESA\$User:(OI)(CI)(M)"
icacls $HomePath /grant "EMPRESA\Administradores de Domínio:(OI)(CI)(F)"

New-SmbShare -Name $ShareName -Path $HomePath -ChangeAccess "EMPRESA\$User" -FullAccess "EMPRESA\Administradores de Domínio"

Set-ADUser -Identity $User -HomeDirectory "\\fs01\$ShareName" -HomeDrive "H:"
Get-ADUser $User -Properties HomeDirectory,HomeDrive | Select SamAccountName,HomeDirectory,HomeDrive
```

## Remover acesso com segurança

```powershell
# Remover usuário do grupo, não mexer direto na ACL se o padrão for por grupo
Remove-ADGroupMember -Identity "DL-FS-TI-RW" -Members "j.silva" -Confirm:$true

# Validar
Get-ADPrincipalGroupMembership j.silva | Where-Object Name -like 'DL-FS-TI*'
```

Para desligamento:

```powershell
$User = "j.silva"
Disable-ADAccount $User
Get-ADPrincipalGroupMembership $User |
  Where-Object {$_.Name -ne "Domain Users"} |
  ForEach-Object { Remove-ADGroupMember -Identity $_.DistinguishedName -Members $User -Confirm:$false }
Move-ADObject -Identity (Get-ADUser $User).DistinguishedName -TargetPath "OU=Desligados,DC=empresa,DC=local"
```

## Script de onboarding idempotente

Use este modelo quando o usuário pedir “automatizar criação de user e liberação de pastas”.

```powershell
param(
  [Parameter(Mandatory)] [string]$Sam,
  [Parameter(Mandatory)] [string]$DisplayName,
  [Parameter(Mandatory)] [string]$GivenName,
  [Parameter(Mandatory)] [string]$Surname,
  [Parameter(Mandatory)] [string[]]$Groups,
  [string]$OU = "OU=Usuarios,DC=empresa,DC=local"
)

Import-Module ActiveDirectory

$existing = Get-ADUser -Filter "SamAccountName -eq '$Sam'" -ErrorAction SilentlyContinue
if (-not $existing) {
  $pwd = Read-Host "Senha temporária" -AsSecureString
  New-ADUser -SamAccountName $Sam -UserPrincipalName "$Sam@empresa.local" `
    -Name $DisplayName -DisplayName $DisplayName -GivenName $GivenName -Surname $Surname `
    -Path $OU -AccountPassword $pwd -ChangePasswordAtLogon $true -Enabled $false
  Write-Host "Usuário criado: $Sam"
} else {
  Write-Host "Usuário já existe: $Sam"
}

foreach ($g in $Groups) {
  $isMember = Get-ADGroupMember -Identity $g -Recursive | Where-Object SamAccountName -eq $Sam
  if (-not $isMember) {
    Add-ADGroupMember -Identity $g -Members $Sam
    Write-Host "Adicionado em grupo: $g"
  } else {
    Write-Host "Já membro: $g"
  }
}

Enable-ADAccount -Identity $Sam
Get-ADUser $Sam -Properties Enabled,MemberOf | Select SamAccountName,Enabled
```

## GPO básica para onboarding

A skill também cobre orientação segura para GPO, principalmente quando o onboarding depende de política aplicada por OU ou grupo. Use GPO com leitura primeiro, backup e alteração pequena.

Pré-requisitos:

```powershell
Import-Module GroupPolicy
Get-Command Get-GPO, New-GPO, New-GPLink, Backup-GPO
```

Inventariar GPOs e links antes de mexer:

```powershell
# Listar GPOs
Get-GPO -All | Select DisplayName,Id,Owner,GpoStatus,CreationTime,ModificationTime

# Ver links em uma OU
Get-GPInheritance -Target "OU=Usuarios,DC=empresa,DC=local" |
  Select -ExpandProperty GpoLinks |
  Select DisplayName,Enabled,Enforced,Order

# Backup antes de alterar
$BackupPath = "D:\Backups\GPO"
New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null
Backup-GPO -All -Path $BackupPath
```

Criar e linkar uma GPO de onboarding, sem configurar itens perigosos automaticamente:

```powershell
$GpoName = "GPO-Usuarios-Onboarding"
$TargetOU = "OU=Usuarios,DC=empresa,DC=local"

if (-not (Get-GPO -Name $GpoName -ErrorAction SilentlyContinue)) {
  New-GPO -Name $GpoName -Comment "Políticas padrão de onboarding de usuários"
}

# Linkar na OU; validar herança antes em produção
New-GPLink -Name $GpoName -Target $TargetOU -LinkEnabled Yes
Get-GPInheritance -Target $TargetOU | Select -ExpandProperty GpoLinks
```

Validar no cliente/usuário afetado:

```cmd
gpupdate /force
gpresult /r
gpresult /h C:\Temp\gpresult.html
```

Cuidados:

- não alterar Default Domain Policy sem necessidade real;
- preferir GPO nova, pequena e com nome claro;
- testar em OU piloto antes de aplicar no domínio inteiro;
- fazer backup/export antes de editar;
- documentar quem pediu, alvo da OU, GPO criada e rollback.

## Integração Hermes → AD

Opções comuns:

1. **Hermes rodando no próprio Windows/servidor administrativo**: executar PowerShell local com módulo AD.
2. **Hermes Linux acessando Windows via SSH**: habilitar OpenSSH Server no Windows e executar `powershell.exe` remoto.
3. **Hermes Linux acessando WinRM**: usar `pywinrm`/`pypsrp`, Kerberos/NTLM conforme política.
4. **API interna**: criar um microserviço FastAPI/PowerShell restrito, com endpoints de alto nível (`criar_usuario`, `liberar_pasta`) e logs.

Exemplo SSH a partir do Linux:

```bash
ssh svc-hermes-ad@dc01 'powershell -NoProfile -Command "Get-ADDomain | Select DNSRoot"'
```

Exemplo com script versionado:

```bash
scp scripts/onboard-user.ps1 svc-hermes-ad@dc01:C:/Hermes/onboard-user.ps1
ssh svc-hermes-ad@dc01 'powershell -ExecutionPolicy Bypass -File C:\Hermes\onboard-user.ps1 -Sam j.silva -DisplayName "João Silva" -GivenName João -Surname Silva -Groups "GG-Funcionarios","DL-FS-TI-RW"'
```

## Diagnóstico rápido

### Usuário não acessa pasta

```powershell
Get-ADUser j.silva -Properties Enabled,LockedOut | Select SamAccountName,Enabled,LockedOut
Get-ADPrincipalGroupMembership j.silva | Select Name
Get-SmbShareAccess -Name "TI$"
icacls "D:\Dados\TI"
```

Causas comuns:
- usuário não fez logoff/logon após entrar no grupo;
- token Kerberos antigo sem o novo grupo;
- acesso no share ok, mas NTFS negando;
- `Deny` explícito ganhando de `Allow`;
- grupo errado (`R` em vez de `RW`);
- DFS apontando para outro target.

### Usuário criado não autentica

```powershell
Get-ADUser j.silva -Properties Enabled,LockedOut,PasswordExpired,PasswordLastSet,UserPrincipalName |
  Select SamAccountName,UserPrincipalName,Enabled,LockedOut,PasswordExpired,PasswordLastSet
```

Causas comuns:
- conta ainda desabilitada;
- UPN errado;
- senha temporária não definida corretamente;
- política de senha bloqueou a senha;
- replicação entre DCs ainda não ocorreu.

### Grupo não aplica

```powershell
Get-ADGroupMember "DL-FS-TI-RW" | Select SamAccountName,ObjectClass
repadmin /replsummary
```

No cliente Windows, validar token:

```cmd
whoami /groups
klist purge
```

## Boas práticas de desenho

- Uma OU para usuários ativos, outra para desligados e outra para service accounts.
- Separar grupos de função (`GG-Depto-TI`) de grupos de recurso (`DL-FS-TI-RW`).
- Evitar permissão direta em usuário; sempre preferir grupo.
- Usar nomes padronizados para grupos de pasta.
- Registrar automações em Git, sem senha no repositório.
- Exportar logs de execução para CSV/JSON.
- Revisar membros de grupos sensíveis periodicamente.
- Delegar permissões por OU, não no domínio inteiro.

## Armadilhas comuns

1. **Dar acesso direto ao usuário na ACL**: vira bagunça e dificulta auditoria. Use grupo.
2. **Mexer só no share e esquecer NTFS**: Windows avalia os dois; o mais restritivo vence.
3. **Usar Domain Admin na automação**: alto risco; delegue OU e file server específicos.
4. **Criar senha em texto claro no script**: use `Read-Host -AsSecureString`, cofre ou SecretManagement.
5. **Não validar replicação**: em ambiente com múltiplos DCs, mudança pode demorar.
6. **Não considerar token de logon**: usuário pode precisar logoff/logon para pegar novo grupo.
7. **Remover herança sem revisar**: pode travar acesso administrativo. Teste em pasta de laboratório.
8. **Publicar lista de usuários no grupo**: pode conter PII. Compartilhe só recorte necessário.

## Checklist de verificação

- [ ] Domínio/DC identificado com `Get-ADDomain`.
- [ ] Módulo `ActiveDirectory` carregado.
- [ ] Estado atual coletado antes da mudança.
- [ ] Escopo confirmado para alteração em produção.
- [ ] Usuário/grupo/share/pasta validado após executar.
- [ ] Permissões aplicadas em grupo, não diretamente em usuário.
- [ ] Senha/token não apareceu em chat, log público ou commit.
- [ ] Resultado final testado com usuário ou grupo alvo.

## Prompt pronto para o aluno usar

```text
/skill active-directory-ops
Tenho um domínio AD e quero automatizar criação de usuários e liberação de pastas. Primeiro me ajude a levantar o padrão de OUs, grupos, servidor de arquivos e permissões atuais. Depois gere scripts PowerShell seguros e idempotentes, sem expor senha/token.
```
