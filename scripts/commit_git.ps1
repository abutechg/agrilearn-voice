$git = "$env:LOCALAPPDATA\Programs\MinGit\cmd\git.exe"

& $git rm -r --cached . 2>$null
Write-Host "Staging clean files..."
& $git add .

Write-Host "Committing..."
& $git commit -m "Initial commit: AgriLearn Voice multilingual ASR and benchmark"

Write-Host "Git status:"
& $git status -s
