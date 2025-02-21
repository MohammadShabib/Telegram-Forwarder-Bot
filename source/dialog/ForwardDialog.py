from source.dialog.BaseDialog import BaseDialog
from source.model.ForwardConfig import ForwardConfig

class ForwardDialog(BaseDialog):
    async def get_config(self):
        self.clear()
        config = await self._get_forward_config()
        if not config:
            return None
        
        forward_type = await self._get_forward_type()
        return config, forward_type

    async def _get_forward_config(self):
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

    async def _get_forward_type(self):
        options = [
            {"name": "Live", "value": "1"},
            {"name": "Past", "value": "2"}
        ]
        return await self.show_options("Forward Type:", options) 