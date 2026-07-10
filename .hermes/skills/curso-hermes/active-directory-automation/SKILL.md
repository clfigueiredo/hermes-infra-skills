---
name: active-directory-automation
description: Automatizar tarefas de Active Directory com PowerShell de forma segura: criação de usuários, grupos, GPOs vinculadas a OUs, liberação de pastas/compartilhamentos SMB e permissões NTFS.
version: 1.0.0
author: Fórum Telecom / Hermes Course
license: MIT
metadata:
  hermes:
    tags:
      - curso-hermes
      - active-directory
      - windows-server
      - powershell
      - gpo
      - group-policy
      - smb
      - ntfs
      - automation
    related_skills:
      - security-review
      - testing-quality-gates
---

# Active Directory Automation

Use esta skill quando o aluno pedir para automatizar rotinas de **Active Directory** no Hermes Agent: criar usuários, habilitar/desabilitar contas, adicionar em grupos, criar/liberar pastas de rede, aplicar permissões NTFS/SMB e validar o resultado.

## Escopo

Esta skill ajuda o Hermes a operar como assistente de automação AD/Windows Server, sempre com validação antes de alterar produção.

Casos cobertos:

- criar usuário com `New-ADUser`;
- definir senha inicial segura e exigir troca no próximo logon;
- habilitar/desabilitar usuário;
- adicionar usuário a grupos com `Add-ADGroupMember`;
- criar e vincular GPO básica com `New-GPO` e `New-GPLink`;
- consultar herança/aplicação de GPO por OU com `Get-GPInheritance` e `gpresult`;
- criar pasta de rede por setor/usuário;
- criar compartilhamento SMB com `New-SmbShare`;
- conceder acesso SMB com `Grant-SmbShareAccess`;
- ajustar NTFS com `icacls` ou ACL PowerShell;
- gerar scripts idempotentes e logs de execução.

Fora do escopo:

- burlar política de senha;
- coletar senha real de usuário em grupo/chat;
- expor senha, hash, token, domínio privado ou inventário sensível;
- executar alteração destrutiva sem confirmação humana.

## Regras obrigatórias

1. **Nunca inventar domínio, OU, grupo ou caminho**. Se faltar, pedir os dados mínimos.
2. **Nunca pedir senha real no grupo**. Para senha inicial, gerar placeholder ou orientar variável segura.
3. **Antes de executar mudança**, mostrar plano curto e comando de validação.
4. **Para permissões**, aplicar princípio do menor privilégio.
5. **Para `UPDATE` operacional em AD** — criar primeiro comandos de consulta (`Get-ADUser`, `Get-ADGroup`, `Get-Acl`) antes da alteração.
6. **Gerar script reversível** quando possível: registrar o que foi criado/alterado.

## Dados mínimos para criar usuário

Peça somente o necessário:

```text
Nome completo:
Login/SamAccountName:
OU destino:
E-mail/UPN:
Grupos:
Setor:
Pasta/compartilhamento necessário:
Servidor de arquivos:
```

## Fluxo operacional

### 1. Levantamento

Confirmar:

```powershell
Import-Module ActiveDirectory
Get-ADDomain
Get-ADOrganizationalUnit -Filter * | Select-Object Name,DistinguishedName
Get-ADGroup -Filter * | Select-Object Name,DistinguishedName
```

### 2. Pré-checagem do usuário

```powershell
$Sam = "j.silva"
Get-ADUser -Filter "SamAccountName -eq '$Sam'" -Properties Enabled,MemberOf |
  Select-Object SamAccountName,Enabled,DistinguishedName
```

Se já existir, não recriar. Ajustar apenas o necessário.

### 3. Criar usuário

Modelo seguro:

```powershell
Import-Module ActiveDirectory

$Nome = "João Silva"
$Sam = "j.silva"
$UPN = "j.silva@empresa.local"
$OU = "OU=Usuarios,DC=empresa,DC=local"
$SenhaInicial = Read-Host "Senha inicial" -AsSecureString

New-ADUser `
  -Name $Nome `
  -DisplayName $Nome `
  -SamAccountName $Sam `
  -UserPrincipalName $UPN `
  -Path $OU `
  -AccountPassword $SenhaInicial `
  -Enabled $true `
  -ChangePasswordAtLogon $true

Get-ADUser $Sam -Properties Enabled,UserPrincipalName,DistinguishedName |
  Select-Object SamAccountName,Enabled,UserPrincipalName,DistinguishedName
```

### 4. Adicionar a grupos

```powershell
$Sam = "j.silva"
$Grupos = @("Financeiro", "VPN-Usuarios")

foreach ($Grupo in $Grupos) {
  if (Get-ADGroup -Filter "Name -eq '$Grupo'") {
    Add-ADGroupMember -Identity $Grupo -Members $Sam
  } else {
    Write-Warning "Grupo não encontrado: $Grupo"
  }
}

Get-ADPrincipalGroupMembership $Sam | Select-Object Name | Sort-Object Name
```

