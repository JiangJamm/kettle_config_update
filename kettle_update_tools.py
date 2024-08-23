import json

from lxml import etree


class KettleConfig:
    def __init__(self, config_path):
        self.config = self._get_config(self, config_path=config_path)
        self.database_config = self._get_database_config(self, self.config)
        self.root_path_config = self._get_path_config(self, self.config)

    @staticmethod
    def _get_config(self, config_path) -> dict:
        _config = json.load(open(config_path))

        return _config

    @staticmethod
    def _get_database_config(self, _config) -> list[dict]:
        _database_config = _config.get("database")

        return _database_config

    @staticmethod
    def _get_path_config(self, _config) -> list:
        _root_path_config = _config.get("root_path")

        return _root_path_config


class KettleUpdate:
    def __init__(self):
        pass

    def update_connection(self, element, connection_config):
        if element.text is None:
            pass
        elif len(element) == 0 and element.text is not None:
            for connection_item in connection_config:
                if connection_item["old"].get("name") == element.text:
                    element.text = connection_item["new"]["name"]
        else:
            name = element.find("name")
            if name is not None:
                name_text = name.text
                for connection_item in connection_config:
                    if name_text == connection_item["old"].get("name"):
                        for key, value in connection_item["new"].items():
                            old_element = element.find(key)
                            if old_element is not None:
                                old_element.text = value

    def update_root_path(self, element, root_path_config):
        filename = element.find("filename")
        if filename is not None and filename.text:
            # 获取当前的路径
            original_path = filename.text.replace("\\", "/")

            # 遍历替换路径列表
            for path in root_path_config:
                old = path["old"]
                new = path["new"]
                if old in original_path:
                    # 执行路径替换
                    original_path = original_path.replace(old, new)
                    print(f"Updated path: {original_path}")

            # 更新 XML 中的路径
            filename.text = original_path
