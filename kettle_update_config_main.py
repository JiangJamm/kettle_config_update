import os

from kettle_update_tools import KettleConfig, KettleUpdate
from lxml import etree

config_path = "kettle_config.json"
source_root = "input/"
output_root = "output/"

config = KettleConfig(config_path)
kettle_update = KettleUpdate()

# 遍历源文件夹
for root_dir, sub_dirs, files in os.walk(source_root):
    for file_name in files:
        # 获取当前文件的完整路径
        file_path = os.path.join(root_dir, file_name)
        print(file_path)

        with open(file_path, "r", encoding="utf-8") as xml_file:
            parser = etree.XMLParser(resolve_entities=False)
            tree = etree.parse(xml_file, parser=parser)
            root = tree.getroot()

            if file_name.endswith(".kjb"):
                entries = root.find(".//entries").findall(".//entry")
                for entry in entries:
                    kettle_update.update_root_path(entry, config.root_path_config)

                connections = tree.findall(".//connection")
                for connection in connections:
                    kettle_update.update_connection(connection, config.database_config)

            elif file_name.endswith(".ktr"):
                connections = tree.findall(".//connection")
                for connection in connections:
                    kettle_update.update_connection(connection, config.database_config)
            else:
                print(f"{file_path} is not a kettle file.")

        # 创建对应的输出目录
        relative_path = os.path.relpath(root_dir, source_root)
        output_dir = os.path.join(output_root, relative_path)
        os.makedirs(output_dir, exist_ok=True)

        # 保存处理后的文件到输出目录
        output_file_path = os.path.join(output_dir, file_name)
        tree.write(
            output_file_path,
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )
