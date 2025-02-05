# Specify the folder to run the script in
$targetFolder = "recieved/mlr_serhiipaukovmicro"

Get-ChildItem -Path $targetFolder -Recurse | ForEach-Object {
    if ($_ -is [io.fileinfo]) {
        $relativePath = $_.FullName.Substring($targetFolder.Length)
        $fileContent = Get-Content $_.FullName
        Write-Output "`n<$relativePath>"
        Write-Output '"""'
        Write-Output $fileContent
        Write-Output '"""'
    }
}