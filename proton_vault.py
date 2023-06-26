import json


class Content:
    """
    This class represents the credentials of a website
    """
    def __init__(self, username='', password='', urls=[], totpUri=''):
        """
        This class represents the credentials of a website
        :param username: credential username
        :param password: credential password
        :param urls: urls list credential
        :param totpUri: TOTP
        """
        self.username = username
        self.password = password
        self.urls = urls
        self.totpUri = totpUri

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "urls": self.urls,
            "totpUri": self.totpUri
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)


class Metadata:
    """
    This class contains the metadata of the credentials
    """
    def __init__(self, name, note, itemUuid):
        """
        This class contains the metadata of the credentials
        :param name: name written by user
        :param note: note written by user
        :param itemUuid:
        """
        self.name = name
        self.note = note
        self.itemUuid = itemUuid

    def to_dict(self):
        return {
            "name": self.name,
            "note": self.note,
            "itemUuid": self.itemUuid
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)


class Data:
    """
    This class groups the data, i.e. metadata and credential data
    """
    def __init__(self, metadata, extraFields, type, content, lastRevision=None):
        """
        This class groups the data, i.e. metadata and credential data
        :param metadata: see Metadata class
        :param extraFields:
        :param type: login or alias or note or password
        :param content: see Content classe
        :param lastRevision: chronological index
        """
        self.metadata = Metadata(**metadata)
        self.extraFields = extraFields
        self.type = type
        self.content = Content(**content)
        self.lastRevision = lastRevision

    def to_dict(self):
        return {
            "metadata": self.metadata.to_dict(),  # call dict method of Metadata class
            "extraFields": self.extraFields,
            "type": self.type,
            "content": self.content.to_dict(),  # call dict method of Content class
            "lastRevision": self.lastRevision
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)


class Item:
    """
    This class groups data and other complementary data
    """
    def __init__(self, itemId, shareId, data, state, aliasEmail, contentFormatVersion, createTime, modifyTime):
        """
        This class groups data and other complementary data
        :param itemId: unique item identifier
        :param shareId: the identifier of the vault to which the item belongs
        :param data: see Data class
        :param state:
        :param aliasEmail:
        :param contentFormatVersion:
        :param createTime:
        :param modifyTime:
        """
        self.itemId = itemId
        self.shareId = shareId
        self.data = Data(**data)
        self.state = state
        self.aliasEmail = aliasEmail
        self.contentFormatVersion = contentFormatVersion
        self.createTime = createTime
        self.modifyTime = modifyTime

    def to_dict(self):
        return {
            "itemId": self.itemId,
            "shareId": self.shareId,
            "data": self.data.to_dict(),  # call dict method of Data class
            "state": self.state,
            "aliasEmail": self.aliasEmail,
            "contentFormatVersion": self.contentFormatVersion,
            "createTime": self.createTime,
            "modifyTime": self.modifyTime
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)


class Vault:
    """
    This class represents a vault, vault is a folder containing several items (class Item)
    """
    def __init__(self, id, name, description, display, items):
        """
        This class represents a vault, vault is a folder containing several items (class Item)
        :param id: the vault identifier
        :param name: the name of the vault given by the user
        :param description:
        :param display: vault icon/symbol and this color
        :param items:
        """
        self.id = id
        self.name = name
        self.description = description
        self.display = display  # dict icon & color icon
        self.items = [Item(**items) for items in items]

    def get_id_by_name(self, name):
        if self.name == name:
            return self.id
        else:
            return None

    def to_dict(self):
        """
        :return: sub-dictionary
        """
        item_dicts = [item.to_dict() for item in self.items]
        return {
            "name": self.name,
            "description": self.description,
            "display": self.display,
            "items": item_dicts
        }

    def to_dict_root(self):
        """
        :return: primary dictionary of vaults
        """
        return {
            self.id: self.to_dict()
        }

    def __str__(self):
        """
        :return: print vaults
        """
        return json.dumps(self.to_dict_root(), indent=4)


class ProtonPass:
    """
    This class represent all password manager sub-divided by severals vaults
    """
    def __init__(self, content_json):
        """
        This class represent all password manager sub-divided by severals vaults
        :param content_json: json file of Proton-Pass
        """
        self.__dict__.update(content_json)
        self.version = content_json['version'] if "version" in content_json else None
        self.userId = content_json['userId'] if "userId" in content_json else None
        self.encrypted = content_json['encrypted'] if "encrypted" in content_json else None
        self.vaults = [Vault(id, value.get('name'), value.get('description'), value.get('display'), value.get('items'))
                       for id, value in content_json.get('vaults', {}).items()]

    def __str__(self):
        return str(content_json)


if __name__ == '__main__':

    with open('data.json', 'r') as file:
        content_json = json.load(file)
        proton_pass = ProtonPass(content_json)
        # print(proton_pass)  # print all json
        # print(proton_pass.version)
        # print(proton_pass.userId)
        # print(proton_pass.encrypted)
        #for vault in proton_pass.vaults:
            #print(vault)
            # print(vault.id)
            # print(vault.name)
            # print(vault.description)
            # print(vault.display)
            #for item in vault.items:
                #print(item)
                # print(item.itemId)
                # print(item.shareId)  # id vault
                ## print(item.data)
                # print(item.state)
                # print(item.aliasEmail)
                # print(item.contentFormatVersion)
                # print(item.createTime)
                # print(item.modifyTime)
                ## print(item.data.metadata) # dict
                # print(item.data.extraFields)
                # print(item.data.type)
                ## print(item.data.content) # dict
                # print(item.data.lastRevision)
                # print(item.data.metadata.name)
                # print(item.data.metadata.note)
                # print(item.data.metadata.itemUuid)
                # print(item.data.content.username)
                # print(item.data.content.password)
                # print(item.data.content.urls)
                # print(item.data.content.totpUri)
                # for url in item.data.content.urls:
                    # print(url)
