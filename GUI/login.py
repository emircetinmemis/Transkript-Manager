from    Utilities       import  get_gif_frame_count, authenticate, validate_transcript # -> Utilitiy functions
from    Utilities       import  OfflineParser, OnlineParser # -> Utilitiy classes
from    PIL             import  Image, ImageTk # -> Image processing
from    tkinter         import  PhotoImage # -> Image processing
from    tkinter         import  filedialog # -> Ask file path
from    Environment     import  ASSETS_DC # -> Environment variables
#from    tkinter         import  ttk # -> GUI
import  customtkinter   as      ctk # -> GUI
#import  tkinter         as      tk # -> GUI
import  os # -> Get current working directory
import  time # -> Simulate a long process
import  threading # -> Split long processes into threads

class LoginFrame(ctk.CTkFrame) :

    # Data Fields
    mef_uni_logo_size  = (216, 140)
    gif_size           = (50, 50)

    def __init__(self, parent : ctk.CTkFrame, root : ctk.CTk, DEBUG : bool = False, *args, **kwargs) -> None:
        """
        Constructor method for LoginFrame class. Used to initialize main window of the login.
        @Parameters:
            parent - Required : Container frame of the login. (ttk.Frame) -> Which is used to place the login frame.
            root   - Required : Root window of the login. (tk.Tk) -> Which is used to set connection between frames.
            DEBUG  - Optional : Debug mode flag. (bool) (default : False) -> Which is used to determine whether the login is in debug mode or not.
        @Returns:
            None
        """
        # Initialize main frame
        super().__init__(parent, *args, **kwargs)

        # Initialize variables
        self.parent = parent
        self.root   = root
        self.DEBUG  = DEBUG
        self.username = ctk.StringVar(value=None)
        self.password = ctk.StringVar(value=None)
        self.path_to_transcript = ctk.StringVar(value=None)
        self.name_of_transcript = ctk.StringVar(value=None)
        self.execution_mode = ctk.StringVar(value="online")
        self.work_dir = os.getcwd()
        self.desktop_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

        # Initialize widget containers.
        self.__load_containers()

        # # Load widgets.
        self.__load_mef_label()
        self.__load_online_login()
        self.__load_output()

    def __load_containers(self) -> None:
        """
        Method to load the main containers.
        @Parameters:
            None
        @Returns:
            None
        """
        # Create the main container.
        self.container = ctk.CTkFrame(self, fg_color=self.root.light_background, bg_color=self.root.dark_background, corner_radius=25)
        self.container.grid(row=0, column=0)
        # Configure the main container.
        self.container.grid_rowconfigure((0,1,2), weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create the sub containers.
        self.mef_label_container = ctk.CTkFrame(self.container)
        self.mef_label_container.grid(row=0, column=0)

        self.online_login_container = ctk.CTkFrame(self.container)
        self.online_login_container.grid(row=1, column=0)

        self.offline_login_container = ctk.CTkFrame(self.container)
        self.offline_login_container.grid(row=1, column=0)

        self.output_container = ctk.CTkFrame(self.container)
        self.output_container.grid(row=2, column=0)

        # Iterate over containers, and configure them.
        for container in self.container.winfo_children() :
            container.configure(fg_color=self.root.light_background)
            container.grid_configure(padx=self.root.general_padding, pady=self.root.general_padding, sticky="nsew")

        # Remove the containers that shouldn't be visible at the beginning.
        self.offline_login_container.grid_remove()
        self.output_container.grid_remove()

    def __load_mef_label(self) -> None:
        """
        Method to load the mef label.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure the mef label container.
        self.mef_label_container.grid_rowconfigure(0, weight=1)
        self.mef_label_container.grid_columnconfigure(0, weight=1)

        # Load the mef label.
        self.mef_logo_image = ctk.CTkImage(dark_image=Image.open(ASSETS_DC.LOGO_PATH), light_image=Image.open(ASSETS_DC.LOGO_PATH), size=self.mef_uni_logo_size)
        self.mef_logo_label = ctk.CTkLabel(self.mef_label_container, image=self.mef_logo_image, text=None, anchor="center")
        self.mef_logo_label.grid(row=0, column=0, sticky="nsew")

    def __load_online_login(self) -> None:
        """
        Method to load the online login widgets and wires logic.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure the online login container.
        self.online_login_container.grid_rowconfigure((0,1,3,4,5), weight=1)
        self.online_login_container.grid_columnconfigure((0), weight=1)

        """
        self.root.button_light_blue
        self.root.button_light_green
        self.root.inner_padding
        """

        # Create the online login widgets.
        self.online_login_label_button = ctk.CTkButton(self.online_login_container, text="Online Login", command=self.__switch_login_mode, 
                                                       fg_color=self.root.button_light_blue, 
                                                       hover_color=self.root.button_light_blue_hover, 
                                                       border_color=self.root.light_background, 
                                                       bg_color=self.root.light_background, 
                                                       corner_radius=50,
                                                       text_color="white",
                                                       text_color_disabled="gray",
                                                       font=("Arial", 14, "bold")
        )
        self.online_login_label_button.grid(row=0, column=0)

        self.online_login_username_label = ctk.CTkLabel(self.online_login_container, text="Username",
                                                        fg_color=self.root.light_background,
                                                        bg_color=self.root.light_background,
                                                        text_color=self.root.secondary_dark_background,
                                                        font=("Arial", 12, "bold")
        )
        self.online_login_username_label.grid(row=1, column=0, sticky="w", padx=15)
        self.online_login_username_entry = ctk.CTkEntry(self.online_login_container, textvariable=self.username,
                                                        fg_color=self.root.entry_light_background,
                                                        bg_color=self.root.light_background,
                                                        border_color=self.root.secondary_dark_background,
                                                        placeholder_text="username",
                                                        placeholder_text_color="gray",
                                                        text_color=self.root.dark_background,
                                                        font=("Arial", 12, "bold")
        )
        self.online_login_username_entry.grid(row=2, column=0, sticky="we", padx=15)
        
        self.online_login_password_label = ctk.CTkLabel(self.online_login_container, text="Password",
                                                        fg_color=self.root.light_background,
                                                        bg_color=self.root.light_background,
                                                        text_color=self.root.secondary_dark_background,
                                                        font=("Arial", 12, "bold")
        )
        self.online_login_password_label.grid(row=3, column=0, sticky="w", padx=15)
        self.online_login_password_entry = ctk.CTkEntry(self.online_login_container, textvariable=self.password, show="*",
                                                        fg_color=self.root.entry_light_background,
                                                        bg_color=self.root.light_background,
                                                        border_color=self.root.secondary_dark_background,
                                                        placeholder_text="password",
                                                        placeholder_text_color="gray",
                                                        text_color=self.root.dark_background,
                                                        font=("Arial", 12, "bold")
        )
        self.online_login_password_entry.grid(row=4, column=0, sticky="we", padx=15)

        self.online_login_button = ctk.CTkButton(self.online_login_container, text="Login", command=self.__handle_login, 
                                                 fg_color=self.root.button_light_green, 
                                                 hover_color=self.root.button_light_green_hover, 
                                                 border_color=self.root.light_background, 
                                                 bg_color=self.root.light_background, 
                                                 corner_radius=50,
                                                 text_color="white",
                                                 text_color_disabled="gray",
                                                 font=("Arial", 14, "bold")
        )
        self.online_login_button.grid(row=5, column=0, pady=12)

    def __load_offline_login(self) -> None:
        """
        Method to load the offline login widgets and wires logic.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure the offline login container.
        self.offline_login_container.grid_rowconfigure((0,1,2), weight=1)
        self.offline_login_container.grid_columnconfigure(0, weight=1)

        # Create the offline login widgets.
        self.offline_login_label_button = ctk.CTkButton(self.offline_login_container, text="Offline Login", command=self.__switch_login_mode,
                                                        fg_color=self.root.button_light_blue, 
                                                        hover_color=self.root.button_light_blue_hover, 
                                                        border_color=self.root.light_background, 
                                                        bg_color=self.root.light_background, 
                                                        corner_radius=50,
                                                        text_color="white",
                                                        text_color_disabled="gray",
                                                        font=("Arial", 14, "bold")
        )
        self.offline_login_label_button.grid(row=0, column=0, pady=12)

        self.offline_open_file_button = ctk.CTkButton(self.offline_login_container, text=self.name_of_transcript.get() or "Select Transcript", command=self.__handle_ask_file_dialog,
                                                      fg_color=self.root.dark_background,
                                                      hover_color=self.root.secondary_dark_background,
                                                      border_color=self.root.light_background,
                                                      bg_color=self.root.light_background,
                                                      corner_radius=50,
                                                      text_color="white",
                                                      text_color_disabled="gray",
                                                      font=("Arial", 14, "bold")
        )
        self.offline_open_file_button.grid(row=1, column=0, pady=12)

        self.offline_login_button = ctk.CTkButton(self.offline_login_container, text="Login", command=self.__handle_login, 
                                                  fg_color=self.root.button_light_green, 
                                                  hover_color=self.root.button_light_green_hover, 
                                                  border_color=self.root.light_background, 
                                                  bg_color=self.root.light_background, 
                                                  corner_radius=50,
                                                  text_color="white",
                                                  text_color_disabled="gray",
                                                  font=("Arial", 14, "bold")
        )
        self.offline_login_button.grid(row=2, column=0, pady=12)

    def __load_output(self) -> None:
        """
        Method to load the output widgets. Used for gif animation
        @Parameters:
            None
        @Returns:
            None
        """
        # Get the number of frames in the gif file.
        self.gif_frame_count = get_gif_frame_count(ASSETS_DC.LOADING_ANIMATION_PATH)

        # Load each embeddable frame of the gif.
        #self.gif_frames = [ctk.CTkImage(file=ASSETS_DC.LOADING_ANIMATION_PATH, format = 'gif -index %i' %(i)) for i in range(self.gif_frame_count)]
        self.gif_frames = []
        for frame in range(self.gif_frame_count):
            
            current_pil_image = Image.open(ASSETS_DC.LOADING_ANIMATION_PATH)
            current_pil_image.seek(frame)
            
            current_gif_object = ctk.CTkImage(light_image=current_pil_image, dark_image=current_pil_image, size=self.gif_size)
            self.gif_frames.append(current_gif_object)

        # Configure the output container.
        self.output_container.grid_rowconfigure(0, weight=1)
        self.output_container.grid_columnconfigure(0, weight=1)

        # Create the output widget.
        self.output_loading_label = ctk.CTkLabel(self.output_container, text=None)
        self.output_loading_label.grid(row=0, column=0, sticky="nsew")



    def __handle_ask_file_dialog(self, *args, **kwargs) -> None:
        """
        Method to handle the ask file dialog.
        @Parameters:
            None
        @Returns:
            None
        """

        # Disable the buttons to prevent multiple file selection.
        self.offline_open_file_button.configure(state="disabled", text="Processing")

        # DEBUG MODE NO COMMENT
        if not self.DEBUG :
            input_file_path = filedialog.askopenfile(initialdir = self.work_dir, title = "Select Transcript", filetypes = [('pdf files only', '*.pdf')])
        else :
            input_file_path = filedialog.askopenfile(initialdir = self.desktop_path, title = "Select Transcript", filetypes = [('pdf files only', '*.pdf')])

        # Set literal for user interraction
        file_selected = False

        # Check if the file is selected.
        if input_file_path is not None and input_file_path != "" and input_file_path != " " :
            # Set the path to transcript and name of transcript.
            self.path_to_transcript.set(input_file_path.name)
            self.name_of_transcript.set(os.path.basename(input_file_path.name))
            # Update statement
            file_selected = True

        # Fix the buttons. So, user can try again.
        if not file_selected :
            self.offline_open_file_button.configure(text="No File Selected", fg_color=self.root.button_light_red, text_color_disabled="white")
            self.after(500, lambda : self.offline_open_file_button.configure(state="normal", text=self.name_of_transcript.get() or "Select Transcript", fg_color=self.root.dark_background, text_color_disabled="gray"))
        else :
            self.offline_open_file_button.configure(state="normal", text=self.name_of_transcript.get() or "Select Transcript")

    def __handle_login(self, *args, **kwargs) -> None:
        """
        Method to handle the login process.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check the execution mode. (online or offline) Than, get the correctness of the login parameters. Also disable buttons to prevent multiple login attempts.
        if self.execution_mode.get() == "online" :
            self.online_login_button.configure(state="disabled", text="Processing")
            self.online_login_label_button.configure(state="disabled")
            self.online_login_username_entry.configure(state="disabled")
            self.online_login_password_entry.configure(state="disabled")
            if (self.username.get() is None or self.username.get() == "" or self.username.get() == " ") or (self.password.get() is None or self.password.get() == "" or self.password.get() == " ") :
                isAllowed = False
            else :            
                isAllowed = authenticate(username=self.username.get(), password=self.password.get())
        elif self.execution_mode.get() == "offline" :
            self.offline_login_button.configure(state="disabled", text="Processing")
            self.offline_open_file_button.configure(state="disabled")
            self.offline_login_label_button.configure(state="disabled")
            if self.path_to_transcript.get() is None or self.path_to_transcript.get() == "" or self.path_to_transcript.get() == " " :
                isAllowed = False
            else :
                isAllowed = validate_transcript(self.path_to_transcript.get())
        else :
            raise ValueError("Invalid Execution Mode")

        # If the login parameters are correct, start the loading animation and load the thread.
        if isAllowed :
            self.__start_loading_animation()
            self.__load_thread()
        else :
            # If the login parameters are incorrect, show the error message and fix the buttons. So, user can try again. Use after to show animation effect on buttons.
            if self.execution_mode.get() == "online" :
                self.online_login_username_entry.configure(state="normal")
                self.online_login_password_entry.configure(state="normal")
                self.online_login_button.configure(text="Wrong Credentials", fg_color=self.root.button_light_red, text_color_disabled="white")
                self.after(500, lambda : self.online_login_button.configure(state="normal", text="Login", fg_color=self.root.button_light_green, text_color_disabled="gray"))
                self.after(500, lambda : self.online_login_label_button.configure(state="normal"))
            elif self.execution_mode.get() == "offline" :
                self.offline_open_file_button.configure(state="normal")
                self.offline_login_button.configure(text="Invalid Transcript", fg_color=self.root.button_light_red, text_color_disabled="white")
                self.after(500, lambda : self.offline_login_button.configure(state="normal", text="Login", fg_color=self.root.button_light_green, text_color_disabled="gray"))
                self.after(500, lambda : self.offline_login_label_button.configure(state="normal"))
            else :
                raise ValueError("Invalid Execution Mode")



    def __load_thread(self) -> None:
        """
        Method to load the thread for the login process.
        @Parameters:
            None
        @Returns:
            None
        """
        def start_parse() -> None:
            """
            Method to start the parsing process on core thread.
            @Parameters:
                None
            @Returns:
                None
            """
            # Create parser object according to the execution mode.
            if self.execution_mode.get() == "online" :
                parser = OnlineParser(username=self.username.get(), password=self.password.get())
            elif self.execution_mode.get() == "offline" :
                parser = OfflineParser(path_to_file=self.path_to_transcript.get())
                if not self.DEBUG :
                    time.sleep(2.3) # Simulate a long process by fake sleeping for 3 seconds.
                else :
                    pass

            # Parse the transcript.
            data = parser.get_transcript_data()

            # Create user info and user data documents.
            user_info_document, user_data_document = self.root.db_client.documentisize(data)
            
            # Uncomment the following lines if you want to push the data to the database at each login. (Not recommended) (INIT PUSH)
            #self.root.db_client.user_info.push_init(user_info_document)
            #self.root.db_client.user_data.push_init(user_data_document)

            # Set the current data to the root.
            self.root.set_current_data(user_info_document, user_data_document)

            # Set the authentication status to the root.
            is_user_authenticated = user_data_document["parsing_type"] != "offline"
            self.root.set_authication_status(is_user_authenticated)

        # Load the thread.
        self.thread = threading.Thread(target=start_parse, daemon=True)
        # Start the thread.
        self.thread.start()

    def __switch_login_mode(self, *args, **kwargs) -> None:
        """
        Method to switch the login mode.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check the execution mode and switch it. Apply remove and grid methods to the containers. than, load the login containers back.
        if self.execution_mode.get() == "online" :
            self.execution_mode.set("offline")
            self.online_login_container.grid_remove()
            self.offline_login_container.grid(row=1, column=0)
            self.__load_offline_login()
        else :
            self.execution_mode.set("online")
            self.offline_login_container.grid_remove()
            self.online_login_container.grid(row=1, column=0)
            self.__load_online_login()


    def __start_loading_animation(self) -> None:
        """
        Method to start the loading animation.
        @Parameters:
            None
        @Returns:
            None
        """
        # Grid the container.
        self.output_container.grid(row=2, column=0)

        # Initialize the animation.
        self.animation_id = self.root.after(0, self.__animate_loading, 0)

    def __animate_loading(self, frame_index : int) -> None:
        """
        Method to animate the loading gif.
        @Parameters:
            frame_index - Required : Index of the frame to be displayed. (int) -> Which is used to get the frame from the frames list.
        @Returns:
            None
        """
        # Check if the thread is alive. Than stop the program.
        if not self.thread.is_alive() :
            self.root.after(0, self.__stop_loading_animation)
            return

        # Check if the frame index is equal to the frame count. Than reset the frame index.
        if frame_index == self.gif_frame_count :
            frame_index = 0
        
        # Set the current frame.
        self.current_frame = self.gif_frames[frame_index]
        self.output_loading_label.configure(image=self.current_frame)

        # Animate the next frame.
        self.animation_id = self.root.after(20, self.__animate_loading, frame_index + 1)
        
    def __stop_loading_animation(self) -> None:
        """
        Method to stop the loading animation.
        @Parameters:
            None
        @Returns:
            None
        """
        # Cancel the animation.
        self.root.after_cancel(self.animation_id)
        self.output_container.grid_remove()

        # Switch to the application.
        self.root._switch_to_application()