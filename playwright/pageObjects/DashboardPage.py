from pageObjects.OrderPage import OrderPage


class DashboardPage():

    def __init__(self, page):
        self.page = page

    def selectOrderNavLink(self):
        self.page.get_by_role('button', name='ORDERS').click()
        orderPage = OrderPage(self.page)
        return orderPage