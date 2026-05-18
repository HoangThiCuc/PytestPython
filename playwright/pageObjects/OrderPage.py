from pageObjects.OrderDetail import OrderDetail


class OrderPage:
    def __init__(self, page):
        self.page = page

    def viewOrder(self, orderId):
        orderRow = self.page.locator('tr').filter(has_text=orderId)
        orderRow.get_by_role('button', name='View').click()
        orderDetail = OrderDetail(self.page)
        return orderDetail