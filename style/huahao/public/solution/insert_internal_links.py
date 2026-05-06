#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为所有 .md 文件插入内链锚文本
"""

import os
import re

# ========================
# 页面元数据定义
# ========================

PAGES = {
    # L1 总汇页
    "bag-industry-solutions.md": {
        "title": "Industry Solutions for Bag Packaging",
        "level": 1,
        "parent": None,
        "children": [
            "01-retail-solution.md",
            "02-food-beverage-solution.md",
            "03-beauty-cosmetics-solution.md",
            "05-education-solution.md",
            "07-food-processing-solution.md",
            "08-hospitality-hotel-solution.md",
        ],
        "siblings": [],
        "cross": [],
    },
    # L2 行业页
    "01-retail-solution.md": {
        "title": "Retail Industry - Shopping Bag Solutions",
        "level": 2,
        "parent": "bag-industry-solutions.md",
        "children": [
            "01-A-luxury-retail-solution.md",
            "01-B-fast-fashion-solution.md",
            "01-C-jewelry-watches-solution.md",
            "01-D-supermarket-grocery-solution.md",
            "01-E-ecommerce-retail-solution.md",
        ],
        "siblings": ["03-beauty-cosmetics-solution.md", "08-hospitality-hotel-solution.md"],
        "cross": [],
    },
    "02-food-beverage-solution.md": {
        "title": "Food & Beverage Industry - Packaging Solutions",
        "level": 2,
        "parent": "bag-industry-solutions.md",
        "children": [
            "02-A-coffee-tea-solution.md",
            "02-B-bakery-desserts-solution.md",
            "02-C-fast-food-delivery-solution.md",
            "02-D-fine-dining-solution.md",
            "02-E-ready-to-cook-solution.md",
        ],
        "siblings": ["07-food-processing-solution.md", "05-education-solution.md"],
        "cross": [],
    },
    "03-beauty-cosmetics-solution.md": {
        "title": "Beauty & Cosmetics Industry - Gift Bag Solutions",
        "level": 2,
        "parent": "bag-industry-solutions.md",
        "children": [
            "03-A-premium-skincare-solution.md",
            "03-B-makeup-fragrance-solution.md",
            "03-C-personal-care-solution.md",
            "03-D-medical-aesthetics-solution.md",
            "03-E-beauty-subscription-solution.md",
        ],
        "siblings": ["01-retail-solution.md", "08-hospitality-hotel-solution.md"],
        "cross": [],
    },
    "05-education-solution.md": {
        "title": "Education Industry - Branded Bag Solutions",
        "level": 2,
        "parent": "bag-industry-solutions.md",
        "children": [
            "05-A-k12-schools-solution.md",
            "05-B-universities-solution.md",
            "05-C-training-centers-solution.md",
            "05-D-edtech-solution.md",
            "05-E-international-education-solution.md",
        ],
        "siblings": ["02-food-beverage-solution.md", "07-food-processing-solution.md"],
        "cross": [],
    },
    "07-food-processing-solution.md": {
        "title": "Food Processing Industry - Freshness Packaging Solutions",
        "level": 2,
        "parent": "bag-industry-solutions.md",
        "children": [
            "07-A-coffee-roasting-solution.md",
            "07-B-snacks-confectionery-solution.md",
            "07-C-seasonings-sauces-solution.md",
            "07-D-dairy-products-solution.md",
            "07-E-health-food-solution.md",
        ],
        "siblings": ["02-food-beverage-solution.md", "05-education-solution.md"],
        "cross": [],
    },
    "08-hospitality-hotel-solution.md": {
        "title": "Hospitality & Hotel Industry - Guest Experience Packaging",
        "level": 2,
        "parent": "bag-industry-solutions.md",
        "children": [
            "08-A-luxury-hotels-solution.md",
            "08-B-boutique-bnb-solution.md",
            "08-C-resorts-tourism-solution.md",
            "08-D-serviced-apartments-solution.md",
            "08-E-business-hotels-solution.md",
        ],
        "siblings": ["01-retail-solution.md", "03-beauty-cosmetics-solution.md"],
        "cross": [],
    },
    # L3 细分页 - 01 Retail
    "01-A-luxury-retail-solution.md": {
        "title": "Luxury Retail - Premium Packaging Solutions",
        "level": 3,
        "parent": "01-retail-solution.md",
        "children": [],
        "siblings": ["01-C-jewelry-watches-solution.md", "01-E-ecommerce-retail-solution.md"],
        "cross": ["03-A-premium-skincare-solution.md", "08-A-luxury-hotels-solution.md"],
    },
    "01-B-fast-fashion-solution.md": {
        "title": "Fast Fashion - Cost-Effective Bag Solutions",
        "level": 3,
        "parent": "01-retail-solution.md",
        "children": [],
        "siblings": ["01-E-ecommerce-retail-solution.md", "01-D-supermarket-grocery-solution.md"],
        "cross": ["02-C-fast-food-delivery-solution.md", "05-C-training-centers-solution.md"],
    },
    "01-C-jewelry-watches-solution.md": {
        "title": "Jewelry & Watches - Protective Packaging Solutions",
        "level": 3,
        "parent": "01-retail-solution.md",
        "children": [],
        "siblings": ["01-A-luxury-retail-solution.md", "01-E-ecommerce-retail-solution.md"],
        "cross": ["03-B-makeup-fragrance-solution.md", "08-A-luxury-hotels-solution.md"],
    },
    "01-D-supermarket-grocery-solution.md": {
        "title": "Supermarket & Grocery - Durable Shopping Bags",
        "level": 3,
        "parent": "01-retail-solution.md",
        "children": [],
        "siblings": ["01-B-fast-fashion-solution.md", "01-E-ecommerce-retail-solution.md"],
        "cross": ["06-A-grains-cereals-solution.md", "07-B-snacks-confectionery-solution.md"],
    },
    "01-E-ecommerce-retail-solution.md": {
        "title": "E-commerce Retail - Shipping & Unboxing Packaging",
        "level": 3,
        "parent": "01-retail-solution.md",
        "children": [],
        "siblings": ["01-A-luxury-retail-solution.md", "01-B-fast-fashion-solution.md"],
        "cross": ["09-A-consumer-electronics-solution.md", "05-D-edtech-solution.md"],
    },
    # L3 细分页 - 02 Food & Beverage
    "02-A-coffee-tea-solution.md": {
        "title": "Coffee & Tea Shop - Insulated Takeaway Bags",
        "level": 3,
        "parent": "02-food-beverage-solution.md",
        "children": [],
        "siblings": ["02-B-bakery-desserts-solution.md", "02-C-fast-food-delivery-solution.md"],
        "cross": ["07-A-coffee-roasting-solution.md", "06-E-tea-industry-solution.md"],
    },
    "02-B-bakery-desserts-solution.md": {
        "title": "Bakery & Desserts - Grease-Resistant Paper Bags",
        "level": 3,
        "parent": "02-food-beverage-solution.md",
        "children": [],
        "siblings": ["02-A-coffee-tea-solution.md", "02-D-fine-dining-solution.md"],
        "cross": ["07-B-snacks-confectionery-solution.md", "02-C-fast-food-delivery-solution.md"],
    },
    "02-C-fast-food-delivery-solution.md": {
        "title": "Fast Food & Delivery - Leak-Proof Packaging",
        "level": 3,
        "parent": "02-food-beverage-solution.md",
        "children": [],
        "siblings": ["02-A-coffee-tea-solution.md", "02-E-ready-to-cook-solution.md"],
        "cross": ["01-B-fast-fashion-solution.md", "07-C-seasonings-sauces-solution.md"],
    },
    "02-D-fine-dining-solution.md": {
        "title": "Fine Dining - Premium Restaurant Packaging",
        "level": 3,
        "parent": "02-food-beverage-solution.md",
        "children": [],
        "siblings": ["02-B-bakery-desserts-solution.md", "02-E-ready-to-cook-solution.md"],
        "cross": ["08-A-luxury-hotels-solution.md", "01-A-luxury-retail-solution.md"],
    },
    "02-E-ready-to-cook-solution.md": {
        "title": "Ready-to-Cook - Cold Chain & Vacuum Packaging",
        "level": 3,
        "parent": "02-food-beverage-solution.md",
        "children": [],
        "siblings": ["02-C-fast-food-delivery-solution.md", "02-D-fine-dining-solution.md"],
        "cross": ["04-B-pharmaceutical-solution.md", "07-D-dairy-products-solution.md"],
    },
    # L3 细分页 - 03 Beauty & Cosmetics
    "03-A-premium-skincare-solution.md": {
        "title": "Premium Skincare - Luxury Cosmetic Packaging",
        "level": 3,
        "parent": "03-beauty-cosmetics-solution.md",
        "children": [],
        "siblings": ["03-B-makeup-fragrance-solution.md", "03-D-medical-aesthetics-solution.md"],
        "cross": ["01-A-luxury-retail-solution.md", "08-A-luxury-hotels-solution.md"],
    },
    "03-B-makeup-fragrance-solution.md": {
        "title": "Makeup & Fragrance - Glass Bottle Protection Bags",
        "level": 3,
        "parent": "03-beauty-cosmetics-solution.md",
        "children": [],
        "siblings": ["03-A-premium-skincare-solution.md", "03-C-personal-care-solution.md"],
        "cross": ["01-C-jewelry-watches-solution.md", "03-E-beauty-subscription-solution.md"],
    },
    "03-C-personal-care-solution.md": {
        "title": "Personal Care - Daily Use Packaging Solutions",
        "level": 3,
        "parent": "03-beauty-cosmetics-solution.md",
        "children": [],
        "siblings": ["03-B-makeup-fragrance-solution.md", "03-D-medical-aesthetics-solution.md"],
        "cross": ["05-A-k12-schools-solution.md", "06-D-organic-farming-solution.md"],
    },
    "03-D-medical-aesthetics-solution.md": {
        "title": "Medical Aesthetics - Post-Treatment Care Kits",
        "level": 3,
        "parent": "03-beauty-cosmetics-solution.md",
        "children": [],
        "siblings": ["03-A-premium-skincare-solution.md", "03-E-beauty-subscription-solution.md"],
        "cross": ["04-E-aesthetic-consumables-solution.md", "04-A-medical-devices-solution.md"],
    },
    "03-E-beauty-subscription-solution.md": {
        "title": "Beauty Subscription - Monthly Box Packaging",
        "level": 3,
        "parent": "03-beauty-cosmetics-solution.md",
        "children": [],
        "siblings": ["03-B-makeup-fragrance-solution.md", "03-D-medical-aesthetics-solution.md"],
        "cross": ["09-A-consumer-electronics-solution.md", "01-E-ecommerce-retail-solution.md"],
    },
    # L3 细分页 - 04 Medical (无L2父页，直接上挂总汇)
    "04-A-medical-devices-solution.md": {
        "title": "Medical Devices - Sterile Barrier Packaging",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["04-B-pharmaceutical-solution.md", "04-C-ivd-diagnostics-solution.md"],
        "cross": ["03-D-medical-aesthetics-solution.md", "09-B-semiconductors-solution.md"],
    },
    "04-B-pharmaceutical-solution.md": {
        "title": "Pharmaceutical - Drug Packaging Solutions",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["04-A-medical-devices-solution.md", "04-C-ivd-diagnostics-solution.md"],
        "cross": ["02-E-ready-to-cook-solution.md", "04-D-supplements-solution.md"],
    },
    "04-C-ivd-diagnostics-solution.md": {
        "title": "IVD Diagnostics - Cold Chain Transport Packaging",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["04-A-medical-devices-solution.md", "04-B-pharmaceutical-solution.md"],
        "cross": ["04-E-aesthetic-consumables-solution.md", "09-B-semiconductors-solution.md"],
    },
    "04-D-supplements-solution.md": {
        "title": "Supplements - Health Product Packaging",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["04-B-pharmaceutical-solution.md", "04-E-aesthetic-consumables-solution.md"],
        "cross": ["07-E-health-food-solution.md", "06-D-organic-farming-solution.md"],
    },
    "04-E-aesthetic-consumables-solution.md": {
        "title": "Aesthetic Consumables - Disposable Medical Packaging",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["04-C-ivd-diagnostics-solution.md", "04-D-supplements-solution.md"],
        "cross": ["03-D-medical-aesthetics-solution.md", "04-A-medical-devices-solution.md"],
    },
    # L3 细分页 - 05 Education
    "05-A-k12-schools-solution.md": {
        "title": "K-12 Schools - Safe & Durable School Bags",
        "level": 3,
        "parent": "05-education-solution.md",
        "children": [],
        "siblings": ["05-B-universities-solution.md", "05-C-training-centers-solution.md"],
        "cross": ["03-C-personal-care-solution.md", "06-D-organic-farming-solution.md"],
    },
    "05-B-universities-solution.md": {
        "title": "Universities - Branded Campus Merchandise Bags",
        "level": 3,
        "parent": "05-education-solution.md",
        "children": [],
        "siblings": ["05-A-k12-schools-solution.md", "05-E-international-education-solution.md"],
        "cross": ["08-D-serviced-apartments-solution.md", "05-E-international-education-solution.md"],
    },
    "05-C-training-centers-solution.md": {
        "title": "Training Centers - Marketing Giveaway Bags",
        "level": 3,
        "parent": "05-education-solution.md",
        "children": [],
        "siblings": ["05-D-edtech-solution.md", "05-E-international-education-solution.md"],
        "cross": ["01-B-fast-fashion-solution.md", "05-D-edtech-solution.md"],
    },
    "05-D-edtech-solution.md": {
        "title": "EdTech - Course Kit & Delivery Packaging",
        "level": 3,
        "parent": "05-education-solution.md",
        "children": [],
        "siblings": ["05-C-training-centers-solution.md", "05-E-international-education-solution.md"],
        "cross": ["01-E-ecommerce-retail-solution.md", "09-E-telecom-equipment-solution.md"],
    },
    "05-E-international-education-solution.md": {
        "title": "International Education - Study Abroad Welcome Kits",
        "level": 3,
        "parent": "05-education-solution.md",
        "children": [],
        "siblings": ["05-B-universities-solution.md", "05-C-training-centers-solution.md"],
        "cross": ["08-C-resorts-tourism-solution.md", "05-B-universities-solution.md"],
    },
    # L3 细分页 - 06 Agriculture (无L2父页)
    "06-A-grains-cereals-solution.md": {
        "title": "Grains & Cereals - Heavy-Duty Woven Bags",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["06-B-fresh-produce-solution.md", "06-C-seeds-seedlings-solution.md"],
        "cross": ["01-D-supermarket-grocery-solution.md", "07-B-snacks-confectionery-solution.md"],
    },
    "06-B-fresh-produce-solution.md": {
        "title": "Fresh Produce - Breathable Storage Bags",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["06-A-grains-cereals-solution.md", "06-D-organic-farming-solution.md"],
        "cross": ["02-E-ready-to-cook-solution.md", "07-D-dairy-products-solution.md"],
    },
    "06-C-seeds-seedlings-solution.md": {
        "title": "Seeds & Seedlings - Moisture-Barrier Foil Bags",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["06-A-grains-cereals-solution.md", "06-E-tea-industry-solution.md"],
        "cross": ["04-D-supplements-solution.md", "07-E-health-food-solution.md"],
    },
    "06-D-organic-farming-solution.md": {
        "title": "Organic Farming - Compostable Eco Bags",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["06-B-fresh-produce-solution.md", "06-E-tea-industry-solution.md"],
        "cross": ["03-C-personal-care-solution.md", "05-A-k12-schools-solution.md"],
    },
    "06-E-tea-industry-solution.md": {
        "title": "Tea Industry - Aroma-Preserving Tea Bags",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["06-C-seeds-seedlings-solution.md", "06-D-organic-farming-solution.md"],
        "cross": ["02-A-coffee-tea-solution.md", "07-A-coffee-roasting-solution.md"],
    },
    # L3 细分页 - 07 Food Processing
    "07-A-coffee-roasting-solution.md": {
        "title": "Coffee Roasting - Degassing Valve Bags",
        "level": 3,
        "parent": "07-food-processing-solution.md",
        "children": [],
        "siblings": ["07-B-snacks-confectionery-solution.md", "07-E-health-food-solution.md"],
        "cross": ["02-A-coffee-tea-solution.md", "06-E-tea-industry-solution.md"],
    },
    "07-B-snacks-confectionery-solution.md": {
        "title": "Snacks & Confectionery - High-Barrier Zipper Bags",
        "level": 3,
        "parent": "07-food-processing-solution.md",
        "children": [],
        "siblings": ["07-A-coffee-roasting-solution.md", "07-C-seasonings-sauces-solution.md"],
        "cross": ["01-D-supermarket-grocery-solution.md", "06-A-grains-cereals-solution.md"],
    },
    "07-C-seasonings-sauces-solution.md": {
        "title": "Seasonings & Sauces - Spout Pouch Packaging",
        "level": 3,
        "parent": "07-food-processing-solution.md",
        "children": [],
        "siblings": ["07-B-snacks-confectionery-solution.md", "07-D-dairy-products-solution.md"],
        "cross": ["02-C-fast-food-delivery-solution.md", "02-E-ready-to-cook-solution.md"],
    },
    "07-D-dairy-products-solution.md": {
        "title": "Dairy Products - Powder & Liquid Barrier Bags",
        "level": 3,
        "parent": "07-food-processing-solution.md",
        "children": [],
        "siblings": ["07-C-seasonings-sauces-solution.md", "07-E-health-food-solution.md"],
        "cross": ["02-E-ready-to-cook-solution.md", "06-B-fresh-produce-solution.md"],
    },
    "07-E-health-food-solution.md": {
        "title": "Health Food - Supplement & Meal Replacement Bags",
        "level": 3,
        "parent": "07-food-processing-solution.md",
        "children": [],
        "siblings": ["07-A-coffee-roasting-solution.md", "07-D-dairy-products-solution.md"],
        "cross": ["04-D-supplements-solution.md", "06-C-seeds-seedlings-solution.md"],
    },
    # L3 细分页 - 08 Hospitality & Hotel
    "08-A-luxury-hotels-solution.md": {
        "title": "Luxury Hotels - Five-Star Welcome Amenities",
        "level": 3,
        "parent": "08-hospitality-hotel-solution.md",
        "children": [],
        "siblings": ["08-B-boutique-bnb-solution.md", "08-C-resorts-tourism-solution.md"],
        "cross": ["01-A-luxury-retail-solution.md", "03-A-premium-skincare-solution.md"],
    },
    "08-B-boutique-bnb-solution.md": {
        "title": "Boutique B&Bs - Cultural Themed Welcome Bags",
        "level": 3,
        "parent": "08-hospitality-hotel-solution.md",
        "children": [],
        "siblings": ["08-A-luxury-hotels-solution.md", "08-C-resorts-tourism-solution.md"],
        "cross": ["02-D-fine-dining-solution.md", "05-E-international-education-solution.md"],
    },
    "08-C-resorts-tourism-solution.md": {
        "title": "Resorts & Tourism - Waterproof Souvenir Bags",
        "level": 3,
        "parent": "08-hospitality-hotel-solution.md",
        "children": [],
        "siblings": ["08-A-luxury-hotels-solution.md", "08-B-boutique-bnb-solution.md"],
        "cross": ["05-E-international-education-solution.md", "02-D-fine-dining-solution.md"],
    },
    "08-D-serviced-apartments-solution.md": {
        "title": "Serviced Apartments - Long-Stay Practical Bags",
        "level": 3,
        "parent": "08-hospitality-hotel-solution.md",
        "children": [],
        "siblings": ["08-B-boutique-bnb-solution.md", "08-E-business-hotels-solution.md"],
        "cross": ["05-B-universities-solution.md", "01-D-supermarket-grocery-solution.md"],
    },
    "08-E-business-hotels-solution.md": {
        "title": "Business Hotels - Corporate Event & Laundry Bags",
        "level": 3,
        "parent": "08-hospitality-hotel-solution.md",
        "children": [],
        "siblings": ["08-C-resorts-tourism-solution.md", "08-D-serviced-apartments-solution.md"],
        "cross": ["09-E-telecom-equipment-solution.md", "05-D-edtech-solution.md"],
    },
    # L3 细分页 - 09 Electronics (无L2父页)
    "09-A-consumer-electronics-solution.md": {
        "title": "Consumer Electronics - Unboxing Experience Packaging",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["09-B-semiconductors-solution.md", "09-C-automotive-electronics-solution.md"],
        "cross": ["01-E-ecommerce-retail-solution.md", "03-E-beauty-subscription-solution.md"],
    },
    "09-B-semiconductors-solution.md": {
        "title": "Semiconductors - ESD & Moisture Barrier Packaging",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["09-A-consumer-electronics-solution.md", "09-C-automotive-electronics-solution.md"],
        "cross": ["04-A-medical-devices-solution.md", "04-C-ivd-diagnostics-solution.md"],
    },
    "09-C-automotive-electronics-solution.md": {
        "title": "Automotive Electronics - VCI Anti-Corrosion Bags",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["09-B-semiconductors-solution.md", "09-D-ev-batteries-solution.md"],
        "cross": ["09-D-ev-batteries-solution.md", "04-A-medical-devices-solution.md"],
    },
    "09-D-ev-batteries-solution.md": {
        "title": "EV Batteries - UN38.3 Certified Transport Bags",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["09-C-automotive-electronics-solution.md", "09-E-telecom-equipment-solution.md"],
        "cross": ["09-C-automotive-electronics-solution.md", "04-A-medical-devices-solution.md"],
    },
    "09-E-telecom-equipment-solution.md": {
        "title": "Telecom Equipment - Anti-Static Bulk Packaging",
        "level": 3,
        "parent": "bag-industry-solutions.md",
        "children": [],
        "siblings": ["09-A-consumer-electronics-solution.md", "09-D-ev-batteries-solution.md"],
        "cross": ["05-D-edtech-solution.md", "08-E-business-hotels-solution.md"],
    },
}


def get_anchor_text(target_file, source_file=None):
    """根据目标文件生成锚文本"""
    meta = PAGES.get(target_file, {})
    title = meta.get("title", target_file.replace("-solution.md", "").replace("-", " ").title())
    # 简化锚文本
    simple = title.split(" - ")[0].strip()
    return simple


def build_link_section(filename, meta):
    """为指定文件生成内链板块 Markdown"""
    lines = []
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🔗 Related Packaging Solutions")
    lines.append("")

    parent = meta.get("parent")
    children = meta.get("children", [])
    siblings = meta.get("siblings", [])
    cross = meta.get("cross", [])
    level = meta.get("level", 3)

    # 上行链
    if parent:
        anchor = get_anchor_text(parent)
        html_file = parent.replace(".md", ".html")
        lines.append(f"- **Up Next**: [{anchor}]({html_file})")
        lines.append("")

    # 下行链
    if children:
        lines.append("**Explore Sub-Solutions:**")
        for child in children:
            anchor = get_anchor_text(child)
            html_file = child.replace(".md", ".html")
            lines.append(f"- [{anchor}]({html_file})")
        lines.append("")

    # 平级链
    if siblings:
        lines.append("**You May Also Like:**")
        for sib in siblings:
            anchor = get_anchor_text(sib)
            html_file = sib.replace(".md", ".html")
            lines.append(f"- [{anchor}]({html_file})")
        lines.append("")

    # 交叉链
    if cross:
        lines.append("**Cross-Industry Solutions:**")
        for c in cross:
            anchor = get_anchor_text(c)
            html_file = c.replace(".md", ".html")
            lines.append(f"- [{anchor}]({html_file})")
        lines.append("")

    # CTA
    lines.append("---")
    lines.append("")
    lines.append("> 💬 **Need a custom packaging solution?** [Request a free quote](/contact.html) or [order samples](/samples.html) today.")
    lines.append("")

    return "\n".join(lines)


def insert_links_to_file(filename):
    """将内链板块插入到指定文件末尾（最后一个分隔线之前）"""
    filepath = os.path.join(os.getcwd(), filename)
    if not os.path.exists(filepath):
        print(f"[SKIP] File not found: {filename}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 如果已存在 Related Packaging Solutions 板块，跳过
    if "## 🔗 Related Packaging Solutions" in content:
        print(f"[SKIP] Already has link section: {filename}")
        return False

    meta = PAGES.get(filename)
    if not meta:
        print(f"[SKIP] No metadata for: {filename}")
        return False

    link_section = build_link_section(filename, meta)

    # 尝试在最后一个 `---` 或版权行前插入
    # 策略：如果文件以 `*©*` 或 `---` 结尾，在其前面插入
    patterns = [
        r"\n---\s*\n\s*\*©",
        r"\n\*©",
        r"\n---\s*\n\s*\*",
    ]
    inserted = False
    for pat in patterns:
        match = list(re.finditer(pat, content))
        if match:
            last_match = match[-1]
            pos = last_match.start()
            new_content = content[:pos] + link_section + content[pos:]
            inserted = True
            break

    if not inserted:
        # 直接追加到末尾
        new_content = content.rstrip("\n") + "\n" + link_section

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[OK] Inserted links into: {filename}")
    return True


def generate_mermaid_graph():
    """生成 Mermaid 流程图代码"""
    lines = []
    lines.append("```mermaid")
    lines.append("flowchart TB")
    lines.append("")

    # L1
    lines.append('  L1["🌐 bag-industry-solutions<br/>Industry Solutions Hub"]')
    lines.append("")

    # L2 nodes
    l2_files = [f for f, m in PAGES.items() if m["level"] == 2]
    for i, f in enumerate(l2_files, 1):
        short = f.replace("-solution.md", "").replace("-", " ")
        lines.append(f'  L2_{i}["📁 {short}"]')
        lines.append(f"  L1 --> L2_{i}")
    lines.append("")

    # L3 nodes grouped by parent
    l3_by_parent = {}
    for f, m in PAGES.items():
        if m["level"] == 3:
            p = m.get("parent", "orphan")
            l3_by_parent.setdefault(p, []).append(f)

    l3_idx = 0
    for parent, children in l3_by_parent.items():
        parent_short = parent.replace("-solution.md", "").replace("-", "") if parent else "orphan"
        for child in children:
            l3_idx += 1
            short = child.replace("-solution.md", "").replace("-", " ")
            lines.append(f'  L3_{l3_idx}["📄 {short}"]')
            # find parent node index
            if parent and parent in PAGES and PAGES[parent]["level"] == 2:
                p_idx = l2_files.index(parent) + 1
                lines.append(f"  L2_{p_idx} --> L3_{l3_idx}")
            else:
                lines.append(f"  L1 --> L3_{l3_idx}")
    lines.append("")

    # Cross links (sample, only show a few to avoid clutter)
    cross_pairs = [
        ("01-A-luxury-retail-solution.md", "08-A-luxury-hotels-solution.md"),
        ("02-A-coffee-tea-solution.md", "07-A-coffee-roasting-solution.md"),
        ("03-D-medical-aesthetics-solution.md", "04-E-aesthetic-consumables-solution.md"),
    ]
    lines.append("  %% Cross-industry links")
    for a, b in cross_pairs:
        # find indices
        def find_idx(f):
            if f in l2_files:
                return f"L2_{l2_files.index(f)+1}"
            else:
                all_l3 = [x for lst in l3_by_parent.values() for x in lst]
                if f in all_l3:
                    return f"L3_{all_l3.index(f)+1}"
            return None
        ai = find_idx(a)
        bi = find_idx(b)
        if ai and bi:
            lines.append(f"  {ai} -.-> {bi}")

    lines.append("```")
    return "\n".join(lines)


def generate_html_table():
    """生成 HTML 内链关系总表"""
    rows = []
    for filename, meta in sorted(PAGES.items()):
        level = meta["level"]
        title = meta["title"]
        html_name = filename.replace(".md", ".html")

        parent = meta.get("parent")
        parent_link = f'<a href="{parent.replace(".md", ".html")}">{get_anchor_text(parent)}</a>' if parent else "—"

        children = meta.get("children", [])
        children_links = "<br/>".join([
            f'<a href="{c.replace(".md", ".html")}">{get_anchor_text(c)}</a>' for c in children
        ]) if children else "—"

        siblings = meta.get("siblings", [])
        siblings_links = "<br/>".join([
            f'<a href="{s.replace(".md", ".html")}">{get_anchor_text(s)}</a>' for s in siblings
        ]) if siblings else "—"

        cross = meta.get("cross", [])
        cross_links = "<br/>".join([
            f'<a href="{c.replace(".md", ".html")}">{get_anchor_text(c)}</a>' for c in cross
        ]) if cross else "—"

        rows.append(f"""
    <tr>
      <td><strong>L{level}</strong></td>
      <td><a href="{html_name}">{title}</a></td>
      <td>{parent_link}</td>
      <td>{children_links}</td>
      <td>{siblings_links}</td>
      <td>{cross_links}</td>
    </tr>
