import ccxt  # библиотека для работы с различными криптобиржами


class Exchange:
    def __init__(self, exchange_id, api_key=None, secret=None):
        self.exchange = getattr(ccxt, exchange_id)({
            'apiKey': api_key,
            'secret': secret,
        })

    def get_balance(self):
        balance = self.exchange.fetch_balance()
        return balance["total"]

    def get_orders(self):
        orders = self.exchange.fetch_open_orders()
        return orders

    def cancel_order(self, order_id):
        result = self.exchange.cancel_order(order_id)
        return result

    def place_order(self, symbol, quantity, side, order_type, price=None, stop_loss=None, take_profit=None):
        order_params = {
            'symbol': symbol,
            'type': order_type,
            'side': side,
            'amount': quantity,
        }
        if order_type == "limit":
            order_params['price'] = price
        elif order_type == "stop_limit":
            order_params['price'] = price
            order_params['stopPrice'] = stop_loss
        elif order_type == "take_profit":
            order_params['price'] = price
            order_params['stopPrice'] = take_profit

        result = self.exchange.create_order(**order_params)
        return result
