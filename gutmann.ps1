<#
.SYNOPSIS
Securely deletes files or directories using the Gutmann method (35 passes).

.PARAMETER File
Specifies the path of the file to securely delete.

.PARAMETER Directory
Specifies the path of the directory to securely delete all files from.
#>

param (
    [string]$File,
    [string]$Directory
)

function Write-RandomData {
    param (
        [string]$Path,
        [int]$Passes = 35
    )

    try {
        $fileSize = (Get-Item $Path).Length
        for ($i = 1; $i -le $Passes; $i++) {
            $randomData = [byte[]]::new($fileSize)
            [void][System.Security.Cryptography.RandomNumberGenerator]::Fill($randomData)
            Set-Content -Path $Path -Value $randomData -Encoding Byte
            Write-Host "Pass $i/$Passes completed for $Path"
        }

        # Truncate and delete the file
        Clear-Content -Path $Path
        Remove-Item -Path $Path -Force
        Write-Host "File $Path securely deleted."
    } catch {
        Write-Host "Error: $($_.Exception.Message)"
    }
}

function SecurelyDeleteDirectory {
    param (
        [string]$DirectoryPath
    )

    if (!(Test-Path $DirectoryPath -PathType Container)) {
        Write-Host "Directory not found: $DirectoryPath"
        return
    }

    Get-ChildItem -Path $DirectoryPath -File -Recurse | ForEach-Object {
        Write-RandomData -Path $_.FullName
    }

    Remove-Item -Path $DirectoryPath -Recurse -Force
    Write-Host "Directory $DirectoryPath securely deleted."
}

if ($File) {
    if (Test-Path $File -PathType Leaf) {
        Write-RandomData -Path $File
    } else {
        Write-Host "File not found: $File"
    }
} elseif ($Directory) {
    SecurelyDeleteDirectory -DirectoryPath $Directory
} else {
    Write-Host "Please specify a file with -File or a directory with -Directory."
}
