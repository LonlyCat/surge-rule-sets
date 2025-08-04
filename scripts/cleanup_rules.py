#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Surge 规则集整理工具
用于移除重复域名，确保一个域名只保留在一个文件内
"""

import re
import os
from collections import defaultdict

class RuleCleaner:
    def __init__(self):
        self.domain_patterns = {
            'DOMAIN': r'^DOMAIN,([^,]+),',
            'DOMAIN-SUFFIX': r'^DOMAIN-SUFFIX,([^,]+),',
            'DOMAIN-KEYWORD': r'^DOMAIN-KEYWORD,([^,]+),',
            'IP-CIDR': r'^IP-CIDR,([^,]+),',
            'IP-CIDR6': r'^IP-CIDR6,([^,]+),',
        }
        
    def extract_domains(self, content):
        """从规则内容中提取域名"""
        domains = defaultdict(set)
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            for rule_type, pattern in self.domain_patterns.items():
                match = re.match(pattern, line)
                if match:
                    domain = match.group(1)
                    domains[rule_type].add(domain)
                    break
                    
        return domains
    
    def find_duplicates(self, files):
        """查找重复的域名"""
        all_domains = {}
        duplicates = defaultdict(list)
        
        for filename in files:
            if not filename.endswith('.list'):
                continue
                
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                
            domains = self.extract_domains(content)
            all_domains[filename] = domains
            
            # 检查重复
            for rule_type, domain_set in domains.items():
                for domain in domain_set:
                    if domain in duplicates:
                        duplicates[domain].append(filename)
                    else:
                        duplicates[domain] = [filename]
        
        return all_domains, duplicates
    
    def get_file_priority(self, filename):
        """获取文件优先级（细粒度规则优先）"""
        high_priority = [
            'adobecc.list',
            'Apple.list', 
            'Claude.list',
            'Microsoft.list',
            'Netflix.list',
            'Adblock4limbo.list'
        ]
        
        if filename in high_priority:
            return 1  # 高优先级
        else:
            return 2  # 低优先级
    
    def suggest_cleanup(self, files):
        """建议清理方案"""
        all_domains, duplicates = self.find_duplicates(files)
        
        print("=== 重复域名分析 ===\n")
        
        # 找出真正的重复
        real_duplicates = {domain: files for domain, files in duplicates.items() 
                          if len(files) > 1}
        
        if not real_duplicates:
            print("✅ 没有发现重复域名")
            return
        
        print(f"发现 {len(real_duplicates)} 个重复域名：\n")
        
        for domain, file_list in real_duplicates.items():
            print(f"域名: {domain}")
            print(f"  出现在: {', '.join(file_list)}")
            
            # 建议保留在哪个文件
            priorities = [(f, self.get_file_priority(f)) for f in file_list]
            priorities.sort(key=lambda x: x[1])
            suggested_file = priorities[0][0]
            
            print(f"  建议保留在: {suggested_file}")
            print()
    
    def cleanup_file(self, filename, domains_to_remove):
        """清理文件中的重复域名"""
        with open(filename, 'r', encoding='utf-8') as f:
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
                        break
            
            if should_keep:
                cleaned_lines.append(line)
        
        # 写回文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        
        return removed_count

def main():
    cleaner = RuleCleaner()
    
    # 获取所有 .list 文件
    rules_dir = '../rules'
    files = [os.path.join(rules_dir, f) for f in os.listdir(rules_dir) if f.endswith('.list')]
    
    print("Surge 规则集整理工具")
    print("=" * 50)
    
    # 分析重复
    cleaner.suggest_cleanup(files)
    
    # 询问是否执行清理
    response = input("\n是否要执行清理操作？(y/N): ").strip().lower()
    
    if response == 'y':
        print("\n开始清理...")
        
        # 这里可以添加具体的清理逻辑
        # 为了安全起见，先只显示分析结果
        print("清理功能待实现，请手动根据建议进行清理")
    else:
        print("取消清理操作")

if __name__ == "__main__":
    main() 