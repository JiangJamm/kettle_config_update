# Kettle 批量替换配置
本程序可以根据标签批量替换Kettle配置，现支持：
- 数据库连接
- 文件夹根路径

# Quick Start
1. 将要替换的Kettle文件放入`input/`文件夹中，支持文件和多层文件夹
2. 修改`kettle_config.json`
   - 必须遵守文件格式
   - 替换时以`database.old.name`进行匹配，`old`其他选项可不填
3. 运行`kettle_update_config_main.py`
4. 结果会与`input`文件夹中相同的组织形式导出到`output/`
