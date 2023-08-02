param(
    [string]$dir = "."
)

Get-ChildItem $dir -Recurse -Directory | ForEach-Object {
    [pscustomobject]@{
        Folder = $_.FullName
        Count = @(Get-ChildItem -Path $_.Fullname -File).Count
    }
} | Select-Object Folder, Count
