class Slot:
    def __init__(self, slot_id):
        self.id = slot_id
        self.item = None  # None means the slot is empty

    def is_empty(self):
        return self.item is None

    def add_item(self, item):
        if self.is_empty():
            self.item = item
            return True
        return False

    def remove_item(self):
        self.item = None


class Inventory:
    def __init__(self, initial_slots=10):
        self.slots = [Slot(i + 1) for i in range(initial_slots)]  # Create 10 empty slots to start
        self.next_id = initial_slots + 1  # Track the next ID for new slots

    def add_item(self, item):
        # Find the first empty slot and add the item
        for slot in self.slots:
            if slot.is_empty():
                slot.add_item(item)
                return True

        # No empty slots, create more slots (even number only)
        if len(self.slots) % 2 == 0:  # Check if the number of slots is even
            new_slots = [Slot(self.next_id + i) for i in range(2)]  # Create two new slots
            self.slots.extend(new_slots)
            self.next_id += 2
            self.slots[-2].add_item(item)  # Add the item to the first new slot
            return True
        return False

    def remove_item(self, slot_id):
        if 1 <= slot_id <= len(self.slots):
            # Remove the item in the specified slot
            self.slots[slot_id - 1].remove_item()

            # Shift items to fill the gap
            for i in range(slot_id - 1, len(self.slots) - 1):
                self.slots[i].item = self.slots[i + 1].item
                self.slots[i].id = i + 1  # Update IDs
            self.slots[-1].remove_item()  # Last slot becomes empty
            return True
        return False

    def display_inventory(self):
        # Display all slots with their ID and items
        for slot in self.slots:
            status = f"Empty" if slot.is_empty() else f"Item: {slot.item}"
            print(f"Slot {slot.id}: {status}")


# Example Usage
inventory = Inventory(initial_slots=10)
inventory.add_item("Sword")
inventory.add_item("Shield")
inventory.add_item("Potion")
inventory.display_inventory()

print("\nRemoving item from slot 2:")
inventory.remove_item(2)
inventory.display_inventory()

print("\nAdding more items to trigger new slots:")
inventory.add_item("Helmet")
inventory.add_item("Boots")
inventory.display_inventory()
