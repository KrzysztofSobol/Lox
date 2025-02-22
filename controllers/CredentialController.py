from datetime import datetime
from models.CredentialModel import Credential
from utils.CryptoUtils import encrypt, decrypt

class CredentialController:
    def __init__(self, credentialRepository, websiteController, encryption_key: bytes = None):
        self.credentialRepository = credentialRepository
        self.websiteController = websiteController
        self.encryption_key = encryption_key # set during login

    def set_encryption_key(self, encryption_key: bytes):
        self.encryption_key = encryption_key

    def create_credential(self, user_id: int, url: str, username: str, password: str) -> Credential:
        normalized_url = self.normalizeUrl(url)

        websites = self.websiteController.get_user_websites(user_id)
        website = next((w for w in websites if w.name == normalized_url), None)

        encrypted_normalized_url = encrypt(normalized_url, self.encryption_key)
        encrypted_url = encrypt(url, self.encryption_key)

        if not website:
            website = self.websiteController.create_website(
                user_id=user_id,
                name=encrypted_normalized_url,
                url=encrypted_url
            )

        # encrypt the data provided by a user using the master's key
        encrypted_password = encrypt(password, self.encryption_key)
        encrypted_username = encrypt(username, self.encryption_key)

        credential = Credential(
            id=None,
            website_id=website.id,
            username=encrypted_username,
            password=encrypted_password,
            saved_link=encrypted_url,
            notes=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return self.credentialRepository.create(credential)

    def edit(self, credential_id: int, username: str = None, password: str = None) -> bool:
        updates = {}
        if username is not None and username.strip():
            updates['username'] = encrypt(username, self.encryption_key)
        if password is not None and password.strip():
            updates['password'] = encrypt(password, self.encryption_key)

        credential = self.credentialRepository.edit(credential_id, updates)
        credential.decrypted_password = decrypt(credential.password, self.encryption_key)
        credential.decrypted_username = decrypt(credential.username, self.encryption_key)
        return credential

    def delete(self, credential_id: int) -> bool:
        return self.credentialRepository.delete(credential_id)

    def getCredentialsByWebsite(self, website_id: int) -> list[Credential]:
        credentials = self.credentialRepository.get_all_by_website_id(website_id)

        for credential in credentials:
            try:
                credential.decrypted_password = decrypt(credential.password, self.encryption_key)
                credential.decrypted_username = decrypt(credential.username, self.encryption_key)
                credential.decrypted_saved_link = decrypt(credential.saved_link, self.encryption_key)
            except Exception:
                credential.decrypted_password = None
        return credentials

    @staticmethod
    def normalizeUrl(url: str) -> str:
        url = url.split('://')[-1]
        url = url.split('/')[0]
        if url.startswith('www.'):
            url = url[4:]
        return url