# Surge 规则集整理

## 项目结构

```
surge-rule-sets/
├── rules/           # 规则文件目录
│   ├── Adblock4limbo.list    # 广告拦截规则
│   ├── adobecc.list          # Adobe Creative Cloud 规则
│   ├── Apple.list            # Apple 服务规则
│   ├── China.list            # 中国大陆服务规则
│   ├── Claude.list           # Claude AI 服务规则
│   ├── Global.list           # 全球通用规则
│   ├── GlobalMedia.list      # 全球媒体服务规则
│   ├── Microsoft.list        # Microsoft 服务规则
│   └── Netflix.list          # Netflix 服务规则
├── scripts/         # 脚本工具目录
│   ├── cleanup_rules.py      # 重复域名分析工具
│   ├── auto_cleanup.py       # 自动清理工具
│   └── final_cleanup.py      # 最终清理工具
├── docs/            # 文档目录
│   ├── 使用说明.md             # 脚本使用说明
│   └── 整理报告.md             # 详细的整理报告
├── backups/         # 备份文件目录
│   ├── *.backup_*           # 清理过程中的备份文件
│   └── *.final_backup_*     # 最终清理的备份文件
└── README.md        # 项目根目录说明
```

## 目录说明

### 📁 rules/
包含所有的 Surge 规则文件，按功能分类：
- **高优先级规则**（细粒度）：专门针对特定服务的规则
- **中优先级规则**（通用）：适用于多个服务的通用规则

### 📁 scripts/
包含用于规则整理和清理的 Python 脚本：
- `cleanup_rules.py`: 分析重复域名并提供清理建议
- `auto_cleanup.py`: 自动执行清理操作
- `final_cleanup.py`: 处理剩余的重复域名

### 📁 docs/
包含项目相关的文档：
- `README.md`: 详细的项目说明和使用指南
- `整理报告.md`: 完整的整理过程报告

### 📁 backups/
存储清理过程中的备份文件，确保可以随时回滚操作。

## 使用说明

### 运行脚本
```bash
# 进入脚本目录
cd scripts

# 分析重复域名
python3 cleanup_rules.py

# 自动清理（谨慎使用）
python3 auto_cleanup.py

# 最终清理
python3 final_cleanup.py
```

### 规则文件使用
1. 根据需要选择合适的规则文件
2. 避免同时使用包含重复域名的文件
3. 优先使用细粒度规则文件

## 整理状态

✅ **整理工作已完成**
- 移除了 78 个重复域名
- 所有域名现在只出现在一个文件中
- 规则文件大小得到优化

## 文件功能定位

### 高优先级文件（细粒度规则）
- `Netflix.list`: 专门针对 Netflix 服务
- `Microsoft.list`: 专门针对 Microsoft 服务  
- `Apple.list`: 专门针对 Apple 服务
- `adobecc.list`: 专门针对 Adobe Creative Cloud
- `Claude.list`: 专门针对 Claude AI
- `Adblock4limbo.list`: 专门针对广告拦截

### 中优先级文件（通用规则）
- `GlobalMedia.list`: 全球媒体服务（不包含 Netflix）
- `Global.list`: 全球通用服务（不包含媒体和特定服务）
- `China.list`: 中国大陆服务

## 维护建议

1. **定期检查**: 定期运行分析脚本检查新的重复域名
2. **备份重要**: 在修改前总是备份重要文件
3. **测试验证**: 修改后测试规则是否正常工作
4. **版本控制**: 使用 Git 进行版本控制

## 更新日志

- 2025-01-04: 完成主要整理工作，移除69个重复域名
- 2025-01-04: 创建自动化工具和详细报告
- 2025-01-04: 完成最终清理，移除剩余9个重复域名
- 2025-01-04: 重新组织目录结构，提高项目可维护性 