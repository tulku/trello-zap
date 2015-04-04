"""
Implements the planning code:

    1. Check if we have enough materials for all requests?
    2. If we don't generate orders
    3. Do we have enough materials for the first request?
"""


class Engine(object):

    def __init__(self, materials, requests):
        self.materials = materials
        self.requests = requests

    def calculate(self):
        needed = self.requests.get_total()
        # How much of each material do I need?
        material_required = self.materials.get_required_materials(needed)
        # Do I have enough of each of them?
        orders_needed = self.materials.have_enough(material_required)
        if (orders_needed):
            # Generate the required orders
            self.materials.create_orders(orders_needed)

        for request in self.requests.get_requests():
            required = self.materials.get_required_materials(request.amount)
            need_more = self.materials.have_enough(required)
            if len(need_more) == 0:
                date = self.materials.use(required)
                print 'Request {} for {}'.format(request.name, date)
            else:
                request.mark_impossible()