### 5. Criar pasta e liberar acesso

Exemplo com pasta por usuário:

```powershell
$Sam = "j.silva"
$Path = "D:\\Shares\\Usuarios\\$Sam"
$ShareName = $Sam.Replace('.', '-')
$GroupOrUser = "EMPRESA\\$Sam"

New-Item -ItemType Directory -Path $Path -Force | Out-Null

if (-not (Get-SmbShare -Name $ShareName -ErrorAction SilentlyContinue)) {
  New-SmbShare -Name $ShareName -Path $Path -ChangeAccess $GroupOrUser
}

icacls $Path /inheritance:r
icacls $Path /grant "Administrators:(OI)(CI)(F)"
icacls $Path /grant "$GroupOrUser:(OI)(CI)(M)"

Get-SmbShare -Name $ShareName
icacls $Path
```

> Ajuste `Modify`/`Read`/`FullControl` conforme política interna. Evite `Everyone` e `Domain Users` com escrita ampla.

## Script base idempotente

Quando o usuário pedir automação completa, gerar um script `.ps1` com este padrão:

```powershell
param(
  [Parameter(Mandatory=$true)] [string]$Nome,
  [Parameter(Mandatory=$true)] [string]$Sam,
  [Parameter(Mandatory=$true)] [string]$UPN,
  [Parameter(Mandatory=$true)] [string]$OU,
  [string[]]$Grupos = @(),
  [string]$HomeRoot = "D:\\Shares\\Usuarios",
  [switch]$CriarPasta
)

Import-Module ActiveDirectory

$Existe = Get-ADUser -Filter "SamAccountName -eq '$Sam'" -ErrorAction SilentlyContinue
if (-not $Existe) {
  $Senha = Read-Host "Senha inicial" -AsSecureString
  New-ADUser -Name $Nome -DisplayName $Nome -SamAccountName $Sam -UserPrincipalName $UPN -Path $OU -AccountPassword $Senha -Enabled $true -ChangePasswordAtLogon $true
  Write-Host "Usuário criado: $Sam"
} else {
  Write-Host "Usuário já existe: $Sam"
}

foreach ($Grupo in $Grupos) {
  if (Get-ADGroup -Filter "Name -eq '$Grupo'" -ErrorAction SilentlyContinue) {
    Add-ADGroupMember -Identity $Grupo -Members $Sam -ErrorAction SilentlyContinue
    Write-Host "Grupo conferido: $Grupo"
  } else {
    Write-Warning "Grupo não encontrado: $Grupo"
  }
}

if ($CriarPasta) {
  $Path = Join-Path $HomeRoot $Sam
  New-Item -ItemType Directory -Path $Path -Force | Out-Null
  icacls $Path /inheritance:r | Out-Null
  icacls $Path /grant "Administrators:(OI)(CI)(F)" | Out-Null
  icacls $Path /grant "$env:USERDOMAIN\\$Sam:(OI)(CI)(M)" | Out-Null
  Write-Host "Pasta conferida: $Path"
}

Get-ADUser $Sam -Properties Enabled,UserPrincipalName,DistinguishedName |
  Select-Object SamAccountName,Enabled,UserPrincipalName,DistinguishedName
Get-ADPrincipalGroupMembership $Sam | Select-Object Name | Sort-Object Name
```

## Checklist de validação

Depois de qualquer alteração:

```powershell
Get-ADUser <sam> -Properties Enabled,UserPrincipalName,DistinguishedName,MemberOf
Get-ADPrincipalGroupMembership <sam> | Select-Object Name | Sort-Object Name
Test-Path <pasta>
Get-SmbShare -Name <share>
icacls <pasta>
```

## Resposta padrão para pedidos incompletos

Se o aluno pedir “cria uma skill/automação para AD criar usuário e liberar pastas”, responder pedindo só estes dados:

```text
Me manda o padrão de domínio/OU, grupos e caminho das pastas. Com isso eu monto o script PowerShell idempotente para criar usuário, adicionar grupos e liberar SMB/NTFS com validação.
```

## Pitfalls

- `SamAccountName` duplicado causa falha ou alteração no usuário errado.
- `icacls` com aspas erradas quebra em nomes com espaço.
- `Grant-SmbShareAccess` cuida do compartilhamento; NTFS precisa ACL separada.
- Permissão SMB liberada e NTFS negada ainda bloqueia acesso.
- Rodar PowerShell sem módulo RSAT/ActiveDirectory falha.
- Criar usuário fora da OU correta quebra GPO/login.
- `Domain Users` com escrita em pasta compartilhada costuma ser risco.

## Comportamento esperado do Hermes

Quando esta skill estiver carregada, Hermes deve:

1. pedir dados mínimos se faltarem;
2. gerar comandos/script PowerShell idempotente;
3. incluir validações antes/depois;
4. destacar riscos de permissão;
5. não executar alteração real sem confirmação e acesso ao Windows/AD;
6. mascarar domínio, usuários e caminhos se forem sensíveis.
