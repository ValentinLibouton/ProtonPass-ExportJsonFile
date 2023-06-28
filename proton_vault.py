import json
import random
import string


class PasswordManager:
    """
    This class represent all password manager sub-divided by severals vaults
    """
    version = "1.0.0"
    encrypted = False

    def __init__(self, version=version, user_id=None, encrypted=encrypted, vaults=None):
        """
        Initializes a new instance of the PasswordManager class.
        :param version: The version of the password manager.
        :param user_id: The user ID associated with the password manager.
        :param encrypted: Indicates whether the password manager is encrypted or not.
        :param vaults: A dictionary of vaults contained in the password manager.
        """
        self.version = version
        self.user_id = user_id or generate_unique_id()
        self.encrypted = encrypted
        self.vaults = vaults or {}

    def add_vault(self, vault_id=None, name=None, description=None, display=None, items=None):
        """
        Adds a new vault to the password manager.
        :param vault_id: The ID of the vault.
        :param name: The name of the vault.
        :param description: The description of the vault.
        :param display: The display settings of the vault.
        :param items: A list of items contained in the vault.
        """
        vault_id = vault_id or generate_unique_id()
        vault = Vault(name=name, description=description, display=display, items=items, vault_id=vault_id)
        self.vaults[vault_id] = vault

    def get_vault(self, name):
        """
        Retrieves a vault with the specified name from the password manager.
        :param name: The name of the vault to retrieve.
        :return: The vault with the specified name, or None if not found.
        """
        for vault_id, vault in self.vaults.items():
            if vault.name == name:
                return vault
        return None

    def get_vault_by_id(self, vault_id):
        """
        Retrieves a vault with the specified ID from the password manager.
        :param vault_id: The ID of the vault to retrieve.
        :return: The vault with the specified ID.
        :raises ValueError: If a vault with the specified ID does not exist.
        """
        if vault_id in self.vaults:
            return self.vaults[vault_id]
        else:
            raise ValueError("Vault with ID '{}' does not exist.".format(vault_id))

    def list_vaults_name(self):
        """
        Lists the names of all the vaults in the password manager.
        :return: A list of vault names.
        """
        return [vault.name for vault in self.vaults.values()]

    def list_vaults_id(self):
        """
        Lists the IDs of all the vaults in the password manager.
        :return: A list of vault IDs.
        """
        return [vault_id for vault_id in self.vaults.keys()]

    def to_dict(self):
        """
        Converts the password manager object to a dictionary.
        :return: A dictionary representation of the password manager object.
        """
        vaults_dict = {}
        for vault_id, vault in self.vaults.items():
            vault_dict = vault.to_dict()
            if isinstance(vault.display, Display):
                vault_dict["display"] = vault.display.to_dict()
            vaults_dict[vault_id] = vault_dict

        return {
            "version": self.version,
            "userId": self.user_id,
            "encrypted": self.encrypted,
            "vaults": vaults_dict
        }

    def __str__(self):
        return self.to_json(indent=4)

    @classmethod
    def from_dict(cls, data):
        """
        Creates a new password manager object from a dictionary.
        :param data: A dictionary representing a password manager object.
        :return: A new password manager object.
        """
        version = data.get("version")
        user_id = data.get("userId")
        encrypted = data.get("encrypted")
        vaults_data = data.get("vaults", {})
        vaults = {}
        for vault_id, vault_data in vaults_data.items():
            vault = Vault.from_dict(vault_id, vault_data)  # Appeler la méthode from_dict() de la classe Vault avec l'ID du coffre-fort
            vaults[vault_id] = vault
        return cls(version, user_id, encrypted, vaults)


    def to_json(self, indent=None):
        """
        Converts the password manager object to a JSON string.
        :param indent: The number of spaces to use for indentation.
        :return: A JSON string representation of the password manager object.
        """
        data = self.to_dict()
        return json.dumps(data, indent=indent)

    @classmethod
    def from_json(cls, json_data):
        """
        Creates a new password manager object from a JSON string.
        :param json_data: A JSON string representing a password manager object.
        :return: A new password manager object.
        """
        data = json.loads(json_data)
        return cls.from_dict(data)


