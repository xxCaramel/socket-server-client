from dataclasses import dataclass

@dataclass
class ServerGroup:

    name: str
    admin: str
    users: any

    def size(self)->int:
        return len(self.users)
    
    def in_group(self,user)->bool:
        if user in self.users:
            return True
        else:
            return False

    def remove_users(self,requester,old_users)->bool:

        if len(old_users) and self.is_admin(requester):
            for user in old_users:
                if user in self.users:
                    self.users.remove(user)
            return True
        else:
            return False

    def add_users(self,requester,new_users)->bool:
        if len(new_users) and self.is_admin(requester):
            for user in new_users:
                self.users.append(user)
                return True
        else:
            return False

    def is_admin(self,user):
        return (user == self.admin)

