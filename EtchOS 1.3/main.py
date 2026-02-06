# EtchOS by mistaaB
import time
from pathlib import Path

# Initialize assistant_name globally
assistant_name = ""

# Global variable to control onboarding flow
continue_onboarding = True




def print_file_content(filename):
    # Path to the Wiki_Articles folder next to this script
    base_dir = Path(__file__).parent
    file_path = base_dir / "Wiki_Articles" / filename

    try:
        print(file_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"Error: {filename} was not found inside the 'Wiki_Articles' folder.")





def Language_En():
    print("In what language do you want to continue?")
    print("En - English")
    print("De - Deutsch")
    language = input()
    if "En" == language:
        print("I am now going to continue in English.")
        if continue_onboarding == True:
            Onboarding_En()
        else:
            Main_Menu_En()

    elif "De" == language:
        print("Ich werde nun in Deutsch vorfahren.")
        if continue_onboarding == True:
            Onboarding_De()
        else:
            Main_Menu_De()
    else:
        print("You can only choose one of the listed languages.")
        Language_En()

def Language_De():
    print("In welcher Sprache möchtest du fortfahren?")
    print("En - English")
    print("De - Deutsch")
    language = input()
    if "En" == language:
        print("I am now going to continue in English.")
        if continue_onboarding == True:
            Onboarding_En()
        else:
            Main_Menu_En()

    elif "De" == language:
        print("Ich werde nun in Deutsch vorfahren.")
        if continue_onboarding == True:
            Onboarding_De()
        else:
            Main_Menu_De()
    else:
        print("Du kannst nur die Sprachen auf der Liste wählen.")
        Language_De()


def Onboarding_En():
    global assistant_name  # Access the global variable
    global continue_onboarding
    continue_onboarding == False #TODO: Set continue_onboarding to False
    print("Let's continue!")
    print("What's your name?")
    user_name = input()
    print("Nice to meet you,", user_name, "!")
    print("I am your personal assistant, what are you going to call me?")
    assistant_name = input()  # Assign name to assistant_name
    print(assistant_name, ", I love this name!")
    print("That was the onboarding, if you have questions, ask me!")
    Main_Menu_En()

def Onboarding_De():
    global assistant_name  # Access the global variable
    global continue_onboarding
    continue_onboarding == False #TODO: Set continue_onboarding to False
    print("Lass uns weitermachen!")
    print("Wie heißt du?")
    user_name = input()
    print("Schön dich kennenzulernen, ", user_name, "!")
    print("Ich bin dein personaler Assistent, wie willst du mich nennen?")
    assistant_name = input()  # Assign name to assistant_name
    print(assistant_name, ", ich liebe diesen Name!")
    print("Das war das Onboarding, wenn du fragen hast, wende dich an mich!")
    
    Main_Menu_De()

def Main_Menu_En():
    global assistant_name  # Access the global variable
    print("----------------------------------------------")
    print("                  Main Menu                   ")
    print("----------------------------------------------")
    print("Programms:")
    print("L - Change Language")
    print("A -", assistant_name)  # Display assistant name
    print("S - System Info")
    start_programm = input("Input the corresponding letter: ")
    if "L" == start_programm:
        Language_En()
    elif "A" == start_programm:
        Assistant_En()
    elif "S" == start_programm:
        System_Info("En")  # Pass the language as argument
    else:
        print("Please only choose a letter from the List.")

def Main_Menu_De():
    global assistant_name  # Access the global variable
    print("----------------------------------------------")
    print("                  Hauptmenü                   ")
    print("----------------------------------------------")
    print("Programme:")
    print("L - Sprache ändern")
    print("A -", assistant_name)  # Display assistant name
    print("S - Sistem Informationen")
    start_programm = input("Gebe den korrespondierenden Buchstaben ein: ")
    if "L" == start_programm:
        Language_De()
    elif "A" == start_programm:
        Assistant_De()
    elif "S" == start_programm:
        System_Info("De")  # Pass the language as argument
    else:
        print("Bitte wähle nur Buchstaben aus der Liste aus.")

def Assistant_En():
    print("Hello, I am ", assistant_name, ", your personal assistant!")
    print("Do you want to just speak with me (s) or do you want to get help from the Wiki (w)?")
    assistant_options_wiki_speak = input("s or w: ")
    if "s" == assistant_options_wiki_speak:
        print("----------------------------------------------") # Speak mode
        print("Welcome to speak mode.")
    elif "w" == assistant_options_wiki_speak:
        print("----------------------------------------------") # Wiki mode
        print("Welcome to wiki mode.")
        print("These are the following articles:")
        print("1. How the OS works")
        print("2. Linux Kernel")
        print("3. EtchOS - all Errors explained")
        open_wiki_article = input("Input corresponding number: ")
        if open_wiki_article == "1":
            print_file_content("1._How_the_OS_works.txt")
        elif open_wiki_article == "2":
            print_file_content("2._Linux_Kernel.txt")
        elif open_wiki_article == "3":
            print_file_content("3._EtchOS_-_all_Errors_explained.txt")
        else:
            print("Please only choose from the List.")
        
        print("Type EXIT if you want to leave")
        exit_assistant = input()
        if exit_assistant == "EXIT":
            Main_Menu_En()
        else:
            


        




    else:
        print("Please only input s or w.")
        Assistant_En()

def Assistant_De():
    print("Hallo, ich bin ", assistant_name, ", dein persönlicher Assistent!")
    print("Willst du einfach mit mir sprechen (s) oder willst du Hilfe vom Wiki erhalten (w)?")

def System_Info(language):
    print("----------------------------------------------")
    print("                 System Info                  ")
    print("----------------------------------------------")
    print("EEEEEEE       OOOOOO         SSSSSS")
    print("EE           OO    OO       SS     ")
    print("EE           OO    OO       SS     ")
    print("EEEEEEE      OO    OO        SSSSS ")
    print("EE           OO    OO            SS")
    print("EE           OO    OO            SS")
    print("EEEEEEE       OOOOOO        SSSSSS ")
    print("EtchOS - Python Based Operating System 1.1")
    
    # Check if the 'language' variable matches the correct options
    if language == "En":
        Main_Menu_En()
    elif language == "De":
        Main_Menu_De()
    else:
        print("Syntax Error: Incorrect data inside of Var: language")

def calculator_en():
    print("----------------------------------------------")
    print("Input your first number:")
    first_number = input()
    print("Input your second number:")
    second_number = input()
    print("Input your calculation type (+/-/*//)")
    calc_type = input()
#TODO: Complete calculator





# Startup
print("----------------------------------------------")
print("              Welcome to EtchOS               ")
print("----------------------------------------------")
print("Let's customize your experience. You can change it all in the Settings later.")
continue_onboarding = True
Language_En()
