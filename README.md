# Recoil-Plotting-Tool
Universal antirecoil script with custom plot mapping for all your favorite games

# Undetectable
This project is a POC, nothing official. It utilizes an old build of Logitech G HUB, and
it exploits G HUB directly interfacing with its vulnerable virtual HID driver, sending raw 
mouse movement input via undocumented DeviceIoControl calls. It may be blocked on better anticheats
such as EAC, VGK, FACEIT

# Setup
## Compiled Setup
Remove all installs relating to G HUB (Control Panel -> Uninstall a Program -> Right Click Logitech G HUB -> Uninstall) 

Install [lghub_installer_2021.3.5164.exe](http://irisdma.cdn.zerocdn.com/lghub_installer_2021.3.5164.exe)

Continue through the full setup as normal

Open "svchost.exe" as administraitor

Done!

## Source Code Setup
Install Python 3.9.X + (add py.exe to path)

Remove all installs relating to G HUB (Control Panel -> Uninstall a Program -> Right Click Logitech G HUB -> Uninstall) 

Install [lghub_installer_2021.3.5164.exe](http://irisdma.cdn.zerocdn.com/lghub_installer_2021.3.5164.exe)

Continue through the full setup as normal

Open a cmd prompt and run "pip install pyside6"

Open a cmd prompt in the same directory and run "main.py"

Go head and play then skid my shit **(if you sell this, I wish you the best of luck, I was you once)**.

### Note: This will most definitley be blocked on these games
Apex Legends, Fortnite, Rust, Dead by Daylight, Halo: The Master Chief Collection, Fall Guys, New World, Outriders, 
Spellbreak, Ark: Survival Evolved, Predator: Hunting Grounds, Valorant, League of Legends, CS2 (Faceit)

Also, this is lowkey shit I will release one for CS2 (VAC)

![AK-47 Recoil Compensation](https://cdn.discordapp.com/attachments/1378082147533066280/1384557160591003729/ak47-compensation-curve.gif?ex=6852dcd6&is=68518b56&hm=1fe91c87d006283122c71b7700f647394424ede28d176e884601bd0bbdb42f79)

