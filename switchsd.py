# SwitchSD - A tool to automatically download the latest versions of the required sd files for Atmosphere
# Author - Archit Date (thecommondude)

import json
import requests
import re
import zipfile
import os
import sys

# File paths that point to the latest release via the GitHub API or to nh-server.github.io/switch-guide static path
HEKATE = ('https://api.github.com/repos/CTCaer/Hekate/releases/latest', 'hekate_ctcaer_(.*)_Nyx_(.*)\.zip')
HEKATE_IPL_EMU = 'https://nh-server.github.io/switch-guide/files/emu/hekate_ipl.ini'
HEKATE_IPL_SYS = 'https://nh-server.github.io/switch-guide/files/sys/hekate_ipl.ini'
BOOTLOGOS = 'https://nh-server.github.io/switch-guide/files/bootlogos.zip'
ATMOSPHERE = ('https://api.github.com/repos/Atmosphere-NX/Atmosphere/releases/latest', 'atmosphere-(.*)-master-(.*)+hbmenu-(.*)\.zip')
LOCKPICK_RCM = ('https://api.github.com/repos/shchmue/Lockpick_RCM/releases/latest', 'Lockpick_RCM\.bin')
EDIZON = ('https://api.github.com/repos/WerWolv/EdiZon/releases/latest', 'SD\.zip')
FTPD = ('https://api.github.com/repos/mtheall/ftpd/releases/latest', 'ftpd\.nro')
NXTHEMEINSTALLER = ('https://api.github.com/repos/exelix11/SwitchThemeInjector/releases/latest', 'NXThemesInstaller\.nro')
NXSHELL = ('https://api.github.com/repos/joel16/NX-Shell/releases/latest', 'NX-Shell\.nro')
HBAPPSTORE = ('https://api.github.com/repos/vgmoose/hb-appstore/releases/latest', 'appstore\.nro')


# helper functions

def get_oauth_token():
    if not os.path.exists('config.json'):
        return None
    else:
        with open('config.json', 'r') as fp:
            js = json.load(fp)
        if 'oauth-token' in js.keys():
            return js['oauth-token']
        return None

def download_file(url, output_dir, filename = None):
    if filename == None:
        filename = url.rsplit('/', 1)[1]
    r = requests.get(url)
    with open(output_dir + '/' + filename, 'wb') as f:
        f.write(r.content)
    return filename

def get_github_asset_url(path, regex):
    oauth = get_oauth_token()
    if oauth:
        assets = json.loads(requests.get(path, headers={'Authorization': 'token {}'.format(oauth)}).text)['assets']
    else:
        assets = json.loads(requests.get(path).text)['assets']
    for i in assets:
        if re.match(regex, i['name']):
            return i['browser_download_url']
    return None

def extract_all_zip(zippath, location):
    with zipfile.ZipFile(zippath, 'r') as zip_ref:
        zip_ref.extractall(location)

def extract_file(zippath, filename, location):
    with zipfile.ZipFile(zippath, 'r') as zip_ref:
        try:
            zip_ref.extract(filename, location)
            return filename
        except:
            for file in zip_ref.namelist():
                if re.match(filename, file):
                    zip_ref.extract(file, location)
                    return file

def extract_directory(zippath, directory, location):
    with zipfile.ZipFile(zippath, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.startswith(directory+'/'):
                zip_ref.extract(file, location)


def download_all(downloadable, dlpath):
    for i in downloadable:
        if type(i) is tuple:
            gurl = get_github_asset_url(i[0], i[1])
            download_file(gurl, dlpath)
        else:
            download_file(i, dlpath)

def prepare_sd(path, EMUNAND=True):
    rootpath = path + '/sdswitch'

    # Copy the contents of the Atmosphere .zip file to the root of your SD card
    fname = download_file(get_github_asset_url(ATMOSPHERE[0], ATMOSPHERE[1]), path)
    extract_all_zip(path+'/'+fname, rootpath)
    os.remove(path+'/'+fname)

    # Copy the bootloader folder from the Hekate .zip file to the root of your SD card
    # Copy Hekate's .bin file from the Hekate .zip file to the atmosphere folder on your SD card
    # Delete reboot_payload.bin in the atmosphere folder on your SD card
    # Rename Hekate's .bin file to reboot_payload.bin
    fname = download_file(get_github_asset_url(HEKATE[0], HEKATE[1]), path)
    extract_directory(path+'/'+fname, 'bootloader', rootpath)
    fname2 = extract_file(path+'/'+fname, 'hekate_ctcaer_(.*)\.bin', rootpath+'/atmosphere')
    os.remove(rootpath+'/atmosphere/reboot_payload.bin')
    os.rename(rootpath+'/atmosphere/'+fname2, rootpath+'/atmosphere/reboot_payload.bin')
    os.remove(path+'/'+fname)

    # Copy the bootloader folder from the bootlogos.zip file to the root of your SD card
    fname = download_file(BOOTLOGOS, path)
    extract_directory(path+'/'+fname, 'bootloader', rootpath)
    os.remove(path+'/'+fname)
    
    # Copy hekate_ipl.ini to the bootloader folder on your SD card
    if EMUNAND:
        download_file(HEKATE_IPL_EMU, rootpath+'/bootloader')
    else:
        download_file(HEKATE_IPL_SYS, rootpath+'/bootloader')

    # Copy Lockpick_RCM.bin to the /bootloader/payloads folder on your SD card
    download_file(get_github_asset_url(LOCKPICK_RCM[0], LOCKPICK_RCM[1]), rootpath+'/bootloader/payloads')
    
    # Copy the contents of the EdiZon SD.zip file to the root of your SD card
    fname = download_file(get_github_asset_url(EDIZON[0], EDIZON[1]), path)
    extract_all_zip(path+'/'+fname, rootpath)
    os.remove(path+'/'+fname)

    # Create a folder named appstore inside the switch folder on your SD card, and put appstore.nro in it
    if not os.path.exists(rootpath+'/switch/appstore'):
        os.mkdir(rootpath+'/switch/appstore')
    download_file(get_github_asset_url(HBAPPSTORE[0], HBAPPSTORE[1]), rootpath+'/switch/appstore')

    # Copy ftpd.nro, NX-Shell.nro and NxThemesInstaller.nro to the switch folder on your SD card
    download_file(get_github_asset_url(FTPD[0], FTPD[1]), rootpath+'/switch')
    download_file(get_github_asset_url(NXSHELL[0], NXSHELL[1]), rootpath+'/switch')
    download_file(get_github_asset_url(NXTHEMEINSTALLER[0], NXTHEMEINSTALLER[1]), rootpath+'/switch')
    

if __name__ == '__main__':
    # Usage: python switchsd.py [--sys]
    EMUNAND = True

    if '--sys' in sys.argv or '--sysnand' in sys.argv:
        EMUNAND = False
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists('sdswitch'):
        os.mkdir('sdswitch')
    prepare_sd(os.getcwd(), EMUNAND)