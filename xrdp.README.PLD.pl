=== Sesja: ===

Sesman, uruchamiając sesję użytkownika, korzysta ze skryptu
/etc/X11/xinit/Xclients. Dlatego, aby zmienić manager okien, najprościej
wpisać odpowiedni program w pliku ~/.desktop

Mozna również wskazać inny skrypt uruchamiający sesję Xów w konfiguracji
sesmana: /etc/xrdp/sesman.ini.

=== Uprawnieni użytkownicy: ===

Aby ograniczyć prawo do korzystania z xrdp do określonej grupy uzytkowników,
można wpisać tą grupę w pliku /etc/xrdp/sesman.ini w polu TerminalServerUsers.