class Vault:
    """
    This class represents a vault in a password manager.
    """
    def __init__(self, vault_id, name, description, display=None, items=None):
        """
        Initializes a new instance of the Vault class.
        :param vault_id: The ID of the vault.
        :param name: The name of the vault.
        :param description: The description of the vault.
        :param display: The display settings of the vault.
        :param items: A list of items contained in the vault.
        """
        self.vault_id = vault_id
        self.name = name
        self.description = description
        if isinstance(display, Display):
            self.display = display
        else:
            self.display = Display()
        self.items = items or []

    def add_item(self, itemId=None, data=None, state=None, aliasEmail=None, contentFormatVersion=None, createTime=None, modifyTime=None, name=None, type=None):
        """
        Adds an item to the vault.
        :param itemId: The ID of the item (optional).
        :param data: The data object containing the item's details.
        :param state: The state of the item. Ex into trash or not
        :param aliasEmail: The alias email associated with the item.
        :param contentFormatVersion: The content format version of the item.
        :param createTime: The creation time of the item.
        :param modifyTime: The modification time of the item.
        :param name: The name of the item.
        :param type: The type of the item.
        :return: None
        """
        itemId = itemId or generate_unique_id()
        shareId = self.vault_id
        item = Item(itemId=itemId, shareId=shareId, data=data, state=state, aliasEmail=aliasEmail, contentFormatVersion=contentFormatVersion, createTime=createTime, modifyTime=modifyTime, name=name, type=type)
        self.items.append(item)

    def list_item_id(self):
        """
        Returns a list of item IDs in the vault.
        :return: A list of item IDs.
        """
        return [item.itemId for item in self.items]

    def get_item(self, item_id):
        """
        Retrieves an item from the vault based on the item ID.
        :param item_id: The ID of the item to retrieve.
        :return: The item object if found, None otherwise.
        """
        for item in self.items:
            if item.itemId == item_id:
                return item
        return None

    def to_dict(self):
        """
        Converts the vault object to a dictionary representation.
        :return: A dictionary representation of the vault.
        """
        items_dict = []
        if isinstance(self.items, list):
            for item in self.items:
                if isinstance(item, Item):
                    items_dict.append(item.to_dict())
                # Vous pouvez ajouter une autre logique ici pour gérer les autres types d'objets, si nécessaire
        return {
            "name": self.name,
            "description": self.description,
            "display": self.display.to_dict(),
            "items": items_dict
        }

    def __str__(self):
        """
        Returns a string representation of the vault object.
        :return: A string representation of the vault.
        """
        return self.to_json(indent=4)

    @classmethod
    def from_dict(cls, vault_id, data):
        """
        Creates a vault object from a dictionary representation.
        :param vault_id: The ID of the vault.
        :param data: The dictionary containing the vault data.
        :return: An instance of the Vault class.
        """
        name = data.get("name")
        description = data.get("description")
        display_data = data.get("display", {})
        display = Display.from_dict(display_data) if display_data else Display()  # Utilisation de la méthode from_dict de l'objet Display
        items = data.get("items", [])
        return cls(vault_id, name, description, display, items)

    def to_json(self, indent=None):
        """
        Converts the vault object to a JSON string.
        :param indent: The number of spaces to use for indentation (optional).
        :return: A JSON string representation of the vault.
        """
        data = self.to_dict()
        return json.dumps(data, indent=indent)

    @classmethod
    def from_json(cls, json_data):
        """
        Creates a vault object from a JSON string representation.
        :param json_data: The JSON string containing the vault data.
        :return: An instance of the Vault class.
        """
        data = json.loads(json_data)
        return cls.from_dict(data)

class Display:
    """
    This class represents the display settings for a vault.
    """
    def __init__(self, color=0, icon=0):
        """
        Initializes a new instance of the Display class.
        :param color: The color setting for the display.
        :param icon: The icon setting for the display.
        """
        self.color = color
        self.icon = icon

    def to_dict(self):
        """
        Converts the display object to a dictionary representation.
        :return: A dictionary representation of the display.
        """
        return {
            "color": self.color,
            "icon": self.icon
        }

    def __str__(self):
        """
        Returns a string representation of the display object.
        :return: A string representation of the display.
        """
        return self.to_json(indent=4)

    @classmethod
    def from_dict(cls, data):
        """
        Creates a display object from a dictionary representation.
        :param data: The dictionary containing the display data.
        :return: An instance of the Display class.
        """
        color = data.get("color", 0)
        icon = data.get("icon", 0)
        return cls(color, icon)

    def to_json(self, indent=None):
        """
        Converts the display object to a JSON string.
        :param indent: The number of spaces to use for indentation (optional).
        :return: A JSON string representation of the display.
        """
        data = self.to_dict()
        return json.dumps(data, indent=indent)

    @classmethod
    def from_json(cls, json_data):
        """
        Creates a display object from a JSON string representation.
        :param json_data: The JSON string containing the display data.
        :return: An instance of the Display class.
        """
        data = json.loads(json_data)
        return cls.from_dict(data)

