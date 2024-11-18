import winreg

def list_installed_apps():
    apps = []
    registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    try:
        registry = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path)
        for i in range(0, winreg.QueryInfoKey(registry)[0]):
            app_name = winreg.EnumKey(registry, i)
            apps.append(app_name)
        winreg.CloseKey(registry)
    except Exception as e:
        print(f"Error accessing registry: {e}")
    return apps
