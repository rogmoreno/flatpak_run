# actions/run_flatpak/run_flatpak.py
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GObject # Added Gio and GObject
import logging
import subprocess
from threading import Thread
import os # Added import for os

from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

logger = logging.getLogger(__name__)

def get_flatpak_apps() -> list[dict]:
    """
    Fetches the list of installed Flatpak applications.
    """
    apps = []
    try:
        command = ["flatpak-spawn", "--host", "sh", "-c", "cd ~ && flatpak list --app --columns=application,name"]
        logger.info(f"Current working directory before flatpak-spawn: {os.getcwd()}") # Added logging
        result = subprocess.run(command, capture_output=True, text=True, check=True, cwd="/")

        lines = result.stdout.strip().split('\n')
        start_index = 1 if lines and lines[0].lower().startswith('application') else 0

        for line in lines[start_index:]:
            parts = line.strip().split('\t', 1)
            if len(parts) == 2:
                app_id, app_name = parts
                apps.append({"id": app_id.strip(), "name": app_name.strip()})

        apps.sort(key=lambda x: x["name"])
        logger.info(f"Found {len(apps)} Flatpak applications.")
    except FileNotFoundError:
        logger.error("The 'flatpak' command was not found. Is Flatpak installed?")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error listing Flatpak applications: {e.stderr}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching Flatpak apps: {e}")
    
    return apps

def run_flatpak_app_async(app_id: str):
    """
    Runs a Flatpak application in a separate thread to avoid blocking
    the main StreamController process.
    """
    def target():
        logger.info(f"Attempting to run Flatpak application: {app_id}")
        try:
            subprocess.Popen(["flatpak-spawn", "--host", "sh", "-c", f"cd ~ && flatpak run {app_id}"],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             cwd="/")
            logger.info(f"Successfully launched Flatpak application: {app_id}")
        except FileNotFoundError:
            logger.error("The 'flatpak' command was not found while trying to run an app.")
        except Exception as e:
            logger.error(f"An error occurred while trying to run {app_id}: {e}")

    thread = Thread(target=target)
    thread.daemon = True
    thread.start()


from typing import Optional, Any

class RunFlatpak(ActionBase):
    def __init__(self, action_id: str, action_name: str, deck_controller: DeckController, page: Page, plugin_base: PluginBase, input_ident: Any, coords: Optional[str] = None, **kwargs):
        self.input_ident = input_ident # Store input_ident
        self.flatpak_apps = [] # Store the fetched apps
        if coords is None:
            coords = "" # Provide a default empty string if coords is not provided.
        # coords is a parameter for RunFlatpak, but not for ActionBase
        super().__init__(action_id=action_id, action_name=action_name, deck_controller=deck_controller, page=page, plugin_base=plugin_base, input_ident=input_ident, **kwargs)
        self.combo_row = None

    def on_key_down(self):
        settings = self.get_settings()
        app_id = settings.get("app_id")
        if app_id:
            try:
                run_flatpak_app_async(app_id)
            except Exception as e:
                logger.error(f"Failed to run app {app_id}: {e}")
                self.show_error()
        else:
            logger.warning("No app_id configured for this action.")
            self.show_error()

    def get_config_rows(self) -> list:
        """
        Builds the GTK configuration UI for the action.
        """
        self.model = Gtk.StringList.new([]) # Use Gtk.StringList for Adw.ComboRow

        self.combo_row = Adw.ComboRow(
            title="Application",
            subtitle="Select the Flatpak application to run",
            model=self.model # model is now Gtk.StringList, which is a GListModel
        )
        
        # We don't need a cell renderer with Gtk.StringList and Adw.ComboRow,
        # it displays the string directly. If we needed more complex display,
        # we'd use a Gtk.ListItemFactory and Gtk.DropDown.

        try:
            self.flatpak_apps = get_flatpak_apps()
            if self.flatpak_apps:
                for app in self.flatpak_apps:
                    self.model.append(app["name"]) # Append only the name
            else:
                self.combo_row.set_subtitle("No Flatpak applications found.")
                self.combo_row.set_sensitive(False)
        except Exception as e:
            logger.error(f"Failed to get app list: {e}")
            self.combo_row.set_subtitle("Error loading applications.")
            self.combo_row.set_sensitive(False)

        self.load_config_values()
        self.combo_row.connect("notify::selected-item", self.on_selection_changed)

        return [self.combo_row]

    def load_config_values(self):
        """
        Loads the saved app_id and sets the combo box selection.
        """
        settings = self.get_settings()
        saved_app_id = settings.get("app_id")

        if saved_app_id and self.flatpak_apps:
            for i, app in enumerate(self.flatpak_apps):
                if app["id"] == saved_app_id:
                    self.combo_row.set_selected(i)
                    break
        else:
            if len(self.flatpak_apps) > 0:
                self.combo_row.set_selected(0)

    def on_selection_changed(self, combo_row, _):
        """
        Saves the selected app_id when the user changes the dropdown.
        """
        selected_index = combo_row.get_selected()
        if selected_index >= 0 and self.flatpak_apps:
            app_id = self.flatpak_apps[selected_index]["id"] # Get app_id from stored list
            
            settings = self.get_settings()
            settings["app_id"] = app_id
            self.set_settings(settings)
            logger.info(f"Saved app_id: {app_id}")