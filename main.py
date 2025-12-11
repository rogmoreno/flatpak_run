# main.py
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from .actions.run_flatpak.run_flatpak import RunFlatpak

class FlatpakRunPlugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.lm = self.locale_manager

        # --- Register Action ---
        self.run_flatpak_action_holder = ActionHolder(
            plugin_base=self,
            action_base=RunFlatpak,
            action_id="com.rogmoreno.flatpak_run.run",
            action_name=self.lm.get("actions.flatpak.name"),
        )
        self.add_action_holder(self.run_flatpak_action_holder)

        # --- Register Plugin ---
        self.register(
            plugin_name=self.lm.get("plugin.name"),
            github_repo="https://github.com/rogmoreno/flatpak_run.git",
            plugin_version="1.0.0",
            app_version="1.1.1-alpha",
        )
