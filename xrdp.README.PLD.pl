=== Sesja: ===

Sesman, uruchamiając sesję użytkownika, korzysta ze skryptu
/etc/X11/xinit/Xclients. Dlatego, aby zmienić manager okien, najprościej
wpisać odpowiedni program w pliku ~/.desktop

Mozna również wskazać inny skrypt uruchamiający sesję Xów w konfiguracji
sesmana: /etc/xrdp/sesman.ini.

=== Uprawnieni użytkownicy: ===

Domyślnie tylko użytkownicy należący do grupy xrdp mają prawo logowania. Można
zmienić tą grupę w pliku /etc/xrdp/sesman.ini w polu TerminalServerUsers.
