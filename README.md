# queue_cast

溪村公寓排队预测程序。包含一个命令行版本与一个简易图形界面版本。

## 构建命令行版本

```bash
mkdir -p build && cd build
cmake ..
make
./queue_cast
```

## 运行图形界面

图形界面基于 Python 的 tkinter 实现，可用于交互式地管理排队记录并给出预测结果。程序启动时会加载保存的数据（默认包含历史记录），新添加或修改的记录会保存到 `records.json`，再次运行时将自动恢复。

```bash
python queue_cast_gui.py
```

在界面中输入日期（例如 `7.23` 表示 7 月 23 日）与对应的排队名次，点击 “Add Record” 添加数据。选中一条记录后可编辑输入框并点击 “Update Record” 修改，或点击 “Delete Record” 删除。点击 “Estimate” 将进行线性拟合并显示名次为 0 时的预计天数。

