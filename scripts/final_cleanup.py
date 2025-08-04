#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终清理脚本 - 处理剩余的9个重复域名
"""

import re
import os
import shutil
from datetime import datetime

class FinalCleaner:
    def __init__(self):
        self.domain_patterns = {
            'DOMAIN': r'^DOMAIN,([^,]+),',
            'DOMAIN-SUFFIX': r'^DOMAIN-SUFFIX,([^,]+),',
            'DOMAIN-KEYWORD': r'^DOMAIN-KEYWORD,([^,]+),',
            'IP-CIDR': r'^IP-CIDR,([^,]+),',
            'IP-CIDR6': r'^IP-CIDR6,([^,]+),',
        }
        
        # 剩余的重复域名 - 从其他文件中移除，保留在 Netflix.list 中
        self.remaining_duplicates = {
            'Global.list': {
                '45.57.0.0/17',
                '108.175.32.0/20',
                '23.246.0.0/18',
                '64.120.128.0/17',
                '198.38.96.0/19',
                '66.197.128.0/17',
            },
            'GlobalMedia.list': {
                '192.173.64.0/18',
                '37.77.184.0/21',
                '198.45.48.0/20',
            }
        }
    
    def backup_file(self, filename):
        """备份文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{filename}.final_backup_{timestamp}"
        file_path = os.path.join('../rules', filename)
        backup_path = os.path.join('../backups', backup_name)
        shutil.copy2(file_path, backup_path)
        print(f"✅ 已备份 {filename} 到 {backup_name}")
        return backup_name
    
    def cleanup_file(self, filename, domains_to_remove):
        """清理文件中的重复域名"""
        file_path = os.path.join('../rules', filename)
        if not os.path.exists(file_path):
            print(f"❌ 文件 {filename} 不存在")
            return 0
        
        # 备份原文件
        self.backup_file(filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        cleaned_lines = []
        removed_count = 0
        
        for line in lines:
            should_keep = True
            
            for rule_type, pattern in self.domain_patterns.items():
                match = re.match(pattern, line)
                if match:
                    domain = match.group(1)
                    if domain in domains_to_remove:
                        should_keep = False
                        removed_count += 1
                        print(f"  移除: {domain}")
                        break
            
            if should_keep:
                cleaned_lines.append(line)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        
        return removed_count
    
    def run_cleanup(self):
        """执行最终清理操作"""
        print("🚀 开始最终清理 - 处理剩余重复域名...")
        print("=" * 50)
        
        total_removed = 0
        
        # 清理 Global.list
        print("\n📝 清理 Global.list...")
        removed = self.cleanup_file('Global.list', self.remaining_duplicates['Global.list'])
        print(f"   移除了 {removed} 个重复域名")
        total_removed += removed
        
        # 清理 GlobalMedia.list
        print("\n📝 清理 GlobalMedia.list...")
        removed = self.cleanup_file('GlobalMedia.list', self.remaining_duplicates['GlobalMedia.list'])
        print(f"   移除了 {removed} 个重复域名")
        total_removed += removed
        
        print("\n" + "=" * 50)
        print(f"✅ 最终清理完成！总共移除了 {total_removed} 个重复域名")
        print("\n📋 清理总结:")
        print(f"  - Global.list: 移除了 {len(self.remaining_duplicates['Global.list'])} 个域名")
        print(f"  - GlobalMedia.list: 移除了 {len(self.remaining_duplicates['GlobalMedia.list'])} 个域名")
        print("\n🎉 整理工作完成！")
        print("💡 建议:")
        print("  1. 测试修改后的规则是否正常工作")
        print("  2. 如果发现问题，可以使用备份文件恢复")
        print("  3. 定期检查新的重复域名")

def main():
    cleaner = FinalCleaner()
    
    print("Surge 规则集最终清理工具")
    print("=" * 50)
    print("⚠️  警告: 此操作将修改原始文件")
    print("📋 将执行以下操作:")
    print("  1. 备份所有要修改的文件")
    print("  2. 从 Global.list 中移除 6 个重复域名")
    print("  3. 从 GlobalMedia.list 中移除 3 个重复域名")
    print("  4. 所有重复域名将保留在 Netflix.list 中")
    print()
    
    response = input("是否继续执行最终清理操作？(y/N): ").strip().lower()
    
    if response == 'y':
        cleaner.run_cleanup()
    else:
        print("❌ 取消清理操作")

if __name__ == "__main__":
    main() 