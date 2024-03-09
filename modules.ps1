# List of required Python modules with version specifications
$modules = @("flask==3.0.2", "requests==2.27.1")

# Function to check if a module is installed
function Is-ModuleInstalled {
    param (
        [string]$moduleName
    )

    try {
        $null = Get-Module -Name $moduleName -ListAvailable
        return $true
    } catch {
        return $false
    }
}

# Loop through the modules and install if not already installed
foreach ($module in $modules) {
    $moduleName = $module.Split("==")[0]
    if (-not (Is-ModuleInstalled $moduleName)) {
        Write-Host "Installing $module..."
        pip install $module
    } else {
        Write-Host "$module is already installed."
    }
}
