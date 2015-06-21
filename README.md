# zaphirweb
Appliction web python de conversion des fichiers XLSX vers XML et inversement.

Zaphir web est une application qui permet:

* De convertir des fichiers MS Excel (XLSX) respectant la mise en forme établie dans le cadre du partenariat CIGAL (www.cigalsace.org) en fichiers de métadonnées géographiques XML (norme 19139 / Inspire).
* De convertir des fichiers de métadonnées géographioques XML (norme 19139 / Inspire) en fichiers MS Excel XLSX selon une mise en forme établie dans le cadre du partenariat CIGAL (www.cigalsace.org). - [En cours de développement]

Pour ce faire, charger un fichier et laissez tourner...

Les formats supportés sont:

- XML: fichier de métadonnées respectant la norme ISO 19139 / Inspire
- XLSX: fichier MS Excel mis en forme selon le profil CIGAL
- ZIP: ensemble de fichier XML et/ou XLSX

Lors de la conversion:

- Les fichiers XML sont convertis en XLSX. - [En cours de développement]
- Les fichiers XLSX sont convertis en XML.
- Les autres fichiers sont ignorés.

NB: lors de la conversion d'un fichier XML en XLSX, les éléments relatifs aux spécifications INSPIRE sont ignorés.
