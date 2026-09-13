$git = "$env:LOCALAPPDATA\Programs\MinGit\cmd\git.exe"

Write-Host "Resetting last commit (which contained the token)..."
& $git reset --soft HEAD~1

Write-Host "Removing push_redeploy.ps1 from staging..."
& $git rm --cached scripts/push_redeploy.ps1 2>$null

Write-Host "Creating clean commit..."
& $git add -A
& $git commit -m "Trigger production redeploy"

Write-Host "Pushing to GitHub..."
& $git push $args[0] main --force

Write-Host "Done!"
