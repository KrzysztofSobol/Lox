from datetime import datetime
from typing import List
from models.CredentialModel import Credential

class CredentialController:
    def __init__(self, credentialRepository, websiteController):
        self.credentialRepository = credentialRepository
        self.websiteController = websiteController

    def create_credential(self, user_id: int, url: str, username: str, password: bytes) -> Credential:
        normalized_url = self.normalizeUrl(url)

        websites = self.websiteController.get_user_websites(user_id)
        website = next((w for w in websites if w.name == normalized_url), None)

        if not website:
            website = self.websiteController.create_website(
                user_id=user_id,
                name=normalized_url,
                url=normalized_url
            )

        # Create credential
        credential = Credential(
            id=None,
            website_id=website.id,
            username=username,
            encrypted_password=password,
            notes=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return self.credentialRepository.create(credential)

    def getCredentialsByWebsite(self, website_id: int) -> List[Credential]:
        return self.credentialRepository.get_all_by_website_id(website_id)

    @staticmethod
    def normalizeUrl(url: str) -> str:
        url = url.split('://')[-1]
        url = url.split('/')[0]
        if url.startswith('www.'):
            url = url[4:]
        return url