""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Internal Link Strategy Map</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f8f9fa; }}
  h1 {{ color: #1a1a2e; }}
  h2 {{ color: #16213e; margin-top: 40px; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
  th {{ background: #1a1a2e; color: #fff; padding: 14px 12px; text-align: left; }}
  td {{ padding: 12px; border-bottom: 1px solid #e9ecef; vertical-align: top; }}
  tr:hover {{ background: #f1f3f5; }}
  a {{ color: #0f3460; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
  .L1 {{ background: #e63946; color: white; }}
  .L2 {{ background: #457b9d; color: white; }}
  .L3 {{ background: #2a9d8f; color: white; }}
  .mermaid {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body>
<h1>🔗 Internal Link Strategy Map</h1>
<p>Visual overview of all page relationships, link directions, and cross-industry connections.</p>

<h2>📊 Architecture Flowchart</h2>
<div class="mermaid">
flowchart TB
  L1["🌐 bag-industry-solutions\nIndustry Solutions Hub"]
  L1 --> L2_01["📁 01 Retail"]
  L1 --> L2_02["📁 02 Food Beverage"]
  L1 --> L2_03["📁 03 Beauty Cosmetics"]
  L1 --> L2_05["📁 05 Education"]
  L1 --> L2_07["📁 07 Food Processing"]
  L1 --> L2_08["📁 08 Hospitality Hotel"]
  L1 --> L3_orphan["📄 04 / 06 / 09 Sub-sectors\n(Link directly to Hub)"]

  L2_01 --> L3_01A["📄 01-A Luxury Retail"]
  L2_01 --> L3_01B["📄 01-B Fast Fashion"]
  L2_01 --> L3_01C["📄 01-C Jewelry Watches"]
  L2_01 --> L3_01D["📄 01-D Supermarket"]
  L2_01 --> L3_01E["📄 01-E Ecommerce"]

  L2_02 --> L3_02A["📄 02-A Coffee Tea"]
  L2_02 --> L3_02B["📄 02-B Bakery"]
  L2_02 --> L3_02C["📄 02-C Fast Food"]
  L2_02 --> L3_02D["📄 02-D Fine Dining"]
  L2_02 --> L3_02E["📄 02-E Ready to Cook"]

  L2_03 --> L3_03A["📄 03-A Premium Skincare"]
  L2_03 --> L3_03B["📄 03-B Makeup Fragrance"]
  L2_03 --> L3_03C["📄 03-C Personal Care"]
  L2_03 --> L3_03D["📄 03-D Medical Aesthetics"]
  L2_03 --> L3_03E["📄 03-E Beauty Subscription"]

  L3_01A -.-> L3_08A["📄 08-A Luxury Hotels"]
  L3_02A -.-> L3_07A["📄 07-A Coffee Roasting"]
  L3_03D -.-> L3_04E["📄 04-E Aesthetic Consumables"]
</div>

<h2>📋 Full Link Matrix</h2>
<table>
  <thead>
    <tr>
      <th>Level</th>
      <th>Page</th>
      <th>Parent (Up)</th>
      <th>Children (Down)</th>
      <th>Siblings (Related)</th>
      <th>Cross-Industry</th>
    </tr>
  </thead>
  <tbody>
{''.join(rows)}
  </tbody>
</table>

<h2>📈 Link Distribution Stats</h2>
<table>
  <tr><th>Metric</th><th>Value</th></tr>
  <tr><td>Total Pages</td><td>{len(PAGES)}</td></tr>
  <tr><td>L1 Hub Pages</td><td>{sum(1 for m in PAGES.values() if m['level']==1)}</td></tr>
  <tr><td>L2 Industry Pages</td><td>{sum(1 for m in PAGES.values() if m['level']==2)}</td></tr>
  <tr><td>L3 Sub-sector Pages</td><td>{sum(1 for m in PAGES.values() if m['level']==3)}</td></tr>
  <tr><td>Total Internal Links</td><td>{sum(len(m.get('children',[]))+len(m.get('siblings',[]))+len(m.get('cross',[]))+(1 if m.get('parent') else 0) for m in PAGES.values())}</td></tr>
</table>

<script>mermaid.initialize({{startOnLoad:true}});</script>
</body>
</html>
"""
    return html


def main():
    modified = 0
    skipped = 0

    # 1. 批量插入内链
    for filename in sorted(PAGES.keys()):
        if insert_links_to_file(filename):
            modified += 1
        else:
            skipped += 1

    print(f"\n{'='*50}")
    print(f"Batch Insert Complete: {modified} modified, {skipped} skipped")
    print(f"{'='*50}")

    # 2. 生成可视化图表
    # Mermaid Markdown
    mermaid_md = generate_mermaid_graph()
    with open("internal-link-graph.md", "w", encoding="utf-8") as f:
        f.write("# Internal Link Architecture Graph\n\n")
        f.write("> Generated Mermaid diagram showing page hierarchy and cross-links.\n\n")
        f.write(mermaid_md)
        f.write("\n\n---\n\n")
        f.write("## Legend\n\n")
        f.write("- `Solid arrow (-->)` = Parent → Child (hierarchical link)\n")
        f.write("- `Dotted arrow (-.->)` = Cross-industry / contextual link\n")
        f.write("- `L1` = Hub page  |  `L2` = Industry page  |  `L3` = Sub-sector page\n")
    print("[OK] Generated: internal-link-graph.md")

    # HTML Dashboard
    html_content = generate_html_table()
    with open("internal-link-dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("[OK] Generated: internal-link-dashboard.html")


if __name__ == "__main__":
    main()
