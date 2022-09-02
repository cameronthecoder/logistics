# Logistics
Gtk/Python native Docker client for GNOME.

## Dependencies
- PyGObject (gtk bindings for Python)
- libadwaita (styling)
- vte (terminal emulator for gtk)
- meson
- ninja


## Building from source
```bash
meson builddir --prefix=/usr/local
sudo ninja -C builddir install
```
## Design Credits
This project uses some design elements from these projects:
- [https://gitlab.gnome.org/World/Fragments](Fragments)
- [https://gitlab.gnome.org/World/Shortwave](Shortwave)

## Contributions
All contributions are welcome, no matter how big or small :) Major changes should be discussed with an issue or email first. 

## Translations
Translations are still a work-in-progress. I will update this when more information is available. 


## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
