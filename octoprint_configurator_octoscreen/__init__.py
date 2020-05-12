# coding=utf-8
from __future__ import absolute_import

# import logging
import octoprint.plugin
import flask
import socket

from octoprint.events import Events
from octoprint_configurator_octoscreen.notifications import Notifications
from octoprint_configurator_octoscreen.settings import OctoScreenSettings


class OctoScreenPlugin(octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.EventHandlerPlugin,
                    octoprint.plugin.TemplatePlugin,
                    octoprint.plugin.AssetPlugin,
                    octoprint.plugin.SimpleApiPlugin,
                    octoprint.plugin.StartupPlugin):

    def initialize(self):
        Notifications.initialize(self._plugin_manager)
        self.Settings = OctoScreenSettings(self._settings)


    def get_assets(self):
        return dict(
            less=['less/theme.less'],
            js=['js/octoscreen.js'],
            css=['css/main.css', 'css/theme.css']
        )

    def get_settings_defaults(self):
         return OctoScreenSettings.default_settings()

    def get_template_vars(self):
        return OctoScreenSettings.template_vars()

    def get_api_commands(self):
        return dict(
            get_notification=[],
            get_settings=[]
        )

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

    def on_api_command(self, command, data):
        if command == "get_notification":
            return flask.jsonify(message = Notifications.get_message_to_display())
        elif command == "get_settings":
            return flask.jsonify(self.Settings.get_all())

    def on_api_get(self, request):
        return flask.jsonify(printer_name="test2")


    def get_template_configs(self):
        return [
            dict(type="settings", name="Configurateur OctoScreen", custom_bindings=False),
        ]


    ##~~ Softwareupdate hook
    def get_update_information(self):
        return dict(
        configurator_octoscreen=dict(
            displayName = "Configurateur OctoScreen",
            displayVersion = self._plugin_version,

            type="github_release",
            user="CyrilleSouchet",
            repo="OctoPrint-Configurateur-OctoScreen",
            current=self._plugin_version,

            pip="https://github.com/CyrilleSouchet/OctoPrint-Configurateur-OctoScreen/archive/{target_version}.zip"
            )
        )


__plugin_name__ = "Configurateur OctoScreen"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = OctoScreenPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
