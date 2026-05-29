#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
期刊投稿辅助工具
功能：检查投稿材料清单、生成投稿时间线、提醒重要日期
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict

class SubmissionChecker:
    """投稿材料检查器"""
    
    def __init__(self):
        self.required_materials = {
            "manuscript": {
                "name": "稿件正文",
                "required": True,
                "formats": [".docx", ".doc", ".tex"],
                "tips": "确保格式符合期刊要求，包括行距、字体、页边距等"
            },
            "cover_letter": {
                "name": "Cover Letter",
                "required": True,
                "formats": [".pdf", ".docx"],
                "tips": "包含论文亮点、原创性声明、推荐审稿人"
            },
            "figures": {
                "name": "图片文件",
                "required": True,
                "formats": [".tiff", ".eps", ".png", ".jpg"],
                "tips": "分辨率至少300dpi，色彩模式RGB或CMYK"
            },
            "tables": {
                "name": "表格",
                "required": True,
                "formats": [".docx", ".xls", ".xlsx"],
                "tips": "可编辑格式，不要转为图片"
            },
            "supplementary": {
                "name": "补充材料",
                "required": False,
                "formats": [".pdf", ".zip"],
                "tips": "原始数据、额外图表、视频等"
            },
            "highlights": {
                "name": "研究亮点",
                "required": False,
                "formats": [".docx", ".txt"],
                "tips": "3-5条，每条不超过85字符（含空格）"
            },
            "graphical_abstract": {
                "name": "图文摘要",
                "required": False,
                "formats": [".tiff", ".eps", ".png"],
                "tips": "尺寸通常1200x600像素，清晰展示核心发现"
            },
            "author_info": {
                "name": "作者信息",
                "required": True,
                "formats": ["online form"],
                "tips": "所有作者的姓名、单位、邮箱、ORCID"
            },
            "conflict_of_interest": {
                "name": "利益冲突声明",
                "required": True,
                "formats": [".pdf", ".docx", "online form"],
                "tips": "说明是否存在经济利益或其他利益冲突"
            },
            "data_availability": {
                "name": "数据可用性声明",
                "required": False,
                "formats": [".pdf", ".docx", "in manuscript"],
                "tips": "说明数据存储位置和获取方式"
            }
        }
    
    def check_materials(self, submitted: List[str]) -> Dict:
        """
        检查投稿材料是否完整
        
        Args:
            submitted: 已准备的材料列表
            
        Returns:
            检查结果字典
        """
        result = {
            "complete": True,
            "missing": [],
            "optional_missing": [],
            "ready_items": [],
            "tips": []
        }
        
        for key, info in self.required_materials.items():
            if key in submitted:
                result["ready_items"].append(info["name"])
            else:
                if info["required"]:
                    result["complete"] = False
                    result["missing"].append(info["name"])
                    result["tips"].append(f"⚠️ 必需材料缺失：{info['name']} - {info['tips']}")
                else:
                    result["optional_missing"].append(info["name"])
                    result["tips"].append(f"💡 可选材料：{info['name']} - {info['tips']}")
        
        return result
    
    def generate_checklist(self) -> str:
        """生成完整的投稿检查清单"""
        checklist = "## 📋 投稿材料检查清单\n\n"
        checklist += "### ✅ 必需材料\n\n"
        
        for key, info in self.required_materials.items():
            if info["required"]:
                checklist += f"- [ ] **{info['name']}**\n"
                checklist += f"  - 支持格式：{', '.join(info['formats'])}\n"
                checklist += f"  - 提示：{info['tips']}\n\n"
        
        checklist += "### 💡 可选材料（根据期刊要求）\n\n"
        
        for key, info in self.required_materials.items():
            if not info["required"]:
                checklist += f"- [ ] **{info['name']}**\n"
                checklist += f"  - 支持格式：{', '.join(info['formats'])}\n"
                checklist += f"  - 提示：{info['tips']}\n\n"
        
        return checklist


class TimelineGenerator:
    """投稿时间线生成器"""
    
    def __init__(self):
        self.default_durations = {
            "preparation": 14,  # 准备材料
            "internal_review": 7,  # 内部审阅
            "submission": 1,  # 提交
            "editor_assignment": 3,  # 编辑分配
            "peer_review": 30,  # 同行评审（变化大）
            "revision": 14,  # 修改
            "final_decision": 7  # 最终决定
        }
    
    def generate_timeline(self, start_date: str = None) -> List[Dict]:
        """
        生成投稿时间线
        
        Args:
            start_date: 开始日期，格式 YYYY-MM-DD
            
        Returns:
            时间线列表
        """
        if start_date is None:
            start_date = datetime.now().strftime("%Y-%m-%d")
        
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        timeline = []
        
        stages = [
            ("准备材料", "preparation"),
            ("内部审阅", "internal_review"),
            ("在线提交", "submission"),
            ("编辑分配", "editor_assignment"),
            ("同行评审", "peer_review"),
            ("修改完善", "revision"),
            ("最终决定", "final_decision")
        ]
        
        for stage_name, stage_key in stages:
            duration = self.default_durations[stage_key]
            end_date = current_date + timedelta(days=duration)
            
            timeline.append({
                "stage": stage_name,
                "start": current_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "duration_days": duration,
                "status": "pending"
            })
            
            current_date = end_date
        
        return timeline
    
    def print_timeline(self, start_date: str = None) -> str:
        """打印可视化的时间线"""
        timeline = self.generate_timeline(start_date)
        
        output = "## 📅 投稿时间线预估\n\n"
        output += "| 阶段 | 开始日期 | 结束日期 | 预计天数 | 状态 |\n"
        output += "|------|----------|----------|----------|------|\n"
        
        for item in timeline:
            output += f"| {item['stage']} | {item['start']} | {item['end']} | {item['duration_days']} | ⏳ 待完成 |\n"
        
        output += "\n> ⚠️ 注意：同行评审时间因期刊和领域而异，上述时间为预估值\n"
        output += "> 实际周期请参考目标期刊的平均审稿速度\n"
        
        return output


def main():
    """主函数示例"""
    print("=" * 60)
    print("期刊投稿辅助工具")
    print("=" * 60)
    
    # 初始化检查器
    checker = SubmissionChecker()
    
    # 生成检查清单
    print("\n" + checker.generate_checklist())
    
    # 生成时间线
    timeline_gen = TimelineGenerator()
    print(timeline_gen.print_timeline())
    
    # 示例：检查已准备的材料
    sample_submitted = ["manuscript", "cover_letter", "figures", "tables"]
    result = checker.check_materials(sample_submitted)
    
    print("\n## 🔍 当前材料准备情况\n")
    print(f"✅ 已完成：{len(result['ready_items'])} 项")
    print(f"❌ 缺失必需材料：{len(result['missing'])} 项")
    print(f"💡 缺失可选材料：{len(result['optional_missing'])} 项")
    
    if result['tips']:
        print("\n### 建议\n")
        for tip in result['tips']:
            print(f"{tip}")


if __name__ == "__main__":
    main()
