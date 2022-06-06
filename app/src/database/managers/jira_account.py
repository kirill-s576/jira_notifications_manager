from bson import ObjectId
from typing import Optional, Tuple, List

from .base import BaseAsyncMongoManager
from ..models.jira_account import JiraAccountCreate, JiraAccountRead


class JiraAccountAsyncMongoManager(BaseAsyncMongoManager):

    COLLECTION_NAME = "jira_accounts"

    async def get_account_by_resource_id(
            self, resource_id: str
    ) -> Optional[JiraAccountRead]:
        query = {
            "resource_id": resource_id
        }
        result = await self.collection.find_one(query, session=self.session)
        if not result:
            return None
        return JiraAccountRead(**result)

    async def get_and_replace_or_create_account(
            self, account: JiraAccountCreate
    ) -> Tuple[JiraAccountRead, bool]:
        exists_account = await self.get_account_by_resource_id(account.resource_id)
        if exists_account:
            account_data = await self.collection.find_one_and_replace(
                {"_id": exists_account.id},
                account.dict(by_alias=True),
                session=self.session
            )
            return JiraAccountRead(**account_data), False
        account_data = account.dict(by_alias=True)
        object_id = await self.create_object(account_data)
        response = JiraAccountRead(id=object_id, **account_data)
        return response, True

    async def get_user_accounts(self, user_id: str) -> List[JiraAccountRead]:
        query = {
            "user_id": user_id
        }
        cursor = self.collection.find(query, session=self.session)
        accounts = await cursor.to_list(None)
        response = [
            JiraAccountRead(**account) for account in accounts
        ]
        return response
