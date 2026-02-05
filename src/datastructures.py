"""
Update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- get_member: Should return a member from the self._members list
"""

from random import randint  


class FamilyStructure:  # Declares the family structure class.
    def __init__(self, last_name: str, initial_members: list = []):  # Constructor.
        self.last_name = last_name  # Stores the last name.
        self._members = []  # Initializes the internal members list.

        for member in initial_members:  # Iterates initial members.
            self.add_member(member)  # Adds each member using the method.

    # Add a new member to the family
    def add_member(self, member):  # Receives a member dictionary.
        self._members.append(member)  # Adds it to the internal list.

    # Delete a member from the family by ID
    def delete_member(self, id):  # Receives the id to delete.
        self._members = [member for member in self._members if member["id"] != id]  # Filters the list.

    # Get a specific member by ID
    def get_member(self, id: int):  # Receives the id to find.
        for member in self._members:  # Iterates members.
            if member["id"] == id:  # Checks id match.
                return member  # Returns the found member.
        return None  # Returns None if not found.

    # Get all members of the family
    def get_all_members(self):  # Returns all members.
        return self._members  # Returns the full list.

    