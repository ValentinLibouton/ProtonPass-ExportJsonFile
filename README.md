# ProtonPass-ExportJsonFile
Transform ProtonPass export JSON file into object

## Note
Documentation will come later.

## Structure
Le fichier JSON contient les informations suivantes :

- `version` (string): la version du fichier ProtonPass
- `userId` (string): l'identifiant de l'utilisateur
- `encrypted` (boolean): indique si le fichier est chiffré ou non
- `vaults` (array): une liste des coffres (vaults) disponibles

Chaque coffre (vault) a les propriétés suivantes :
- `id` (string): l'identifiant du coffre
- `name` (string): le nom du coffre
- `description` (string): la description du coffre
- `display` (object): l'icône et la couleur associées au coffre
- `items` (array): une liste des éléments (items) dans le coffre

Chaque élément (item) a les propriétés suivantes :
- `itemId` (string): l'identifiant de l'élément
- `shareId` (string): l'identifiant du coffre auquel l'élément appartient
- `data` (object): les données de l'élément, comprenant les métadonnées et le contenu
- `state` (string): l'état de l'élément
- `aliasEmail` (string): l'adresse e-mail associée à l'élément
- `contentFormatVersion` (integer): la version du format de contenu
- `createTime` (string): la date de création de l'élément
- `modifyTime` (string): la date de modification de l'élément

Les données de chaque élément (data) comprennent :
- `metadata` (object): les métadonnées de l'élément, telles que le nom, la description, etc.
- `extraFields` (object): des champs supplémentaires spécifiques à l'élément
- `type` (string): le type de l'élément
- `content` (string): le contenu de l'élément
- `lastRevision` (string, facultatif): la dernière révision de l'élément

Les métadonnées (metadata) de chaque élément ont les propriétés suivantes :
- `name` (string): le nom de l'élément
- `note` (string): la note associée à l'élément
- `itemUuid` (string): l'identifiant unique de l'élément

Le contenu (content) de chaque élément a les propriétés suivantes :
- `username` (string): le nom d'utilisateur
- `password` (string): le mot de passe
- `urls` (array): une liste des URL associées à l'élément
- `totpUri` (string): l'URI du générateur de code à usage unique (TOTP) associé à l'élément