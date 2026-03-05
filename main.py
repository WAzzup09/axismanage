import json
import os
import re

class UserManager:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = self._load_data()

    def _load_data(self):
        """Betölti a felhasználókat a JSON fájlból. Ha nem létezik, üres listát ad."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Hiba a fájl olvasásakor. Új, üres adatbázis indul.")
                return []
        return []

    def _save_data(self):
        """Menti az aktuális felhasználói listát a JSON fájlba."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.users, file, ensure_ascii=False, indent=4)

    def add_user(self, name, email):
        """Új felhasználó hozzáadása, e-mail duplikáció szűrésével."""
        
        # 1. Ellenőrizzük, hogy az e-mail foglalt-e már
        for user in self.users:
            if user['email'].lower() == email.lower():
                print(f"\nHiba: Ezzel az e-mail címmel ({email}) már van regisztrált felhasználó!")
                return  # Kilépünk a függvényből, így az új felhasználó nem lesz elmentve

        # 2. Ha az e-mail szabad, mentjük az új adatokat (eredeti logika)
        new_id = 1 if not self.users else max(user['id'] for user in self.users) + 1
        
        new_user = {
            "id": new_id,
            "name": name,
            "email": email
        }
        self.users.append(new_user)
        self._save_data()
        print(f"Siker: '{name}' hozzáadva az adatbázishoz (ID: {new_id}).")

    def list_users(self):
        """Összes felhasználó kilistázása."""
        if not self.users:
            print("Nincsenek felhasználók az adatbázisban.")
            return

        print("\n--- Felhasználók Listája ---")
        for user in self.users:
            print(f"ID: {user['id']} | Név: {user['name']} | Email: {user['email']}")
        print("----------------------------\n")

    def delete_user(self, user_id):
        """Felhasználó törlése ID alapján."""
        for user in self.users:
            if user['id'] == user_id:
                self.users.remove(user)
                self._save_data()
                print(f"Siker: A(z) {user_id}-es ID-jű felhasználó törölve.")
                return
        print(f"Hiba: Nem található felhasználó a(z) {user_id}-es ID-vel.")

# --- INTERAKTÍV MENÜ ---
def main():
    manager = UserManager()

    while True:
        print("\n=== Felhasználókezelő Menü ===")
        print("1. Felhasználók listázása")
        print("2. Új felhasználó hozzáadása")
        print("3. Felhasználó törlése")
        print("4. Kilépés")
        
        choice = input("Válassz egy opciót (1-4): ")

        if choice == '1':
            manager.list_users()
            
        elif choice == '2':
            name = input("Add meg a nevet: ")
            
            # Ciklus, ami addig fut, amíg jó emailt nem kap
            while True:
                email = input("Add meg az email címet: ")
                # Megnézzük, hogy az email minta helyes-e
                if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                    break # Ha jó, kilépünk a ciklusból
                else:
                    print("Hiba: Érvénytelen email formátum! Kérlek, valós címet adj meg (pl. pelda@email.com).")
                    
            manager.add_user(name, email)
            
        elif choice == '3':
            try:
                user_id = int(input("Add meg a törlendő felhasználó ID-jét: "))
                manager.delete_user(user_id)
            except ValueError:
                print("Hiba: Az ID-nek számnak kell lennie!")
                
        elif choice == '4':
            print("Kilépés. Viszlát!")
            break
            
        else:
            print("Érvénytelen választás, próbáld újra!")

if __name__ == "__main__":
    main()