class Item:
    """
    This class represents an item in a vault.
    """
    def __init__(self, itemId, shareId, data=None, state=None, aliasEmail=None, contentFormatVersion=None, createTime=None, modifyTime=None, name=None, type=None):
        """
        Initializes a new instance of the Item class.
        :param itemId: The ID of the item.
        :param shareId: The ID of the vault share containing the item.
        :param data: The data associated with the item.
        :param state: The state of the item.
        :param aliasEmail: The alias email of the item.
        :param contentFormatVersion: The content format version of the item.
        :param createTime: The creation time of the item.
        :param modifyTime: The modification time of the item.
        :param name: The name of the item.
        :param type: The type of the item.
        """
        self.itemId = itemId or generate_unique_id()
        self.shareId = shareId
        self.data = data or Data(name=name, type=type)
        self.state = state
        self.aliasEmail = aliasEmail
        self.contentFormatVersion = contentFormatVersion
        self.createTime = createTime
        self.modifyTime = modifyTime

    def to_dict(self):
        """
        Converts the item object to a dictionary representation.
        :return: A dictionary representation of the item.
        """
        data_dict = self.data.to_dict() if isinstance(self.data, Data) else {}
        return {
            "itemId": self.itemId,
            "shareId": self.shareId,
            "data": data_dict,
            "state": self.state,
            "aliasEmail": self.aliasEmail,
            "contentFormatVersion": self.contentFormatVersion,
            "createTime": self.createTime,
            "modifyTime": self.modifyTime
        }

    def __str__(self):
        """
        Returns a string representation of the item object.
        :return: A string representation of the item.
        """
        return self.to_json(indent=4)

    @classmethod
    def from_dict(cls, item_id, data):
        """
        Creates an item object from a dictionary representation.
        :param item_id: The ID of the item.
        :param data: The dictionary containing the item data.
        :return: An instance of the Item class.
        """
        return cls(
            item_id,
            data.get("shareId"),
            data.get("data"),
            data.get("state"),
            data.get("aliasEmail"),
            data.get("contentFormatVersion"),
            data.get("createTime"),
            data.get("modifyTime")
        )

    def to_json(self, indent=None):
        """
        Converts the item object to a JSON string.
        :param indent: The number of spaces to use for indentation (optional).
        :return: A JSON string representation of the item.
        """
        data = self.to_dict()
        return json.dumps(data, indent=indent)

    @classmethod
    def from_json(cls, json_data):
        """
        Creates an item object from a JSON string representation.
        :param json_data: The JSON string containing the item data.
        :return: An instance of the Item class.
        """
        data = json.loads(json_data)
        return cls.from_dict(data)


class Data:
    """
    This class represents the data associated with an item.
    """
    def __init__(self, metadata=None, extraFields=None, type=None, content=None, lastRevision=None, name=None):
        """
        Initializes a new instance of the Data class.
        :param metadata: The metadata associated with the data.
        :param extraFields: Additional fields of the data.
        :param type: The type of the data (login, alias, or note).
        :param content: The content of the data.
        :param lastRevision: The last revision of the data.
        :param name: The name of the data.
        """
        self.metadata = metadata or Metadata(name=name)
        self.extraFields = extraFields or []
        self.type = type  # login or alias or note
        self.content = content or Content()
        self.lastRevision = lastRevision

    def to_dict(self):
        """
        Converts the data object to a dictionary representation.
        :return: A dictionary representation of the data.
        """
        metadata_dict = self.metadata.to_dict() if isinstance(self.metadata, Metadata) else {}
        content_dict = self.content.to_dict() if isinstance(self.content, Content) else {}

        return {
            "metadata": metadata_dict,
            "extraFields": self.extraFields,
            "type": self.type,
            "content": content_dict,
            "lastRevision": self.lastRevision
        }

    def __str__(self):
        """
        Returns a string representation of the data object.
        :return: A string representation of the data.
        """
        return self.to_json(indent=4)


    @classmethod
    def from_dict(cls, data):
        """
        Creates a data object from a dictionary representation.
        :param data: The dictionary containing the data.
        :return: An instance of the Data class.
        """
        return cls(
            data.get("metadata"),
            data.get("extraFields"),
            data.get("type"),
            data.get("content"),
            data.get("lastRevision"),
        )

    def to_json(self, indent=None):
        """
        Converts the data object to a JSON string.
        :param indent: The number of spaces to use for indentation (optional).
        :return: A JSON string representation of the data.
        """
        data = self.to_dict()
        return json.dumps(data, indent=indent)

    @classmethod
    def from_json(cls, json_data):
        """
        Creates a data object from a JSON string representation.
        :param json_data: The JSON string containing the data.
        :return: An instance of the Data class.
        """
        data = json.loads(json_data)
        return cls.from_dict(data)

