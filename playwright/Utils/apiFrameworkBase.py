from playwright.sync_api import Playwright

from conftest import user_credentials

ordersPayload = {
        "orders": [
            {
                "country": "India",
                "productOrderedId": "6960eae1c941646b7a8b3ed3"
            }
        ]
    }

class APIUtils2:

    def get_token(self, playwright: Playwright, user_credentials):
        userEmail = user_credentials["userEmail"]
        userPassword = user_credentials["password"]
        apiRequestContext = playwright.request.new_context(base_url="https://rahulshettyacademy.com")
        response = apiRequestContext.post("/api/ecom/auth/login",
                               data={"userEmail": userEmail, "userPassword": userPassword})
        responseBody = response.json()
        return responseBody['token']

    def createOrder(self, playwright: Playwright, user_credentials: dict):
        token = self.get_token(playwright,user_credentials)
        apiRequestContext = playwright.request.new_context(base_url="https://rahulshettyacademy.com")
        response = apiRequestContext.post("/api/ecom/order/create-order", data=ordersPayload, headers={"Authorization": token})
        print(response.json())
        return response.json()['orders'][0]