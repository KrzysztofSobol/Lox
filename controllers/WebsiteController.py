from repositories.WebsiteRepository import WebsiteRepository
from models.WebsiteModel import Website
from datetime import datetime
from utils.CryptoUtils import decrypt


class WebsiteController:
    def __init__(self, websiteRepository: WebsiteRepository, encryption_key: bytes = None):
        self.websiteRepository = websiteRepository
        self.encryption_key = encryption_key

    def set_encryption_key(self, encryption_key: bytes):
        self.encryption_key = encryption_key

    # unused but ill leave it just in case
    def get_user_website_by_id(self, user_id: int, website_id: int) -> Website:
        website = self.websiteRepository.get_user_website_by_id(website_id, user_id)
        if website:
            try:
                website.name = decrypt(website.name, self.encryption_key)
                website.url = decrypt(website.url, self.encryption_key)
            except Exception:
                return None
        return website

    def get_user_websites(self, user_id: int) -> list[Website]:
        websites = self.websiteRepository.get_all_by_user_id(user_id)
        decrypted_websites = []

        for website in websites:
            try:
                website.name = decrypt(website.name, self.encryption_key)
                website.url = decrypt(website.url, self.encryption_key)
                decrypted_websites.append(website)
            except Exception:
                continue

        return decrypted_websites

    def create_website(self, user_id: int, name: str, url: str) -> Website:
        website = Website(
            id=None,
            user_id=user_id,
            name=name,
            url=url,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return self.websiteRepository.create(website)

    def delete_website(self, website_id: int) -> bool:
        return self.websiteRepository.delete(website_id)