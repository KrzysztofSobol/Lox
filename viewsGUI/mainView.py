import customtkinter as ctk
from containerService.container import Container

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Store controller reference
        self.websiteController = Container.getWebsiteController()
        self.credentialController = Container.getCredentialController()  # Add credential controller
        self.current_user_id = None  # Will be set when user logs in
        self.all_websites = []  # Store all websites for filtering
        self.selected_website_id = None  # Track currently selected website

        # Configure grid layout for the main screen
        # 2 columns: 20% left for list, 80% right for another list
        self.grid_columnconfigure(0, weight=1)  # Left column (20% width)
        self.grid_columnconfigure(1, weight=4)  # Right column (80% width)
        self.grid_rowconfigure(1, weight=1)  # Make main content row expandable

        # Left Side Column (20% width) - Previous implementation remains the same
        left_frame = ctk.CTkFrame(self)
        left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Top 5% of left column - Buttons
        left_top_frame = ctk.CTkFrame(left_frame, height=80)  # Increased height
        left_top_frame.pack(side="top", fill="x", padx=5, pady=5)

        # Configure the frame to distribute buttons evenly
        left_top_frame.grid_columnconfigure(0, weight=1)
        left_top_frame.grid_columnconfigure(1, weight=1)

        # Delete Button
        self.delete_button = ctk.CTkButton(
            left_top_frame,
            text="Delete",
            width=100,
            height=40  # Increased button height
        )
        self.delete_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Add Button
        self.add_button = ctk.CTkButton(
            left_top_frame,
            text="Add",
            width=100,
            height=40  # Increased button height
        )
        self.add_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Search input frame
        search_frame = ctk.CTkFrame(left_frame, height=50)
        search_frame.pack(fill="x", padx=5, pady=5)

        # Search Entry
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search websites...",
            width=250
        )
        self.search_entry.pack(expand=True, fill="x", padx=5, pady=5)

        # Bind the search entry to the search method
        self.search_entry.bind("<KeyRelease>", self.filter_websites)

        # Scrollable frame for website list
        self.website_list_frame = ctk.CTkScrollableFrame(left_frame)
        self.website_list_frame.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

        # Right Side Column (80% width)
        right_frame = ctk.CTkFrame(self)
        right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Scrollable frame for credentials list
        self.credentials_list_frame = ctk.CTkScrollableFrame(right_frame)
        self.credentials_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def load_websites(self, user_id):
        """
        Load websites for the given user and populate the website list
        """
        self.current_user_id = user_id

        # Clear existing websites
        for widget in self.website_list_frame.winfo_children():
            widget.destroy()

        # Fetch websites for the user
        self.all_websites = self.websiteController.get_user_websites(user_id)

        # Create a button for each website
        for website in self.all_websites:
            website_button = ctk.CTkButton(
                self.website_list_frame,
                text=website.name,
                anchor="w",
                width=250,
                command=lambda w=website: self.load_credentials(w.id)  # Add command to load credentials
            )
            website_button.pack(padx=5, pady=2, fill="x")

    def load_credentials(self, website_id):
        """
        Load credentials for a specific website
        """
        self.selected_website_id = website_id

        # Clear existing credentials
        for widget in self.credentials_list_frame.winfo_children():
            widget.destroy()

        # Fetch credentials for the selected website
        credentials = self.credentialController.getCredentialsByWebsite(website_id)

        # Create a container for each credential
        for credential in credentials:
            credential_frame = ctk.CTkFrame(self.credentials_list_frame)
            credential_frame.pack(padx=5, pady=5, fill="x")

            # Credential name label (for now, we'll just show the username)
            credential_label = ctk.CTkLabel(
                credential_frame,
                text=credential.username,
                anchor="w",
                width=250
            )
            credential_label.pack(padx=5, pady=2, fill="x")

    def filter_websites(self, event=None):
        """
        Filter websites based on search input
        """
        # Clear existing website buttons
        for widget in self.website_list_frame.winfo_children():
            widget.destroy()

        # Get search term
        search_term = self.search_entry.get().lower()

        # Filter websites
        filtered_websites = [
            website for website in self.all_websites
            if search_term in website.name.lower()
        ]

        # Create buttons for filtered websites
        for website in filtered_websites:
            website_button = ctk.CTkButton(
                self.website_list_frame,
                text=website.name,
                anchor="w",
                width=250,
                command=lambda w=website: self.load_credentials(w.id)  # Add command to load credentials
            )
            website_button.pack(padx=5, pady=2, fill="x")

    def refresh_website_list(self):
        """
        Refresh the website list if a user is logged in
        """
        if self.current_user_id:
            self.load_websites(self.current_user_id)
            # Clear search entry
            self.search_entry.delete(0, 'end')

            # Also clear credentials list
            for widget in self.credentials_list_frame.winfo_children():
                widget.destroy()