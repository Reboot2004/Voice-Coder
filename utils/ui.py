from colorama import Fore, Style, init

init()

def print_info(message):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}")

def print_success(message):
    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")

def print_warning(message):
    print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}")

def print_error(message):
    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")

def print_ai(message):
    print(f"{Fore.MAGENTA}[ASSISTANT]{Style.RESET_ALL} {message}")

def confirm_execution(command):
    print(f"\n{Fore.YELLOW}Suggested Command:{Style.RESET_ALL} {Fore.WHITE}{Style.BRIGHT}{command}{Style.RESET_ALL}")
    choice = input(f"{Fore.GREEN}Execute? [y/N]: {Style.RESET_ALL}").lower()
    return choice == 'y'
