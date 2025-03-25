import argparse
from db.db_manager import create_user, delete_user, list_users, reset_master_password,verify_master_password, store_password, retrieve_password
from core.stego import encode_text_in_image, decode_text_from_image

def create_user_cmd(args):
    create_user(args.username, args.password)

def delete_user_cmd(args):
    delete_user(args.username)

def list_users_cmd(args):
    list_users()

def reset_master_cmd(args):
    reset_master_password(args.username, args.old_password, args.new_password)

def verify_master_cmd(args):
    if verify_master_password(args.username, args.password):
        print("✅ Master password verified successfully.")
    else:
        print("❌ Incorrect master password.")

def add_password_cmd(args):
    """CLI command to add a password hidden inside an image."""
    encrypted_text = f"{args.service}|{args.account_username}|{args.password}"
    
    try:
        encode_text_in_image(args.input_image, encrypted_text, args.output_image)
        store_password(args.username, args.service, args.account_username, args.output_image)
        print(f"✅ Password hidden in {args.output_image} and stored in database.")
    except Exception as e:
        print(f"❌ Error encoding password: {e}")

def retrieve_password_cmd(args):
    """CLI command to retrieve a password from an image."""
    image_path = retrieve_password(args.username, args.service, args.account_username)
    
    if image_path:
        try:
            decrypted_text = decode_text_from_image(image_path)
            service, account_username, password = decrypted_text.split('|')
            print(f"🔑 Service: {service}\n👤 Username: {account_username}\n🔒 Password: {password}")
        except Exception as e:
            print(f"❌ Error decoding password: {e}")
    else:
        print(f"⚠️ No password found for {args.service} and {args.account_username}.")

def main():
    parser = argparse.ArgumentParser(description="🔐 StegoVault - Secure Password Vault with Steganography")
    subparsers = parser.add_subparsers(dest="command")

    # User management
    subparsers.add_parser("list-users", help="List all users").set_defaults(func=list_users_cmd)

    create_user_parser = subparsers.add_parser("create-user", help="Create a new user")
    create_user_parser.add_argument("username")
    create_user_parser.add_argument("password")
    create_user_parser.set_defaults(func=create_user_cmd)

    delete_user_parser = subparsers.add_parser("delete-user", help="Delete a user")
    delete_user_parser.add_argument("username")
    delete_user_parser.set_defaults(func=delete_user_cmd)

    reset_master_parser = subparsers.add_parser("reset-master", help="Reset master password")
    reset_master_parser.add_argument("username")
    reset_master_parser.add_argument("old_password")
    reset_master_parser.add_argument("new_password")
    reset_master_parser.set_defaults(func=reset_master_cmd)

    # Password storage
    add_password_parser = subparsers.add_parser("add-password", help="Store a password in an image")
    add_password_parser.add_argument("username")
    add_password_parser.add_argument("service")
    add_password_parser.add_argument("account_username")
    add_password_parser.add_argument("password")
    add_password_parser.add_argument("input_image")
    add_password_parser.add_argument("output_image")
    add_password_parser.set_defaults(func=add_password_cmd)

    retrieve_password_parser = subparsers.add_parser("retrieve-password", help="Retrieve a password from an image")
    retrieve_password_parser.add_argument("username")
    retrieve_password_parser.add_argument("service")
    retrieve_password_parser.add_argument("account_username")
    retrieve_password_parser.set_defaults(func=retrieve_password_cmd)

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