class Metadata:
    """
    This class represents the metadata associated with an item.
    """
    def __init__(self, name=None, note=None, itemUuid=None):
        """
        Initializes a new instance of the Metadata class.
        :param name: The name associated with the metadata.
        :param note: The note associated with the metadata.
        :param itemUuid: The UUID of the item associated with the metadata.
        """
        self.name = name
        self.note = note
        self.itemUuid = itemUuid

    def to_dict(self):
        """
        Converts the metadata object to a dictionary representation.
        :return: A dictionary representation of the metadata.
        """
        return {
            "name": self.name,
            "note": self.note,
            "itemUuid": self.itemUuid
        }

class Content:
    """
    This class represents the content associated with an item.
    """
    def __init__(self, username=None, password=None, urls=None, totpUri=None):
        """
        Initializes a new instance of the Content class.
        :param username: The username associated with the content.
        :param password: The password associated with the content.
        :param urls: The URLs associated with the content.
        :param totpUri: The TOTP URI associated with the content.
        """
        self.username = username or ""
        self.password = password or ""
        self.urls = urls or []
        self.totpUri = totpUri or ""

    def to_dict(self):
        """
        Converts the content object to a dictionary representation.
        :return: A dictionary representation of the content.
        """
        return {
            "username": self.username,
            "password": self.password,
            "urls": self.urls,
            "totpUri": self.totpUri
        }



#-------------------- Functions --------------------#


def load_password_manager_from_json_file(file_path):
    """
    Load a password manager from a JSON file.
    :param file_path: The path to the JSON file.
    :return: The loaded PasswordManager object.
    """
    with open(file_path, 'r') as file:
        #---------- Password Manager ----------#
        data = json.load(file)
        version = data.get('version')
        user_id = data.get('userId')
        encrypted = data.get('encrypted')
        vaults_data = data.get('vaults')
        pm = PasswordManager(version=version, user_id=user_id, encrypted=encrypted)
        # --------------------#

        for vault_id, vault_data in vaults_data.items():
            # ---------- Vault By Vault ----------#
            name = vault_data['name']
            description = vault_data['description']
            display_data = vault_data['display']
            items_data = vault_data['items']

            display = Display.from_dict(display_data) if display_data else Display()
            pm.add_vault(vault_id=vault_id, name=name, description=description, display=display)

            vault = pm.get_vault_by_id(vault_id)
            # --------------------#

            for item_data in items_data:
                # ---------- Item By Item ----------#
                itemId = item_data['itemId']
                #shareId = item_data['shareId'] #il est déjà automatiquement ajouté par la methode add_item
                data = Data(
                        Metadata(
                            item_data['data']['metadata']['name'],
                            item_data['data']['metadata']['note'],
                            item_data['data']['metadata']['itemUuid']
                        ),
                        item_data['data']['extraFields'],
                        item_data['data']['type'],
                        Content(
                            item_data['data']['content'].get('username'),
                            item_data['data']['content'].get('password'),
                            item_data['data']['content'].get('urls', []),
                            item_data['data']['content'].get('totpUri')
                        ),
                        item_data['data'].get('lastRevision')
                    )
                state = item_data['state']
                aliasEmail = item_data['aliasEmail']
                contentFormatVersion = item_data['contentFormatVersion']
                createTime = item_data['createTime']
                modifyTime = item_data['modifyTime']

                vault.add_item(itemId=itemId, data=data, state=state, aliasEmail=aliasEmail, contentFormatVersion=contentFormatVersion, createTime=createTime, modifyTime=modifyTime)
                # --------------------#
        return pm



def save_password_manager_to_json_file(password_manager, file_path):
    """
    Save a password manager to a JSON file.
    :param password_manager: The PasswordManager object to save.
    :param file_path: The path to the JSON file.
    """
    json_data = password_manager.to_json()
    with open(file_path, 'w') as file:
        file.write(json_data)

def generate_unique_id():
    """
    Generate a unique ID.
    :return: The generated unique ID.
    """
    chars = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(chars) for _ in range(86))
    unique_id += '=='
    return unique_id




if __name__ == '__main__':
    #---------- Example ----------#
    pm = load_password_manager_from_json_file("data.json")

    for vault in pm.list_vaults_name():
        # print(vault)
        pass

    vault_name_1 = pm.list_vaults_name()[0]
    vault = pm.get_vault(vault_name_1)
    # print(vault)
    item_ids = vault.list_item_id()
    # print(item_ids)
    item = vault.get_item(item_ids[0])
    #print(item)

    print(item.data.metadata.name)
    print(item.data.content.username)
    print(item.data.content.password)
    print(item.data.content.urls)
