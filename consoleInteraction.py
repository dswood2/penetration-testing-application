import nmap
import sqlmap
import md5PasswordCracker
import updatingEtcHosts
import PivotingWebsite
import bashforNetcat
import threading

print("Welcome to Pen Test Supreme!")

while True:
    print("Choose an option:")
    print("1 - Run Nmap scan")
    print("2 - Run sqlmap on target website") 
    print("3 - Crack MD5 hashes")
    print("4 - Update /etc/hosts file")
    print("5 - Run netcat")
    print("6 - Hack GoodGames. BEFORE selecting this choice you must select 5 first"
          "\n    then enter n for the manual netcat and then select this option")
    print("7 - Quit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        ip = input("\nPlease enter an IP address to scan (i.e 10.10.11.130): ")
        if ip == '':
            print("\nNo input detected running scan on default IP address \nIP = HTB machine(10.10.11.130)\n")
            nmap.run()
        else:
            nmap.run(ip)        
            
    elif choice == "2":
        entries = sqlmap.main()
        username = input("Select a username from above: ")  
        email = ""
        password = ""
        for entry in entries:
            if entry['Name'] == username:
                password = entry['Password']
                email = entry['Email']

        print(f"Email: {email}")       
        print(f"username: {username}") 
        print(f"Password: {password}")
    elif choice == "3":
        hashedPassword = input("\nPlease input a md5 hashed password and I will try to crack it: ")
        crackedPassword = md5PasswordCracker.crack_hash(hashedPassword)
        if crackedPassword == None:
            print("\nI was unable to crack the password. Recheck that the password is md5 hashed"
                  "\nor updated your words list.\n")
        else:
            print(f"\nYour plain text password is {crackedPassword}\n")
        
    elif choice == "4":
        updatingEtcHosts.disclaimer()
        updatingEtcHosts.run_with_elevated_privileges()
    elif choice == "5":
        print("You will need to start the netcat listener before"
              "\nexecuting any type of XSS that would create a reverse"
              "\nconnection. Start this then do the injection and then"
              "\nyou should be able to communicate in the window\n")
        manualOrNot = input("Do you want the manual necat listner: ")
        if manualOrNot == 'y':
            bashforNetcat.manual_netcat_listener()
        else:
            print("Starting netcat...")
            netcat_thread = threading.Thread(target=bashforNetcat.main)
            netcat_thread.start()
            print("Netcat listening...")
    elif choice == "6":
        print("Now pivoting web app...")
        PivotingWebsite.main()
        
    elif choice == "7":
        print("Exiting...") 
        break
    
    else:
        print("Invalid choice. Please enter a number between 1-5")
