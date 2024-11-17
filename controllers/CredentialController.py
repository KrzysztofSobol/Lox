from datetime import datetime
from typing import List
from models.CredentialModel import Credential

class CredentialController:
    def __init__(self, credentialRepository, websiteController):
        self.credentialRepository = credentialRepository
        self.websiteController = websiteController

    def create_credential(self, user_id: int, url: str, username: str, password: str) -> Credential:
        normalized_url = self.normalizeUrl(url)

        websites = self.websiteController.get_user_websites(user_id)
        website = next((w for w in websites if w.name == normalized_url), None)

        if not website:
            website = self.websiteController.create_website(
                user_id=user_id,
                name=normalized_url,
                url=normalized_url
            )

        credential = Credential(
            id=None,
            website_id=website.id,
            username=username,
            password=password,
            saved_link=url,
            notes=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return self.credentialRepository.create(credential)

    def edit(self, credential_id: int, username: str = None, password: str = None) -> bool:
        updates = {}
        if username is not None and username.strip():
            updates['username'] = username
        if password is not None and password.strip():
            updates['password'] = password
        return self.credentialRepository.edit(credential_id, updates)

    def delete(self, credential_id: int) -> bool:
        return self.credentialRepository.delete(credential_id)

    def getCredentialsByWebsite(self, website_id: int) -> List[Credential]:
        return self.credentialRepository.get_all_by_website_id(website_id)

    @staticmethod
    def normalizeUrl(url: str) -> str:
        url = url.split('://')[-1]
        url = url.split('/')[0]
        if url.startswith('www.'):
            url = url[4:]
        return url