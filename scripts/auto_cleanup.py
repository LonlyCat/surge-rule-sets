#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动清理重复域名的脚本
根据分析结果自动移除重复域名
"""

import re
import os
import shutil
from datetime import datetime

class AutoCleaner:
    def __init__(self):
        self.domain_patterns = {
            'DOMAIN': r'^DOMAIN,([^,]+),',
            'DOMAIN-SUFFIX': r'^DOMAIN-SUFFIX,([^,]+),',
            'DOMAIN-KEYWORD': r'^DOMAIN-KEYWORD,([^,]+),',
            'IP-CIDR': r'^IP-CIDR,([^,]+),',
            'IP-CIDR6': r'^IP-CIDR6,([^,]+),',
        }
        
        # 需要从 Global.list 中移除的域名
        self.global_remove_domains = {
            '27.0.236.0/22',
            '110.76.140.0/22',
            '103.246.56.0/22',
            '103.27.148.0/22',
            '1.201.0.0/24',
            '198.45.48.0/20',
            '192.173.64.0/18',
            '37.77.184.0/21',
            '113.61.104.0/22',
            '101.32.96.0/20',
            '101.32.118.0/23',
            '129.226.0.0/16',
        }
        
        # 需要从 GlobalMedia.list 中移除的域名
        self.globalmedia_remove_domains = {
            '52.12.0.0/15',
            '23.246.0.0/18',
            '52.0.0.0/15',
            '52.7.0.0/16',
            '52.24.0.0/14',
            '218.102.32.0/19',
            '52.10.0.0/15',
            '64.120.128.0/17',
            '52.32.0.0/14',
            '52.5.0.0/16',
            '35.160.0.0/13',
            '45.57.0.0/17',
            '198.38.96.0/19',
            '52.54.0.0/16',
            '54.213.0.0/16',
            '208.75.76.0/22',
            '203.83.220.0/22',
            '38.72.126.0/24',
            '66.197.128.0/17',
            '203.198.80.0/21',
            '203.198.0.0/20',
            '54.188.0.0/15',
            '207.45.72.0/22',
            '108.175.32.0/20',
            '54.76.0.0/15',
            '185.2.220.0/22',
            '52.40.0.0/14',
            '54.68.0.0/15',
            '52.88.0.0/15',
            '203.116.0.0/16',
            '54.214.128.0/17',
            '203.75.84.0/24',
            '54.86.0.0/16',
            '54.0.0.0/16',
            '34.192.0.0/16',
            '23.78.0.0/16',
            '69.53.224.0/19',
            '54.148.0.0/15',
            '34.248.0.0/13',
            '52.72.0.0/16',
            '103.87.204.0/22',
            '54.175.0.0/16',
            '52.22.0.0/16',
            '54.186.0.0/15',
            '54.85.0.0/16',
            '52.48.0.0/14',
            '54.74.0.0/15',
            '34.208.0.0/12',
            '185.9.188.0/22',
            '44.230.0.0/16',
            '8.41.4.0/24',
            '44.224.0.0/16',
            '219.76.0.0/17',
            '2607:fb10::/32',
            '2620:10c:7000::/44',
            '2a03:5640::/32',
            '2a00:86c0::/32',
        }
    
    def backup_file(self, filename):
        """备份文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{filename}.backup_{timestamp}"
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
        """执行清理操作"""
        print("🚀 开始自动清理重复域名...")
        print("=" * 50)
        
        total_removed = 0
        
        # 清理 Global.list
        print("\n📝 清理 Global.list...")
        removed = self.cleanup_file('Global.list', self.global_remove_domains)
        print(f"   移除了 {removed} 个重复域名")
        total_removed += removed
        
        # 清理 GlobalMedia.list
        print("\n📝 清理 GlobalMedia.list...")
        removed = self.cleanup_file('GlobalMedia.list', self.globalmedia_remove_domains)
        print(f"   移除了 {removed} 个重复域名")
        total_removed += removed
        
        print("\n" + "=" * 50)
        print(f"✅ 清理完成！总共移除了 {total_removed} 个重复域名")
        print("\n📋 清理总结:")
        print(f"  - Global.list: 移除了 {len(self.global_remove_domains)} 个域名")
        print(f"  - GlobalMedia.list: 移除了 {len(self.globalmedia_remove_domains)} 个域名")
        print("\n💡 建议:")
        print("  1. 测试修改后的规则是否正常工作")
        print("  2. 如果发现问题，可以使用备份文件恢复")
        print("  3. 定期检查新的重复域名")

def main():
    cleaner = AutoCleaner()
    
    print("Surge 规则集自动清理工具")
    print("=" * 50)
    print("⚠️  警告: 此操作将修改原始文件")
    print("📋 将执行以下操作:")
    print("  1. 备份所有要修改的文件")
    print("  2. 从 Global.list 中移除 12 个重复域名")
    print("  3. 从 GlobalMedia.list 中移除 57 个重复域名")
    print()
    
    response = input("是否继续执行清理操作？(y/N): ").strip().lower()
    
    if response == 'y':
        cleaner.run_cleanup()
    else:
        print("❌ 取消清理操作")

if __name__ == "__main__":
    main() 