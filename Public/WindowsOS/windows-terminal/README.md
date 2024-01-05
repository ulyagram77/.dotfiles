
# Configuration Guide 
Here you can see how to config [terminal](https://www.microsoft.com/store/productId/9N0DX20HK701?ocid=pdpshare) on Windows 10/11.


## Dependensies

 - [oh-my-posh](https://ohmyposh.dev/)
 - [scoop file manager](https://scoop.sh/)
 - [terminal-icons](https://www.powershellgallery.com/packages/Terminal-Icons/0.9.0)
 - [power shell](https://www.microsoft.com/store/productId/9MZ1SNWT0N5D?ocid=pdpshare)



## How to setup

Copy `settings.json` file to folder of terminal by following this path or click on icon in the program:

```bash
  C:\Users\{your_user}\AppData\Local\Packages\Microsoft.WindowsTerminal\LocalState
```

Install `oh-my-posh` using `scoop`:

```bash
  scoop install https://github.com/JanDeDobbeleer/oh-my-posh/releases/latest/download/oh-my-posh.json
```

Setup theme in `profile file`, to create file use command:

```bash
  notepad $PROFILE
```

Paste some code in this file:

```bash
  oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH/theme-name.omp.json" | Invoke-Expression
  Import-Module -Name Terminal-Icons
```

Also you can find some themes on official github or resetup theirs json file, you can find them locally here:

```bash
  C:\Users\{your_user}\AppData\Local\Programs\oh-my-posh\themes
```

