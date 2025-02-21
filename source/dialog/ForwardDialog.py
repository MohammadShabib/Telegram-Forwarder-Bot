from source.dialog.BaseDialog import BaseDialog
from source.model.ForwardConfig import ForwardConfig

class ForwardDialog(BaseDialog):
    async def get_config(self):
        """Get forward configuration from user.
        
        Returns:
            Dict mapping source chat IDs to their forward configurations
        """
        self.clear()
        return await self._get_forward_config()

    async def _get_forward_config(self):
        """Get forward configuration settings.
        
        Returns:
            Dict mapping source chat IDs to their forward configurations
        """
        forward_config_list = await ForwardConfig.get_all(True)
        config_string = '\n   '.join(str(config) for config in forward_config_list)
        
        options = [
            {"name": "Use saved settings.\n   " + config_string, "value": "1"},
            {"name": "New settings", "value": "2"}
        ]

        choice = await self.show_options("Forward Settings:", options)
        if choice == "2":
            forward_config_list = await ForwardConfig.get_all(False)
        
        return {item.sourceID: item for item in forward_config_list} 