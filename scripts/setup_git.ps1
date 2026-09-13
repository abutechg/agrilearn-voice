$git = "$env:LOCALAPPDATA\Programs\MinGit\cmd\git.exe"
Write-Host "Using Git at: $git"

& $git init -b main
& $git config user.name "abutechg"
& $git config user.email "abutechg@users.noreply.github.com"
& $git remote remove origin 2>$null
& $git remote add origin https://github.com/abutechg/agrilearn-voice.git

Write-Host "Git status summary:"
& $git status -s
