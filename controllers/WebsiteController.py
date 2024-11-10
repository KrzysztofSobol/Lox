from repositories.WebsiteRepository import WebsiteRepository
from models.WebsiteModel import Website
from datetime import datetime

class WebsiteController:
    def __init__(self, websiteRepository: WebsiteRepository):
        self.websiteRepository = websiteRepository

    def get_user_websites(self, user_id: int) -> list[Website]:
        return self.websiteRepository.get_all_by_user_id(user_id)

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