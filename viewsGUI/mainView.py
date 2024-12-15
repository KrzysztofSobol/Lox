import tkinter as tk
import customtkinter as ctk
import pyperclip

from containerService.container import Container


class WebsiteWidget(ctk.CTkFrame):
    def __init__(self, parent, website, on_click_callback, on_delete_callback, delete_mode=False, initially_deleted=False):
        super().__init__(parent)
        self.website = website
        self.on_delete_callback = on_delete_callback
        self.website_id = website.id

        # Configure layout
        self.pack(padx=10, pady=2, fill="x")

        # Website button
        self.website_button = ctk.CTkButton(
            self,
            text=website.name,
            anchor="w",
            height=40,
            font=("", 14),
            command=lambda: on_click_callback(website.id)
        )
        self.website_button.pack(side="left", expand=True, fill="x")

        # Delete switch
        self.delete_switch = ctk.CTkSwitch(self, text="")
        self.delete_switch.configure(command=self._toggle_delete)

        # Manage delete mode and initial deletion state
        self._is_delete_mode = delete_mode
        self._initially_deleted = initially_deleted

        # Initialize switch based on delete mode and initial state
        if delete_mode:
            self.delete_switch.pack(side="right", expand=True)
            if initially_deleted:
                self.delete_switch.select()
            else:
                self.delete_switch.deselect()

    def _toggle_delete(self):
        if self._is_delete_mode:
            self.on_delete_callback(self.website)

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.websites_to_delete = []
        self.controller = controller  # Store controller reference
        self.websiteController = Container.getWebsiteController()
        self.credentialController = Container.getCredentialController()  # Add credential controller
        self.current_user_id = None  # Will be set when user logs in
        self.all_websites = []  # Store all websites for filtering
        self.selected_website_id = None  # Track currently selected website
        self.deleted_website_ids = set()

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
            width=120,  # Increased from 100
            height=50  # Increased from 40
        )
        self.delete_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Add Button
        self.add_button = ctk.CTkButton(
            left_top_frame,
            text="Add",
            width=120,  # Increased from 100
            height=50  # Increased from 40
        )
        self.add_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Search input frame
        search_frame = ctk.CTkFrame(left_frame, height=70)
        search_frame.pack(fill="x", padx=5, pady=5)

        # Search Entry
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search websites...",
            width=250,  # Increased from 250
            font=("", 14)  # Added font size
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
        self.current_user_id = user_id
        self.websites_to_delete = []  # Reset websites selected for deletion

        # Clear existing website widgets
        for widget in self.website_list_frame.winfo_children():
            widget.destroy()

        # Fetch websites for the user
        self.all_websites = self.websiteController.get_user_websites(user_id)

        # Create WebsiteWidgets for all websites
        for website in self.all_websites:
            WebsiteWidget(
                self.website_list_frame,
                website,
                self.load_credentials,
                self.toggle_website_deletion,
                delete_mode=False,  # Default to not showing switches at creation
                initially_deleted=website.id in self.deleted_website_ids
            )

        # Reset delete button state
        self.delete_button.configure(
            command=self.toggle_delete_mode,
            text="Delete Websites"
        )

    def toggle_delete_mode(self):
        delete_mode = self.delete_button.cget("text") == "Delete Websites"

        if delete_mode:
            # Enter delete mode
            self.delete_button.configure(text="I'm Sure, Delete")
            self.websites_to_delete = []  # Reset websites to delete

            # Enable delete mode for all widgets
            for container in self.website_list_frame.winfo_children():
                if isinstance(container, WebsiteWidget):
                    container._is_delete_mode = True
                    container.delete_switch.pack(side="right", padx=5)
                    # Apply the previously selected state (if any)
                    if container.website_id in self.deleted_website_ids:
                        container.delete_switch.select()
                    else:
                        container.delete_switch.deselect()
        else:
            # Exit delete mode
            self.delete_button.configure(text="Delete Websites")

            if self.websites_to_delete:
                # Perform deletion
                for website_id in self.websites_to_delete:
                    self.websiteController.delete_website(website_id)

                # Refresh the list after deletion
                self.refresh_website_list()

                # Reset delete state
                self.deleted_website_ids.clear()
                self.websites_to_delete.clear()
            else:
                # Just hide delete switches if no websites selected
                for container in self.website_list_frame.winfo_children():
                    if isinstance(container, WebsiteWidget):
                        container._is_delete_mode = False
                        container.delete_switch.pack_forget()

    def toggle_website_deletion(self, website):
        """
        Track websites selected for deletion
        """
        if website.id in self.deleted_website_ids:
            self.deleted_website_ids.remove(website.id)
            if website.id in self.websites_to_delete:
                self.websites_to_delete.remove(website.id)
        else:
            self.deleted_website_ids.add(website.id)
            if website.id not in self.websites_to_delete:
                self.websites_to_delete.append(website.id)

    def load_credentials(self, website_id):
        """
        Load credentials for a specific website with edit functionality
        """
        self.selected_website_id = website_id

        # Clear existing credentials
        for widget in self.credentials_list_frame.winfo_children():
            widget.destroy()

        # Fetch credentials for the selected website
        credentials = self.credentialController.getCredentialsByWebsite(website_id)

        if not credentials:
            # If no credentials are found, display a message
            no_credentials_label = ctk.CTkLabel(
                self.credentials_list_frame,
                text="No credentials found for this website",
                font=("", 16),
                text_color="red"
            )
            no_credentials_label.pack(padx=10, pady=20)
        else:
            # If credentials exist, load and display them
            for credential in credentials:
                credential_frame = ctk.CTkFrame(self.credentials_list_frame)
                credential_frame.pack(padx=5, pady=5, fill="x")

                # Credential header (link, edit, delete)
                header_frame = ctk.CTkFrame(credential_frame, fg_color="#2c2c2c")
                header_frame.pack(fill="x", padx=5, pady=2)

                # Credential link
                credential_link = ctk.CTkLabel(
                    header_frame,
                    text=credential.saved_link,
                    anchor="w",
                    width=250,
                    fg_color="transparent",
                    text_color="#00b8d9",
                    cursor="hand2",
                    font=("", 14)
                )
                credential_link.pack(side="left", padx=5, pady=2)
                credential_link.bind("<Button-1>", lambda event, url=credential.saved_link: self.open_url(url))

                # Credential details (login, password)
                details_frame = ctk.CTkFrame(credential_frame, bg_color="#2c2c2c", fg_color="#2c2c2c")
                details_frame.pack(fill="x", padx=5, pady=2)

                delete_button = ctk.CTkButton(
                    header_frame,
                    text="Delete",
                    width=100,
                    height=40,
                    fg_color="#00b8d9",
                    hover_color="#007d8c",
                    font=("", 14),
                    command=lambda cred_id=credential.id, frame=details_frame:
                    self.handle_delete_button(cred_id, frame)
                )
                delete_button.pack(side="right", padx=5, pady=2)

                # Edit button
                edit_button = ctk.CTkButton(
                    header_frame,
                    text="Edit",
                    width=100,
                    height=40,
                    fg_color="#00b8d9",
                    hover_color="#007d8c",
                    font=("", 14)
                )
                edit_button.pack(side="right", padx=5, pady=2)

                # Login section
                login_label = ctk.CTkLabel(details_frame, text="Login:", font=("", 14), anchor="w", bg_color="#2c2c2c",
                                           text_color="#00b8d9")
                login_label.pack(side="left", padx=5, pady=2)

                login_text = ctk.CTkEntry(details_frame, placeholder_text=credential.username, font=("", 14),
                                          state="normal")
                login_text.configure(state="disabled")
                login_text.pack(side="left", padx=5, pady=2)

                copy_icon = tk.PhotoImage(file="viewsGUI/icons/copy.png").subsample(21, 21)

                login_copy_button = ctk.CTkButton(
                    details_frame,
                    text="Copy",
                    width=80,
                    height=40,
                    font=("", 14),
                    fg_color="#3b3b3b",
                    bg_color="#2c2c2c",
                    hover_color="#007d8c",
                    image=copy_icon,
                    command=lambda: pyperclip.copy(credential.username)
                )
                login_copy_button.pack(side="left", padx=5, pady=2)

                # Password section
                details_frame2 = ctk.CTkFrame(credential_frame, bg_color="#2c2c2c", fg_color="#2c2c2c")
                details_frame2.pack(fill="x", padx=5, pady=2)

                password_label = ctk.CTkLabel(details_frame2, text="Password:", font=("", 14), anchor="w",
                                              bg_color="#2c2c2c", text_color="#00b8d9")
                password_label.pack(side="left", padx=5, pady=2)

                password_text = ctk.CTkEntry(details_frame2, placeholder_text=credential.password, font=("", 14),
                                             state="normal")
                password_text.configure(state="disabled")
                password_text.pack(side="left", padx=5, pady=2)

                password_copy_button = ctk.CTkButton(
                    details_frame2,
                    text="Copy",
                    width=80,
                    height=40,
                    font=("", 14),
                    fg_color="#3b3b3b",
                    bg_color="#2c2c2c",
                    hover_color="#007d8c",
                    image=copy_icon,
                    command=lambda: pyperclip.copy(credential.password)
                )
                password_copy_button.pack(side="left", padx=5, pady=2)

                # Edit functionality
                def toggle_edit(cred_id, login_entry, password_entry, edit_btn):
                    if edit_btn.cget("text") == "Edit":
                        # Switch to edit mode
                        login_entry.configure(state="normal")
                        password_entry.configure(state="normal")

                        # Clear any existing text and insert current credential values
                        login_entry.delete(0, 'end')
                        login_entry.insert(0, credential.username)

                        password_entry.delete(0, 'end')
                        password_entry.insert(0, credential.password)

                        edit_btn.configure(text="Save")
                    else:
                        # Save changes
                        new_username = login_entry.get() or credential.username
                        new_password = password_entry.get() or credential.password

                        # Call edit method
                        success = self.credentialController.edit(cred_id, new_username, new_password)

                        if success:
                            # Reload credentials to reflect changes
                            self.load_credentials(website_id)
                        else:
                            # Optionally handle edit failure (show error message)
                            print("Failed to update credential")

                # Bind edit button to toggle function
                edit_button.configure(
                    command=lambda btn=edit_button, login=login_text,
                                   pwd=password_text, cred_id=credential.id:
                    toggle_edit(cred_id, login, pwd, btn)
                )

    def filter_websites(self, event=None):
        """
        Filter websites based on search input while preserving delete mode and switch states
        """
        # Clear existing website widgets
        for widget in self.website_list_frame.winfo_children():
            widget.destroy()

        # Get the search term
        search_term = self.search_entry.get().lower()

        # Filter websites based on the search term
        filtered_websites = [
            website for website in self.all_websites
            if search_term in website.name.lower()
        ]

        # Determine if we are currently in delete mode
        delete_mode = self.delete_button.cget("text") == "I'm Sure, Delete"

        # Recreate widgets for the filtered websites
        for website in filtered_websites:
            WebsiteWidget(
                self.website_list_frame,
                website,
                self.load_credentials,
                self.toggle_website_deletion,
                delete_mode=delete_mode,
                # Initialize switch state based on `self.deleted_website_ids`
                initially_deleted=website.id in self.deleted_website_ids
            )

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

    def show_delete_confirmation(self, credential_id, delete_frame):
        # Create a confirmation button
        self.sure_delete_button = ctk.CTkButton(
            delete_frame,
            text="Sure?",
            width=100,
            height=40,
            fg_color="#FF4500",  # Bright red to indicate danger
            hover_color="#FF6347",
            font=("", 14),
            command=lambda: self.confirm_delete(credential_id, delete_frame)
        )
        self.sure_delete_button.pack(side="right", padx=5, pady=2)

    def confirm_delete(self, credential_id, delete_frame):
        # Perform the actual deletion
        success = self.credentialController.delete(credential_id)

        if success:
            # If deletion successful, reload credentials and remove confirmation button
            if self.selected_website_id:
                self.load_credentials(self.selected_website_id)
            # Optionally, you can add a success message or toast notification

    def handle_delete_button(self, credential_id, delete_frame):
        # Check if the sure button is already present
        sure_button_exists = any(
            isinstance(child, ctk.CTkButton) and child.cget("text") == "Sure?"
            for child in delete_frame.winfo_children()
        )

        if not sure_button_exists:
            # If no sure button, show confirmation
            self.show_delete_confirmation(credential_id, delete_frame)
        else:
            # If sure button exists, remove it (cancel delete)
            for child in delete_frame.winfo_children():
                if isinstance(child, ctk.CTkButton) and child.cget("text") == "Sure?":
                    child.destroy()