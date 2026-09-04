from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone, timedelta
from app.models import InventoryItem, Vendor, PurchaseOrder
from app.services.ai import get_ai_provider

def get_inventory_status(db: Session):
    items = db.query(InventoryItem).all()
    
    low_stock = []
    normal_stock = []
    
    for item in items:
        vendor_name = db.query(Vendor).filter(Vendor.id == item.vendor_id).first().name
        item_data = {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "current_stock": item.current_stock,
            "minimum_stock": item.minimum_stock,
            "vendor": vendor_name,
            "price": item.unit_price,
            "status": "Low Stock" if item.current_stock <= item.minimum_stock else "Normal"
        }
        
        if item.current_stock <= item.minimum_stock:
            low_stock.append(item_data)
        else:
            normal_stock.append(item_data)
            
    # Generate AI Purchase Recommendations for Low Stock
    ai_recommendations = []
    if low_stock:
        provider = get_ai_provider()
        prompt_data = {
            "task": "Procurement Recommendation",
            "low_stock_items": low_stock
        }
        insights = provider.generate_insights(prompt_data)
        ai_recommendations = insights.get("recommendations", [])
        
    return {
        "summary": {
            "total_items": len(items),
            "low_stock_count": len(low_stock),
            "healthy_stock_count": len(normal_stock)
        },
        "low_stock_items": low_stock,
        "all_items": low_stock + normal_stock,
        "ai_recommendations": ai_recommendations
    }

def get_low_stock(db: Session):
    items = db.query(InventoryItem).filter(InventoryItem.current_stock <= InventoryItem.minimum_stock).all()
    results = []
    for item in items:
        shortage = item.minimum_stock - item.current_stock
        recommended = max(shortage + item.daily_consumption * 14, item.maximum_stock - item.current_stock)
        results.append({
            "item": item,
            "current_stock": item.current_stock,
            "minimum_stock": item.minimum_stock,
            "shortage": shortage,
            "recommended_reorder_quantity": int(recommended),
            "severity": "CRITICAL" if item.current_stock == 0 else "HIGH"
        })
    return {"items": results}

def get_expiring(db: Session):
    items = db.query(InventoryItem).filter(InventoryItem.expiry_date != None).all()
    today = datetime.now(timezone.utc).date()
    
    expired = []
    expiring_soon = []
    
    for item in items:
        days_rem = (item.expiry_date - today).days
        if days_rem < 0:
            expired.append({
                "item": item,
                "expiry_date": item.expiry_date,
                "days_remaining": days_rem,
                "severity": "EXPIRED"
            })
        elif days_rem <= 30:
            expiring_soon.append({
                "item": item,
                "expiry_date": item.expiry_date,
                "days_remaining": days_rem,
                "severity": "WARNING"
            })
            
    return {
        "expired_items": expired,
        "expiring_soon_items": expiring_soon
    }

def get_vendors(db: Session):
    vendors = db.query(Vendor).all()
    results = []
    for vendor in vendors:
        pos = db.query(PurchaseOrder).filter(PurchaseOrder.vendor_id == vendor.id).all()
        total_value = sum(po.total_amount for po in pos if po.total_amount)
        results.append({
            "id": vendor.id,
            "name": vendor.name,
            "contact_email": vendor.contact_email,
            "delivery_time_days": vendor.delivery_time_days,
            "reliability_score": vendor.reliability_score,
            "rating": vendor.rating,
            "purchase_orders_count": len(pos),
            "total_purchase_value": total_value
        })
    return results

def get_reorder_suggestions(db: Session):
    items = db.query(InventoryItem).filter(InventoryItem.current_stock <= InventoryItem.minimum_stock * 1.2).all()
    suggestions = []
    for item in items:
        recommended = item.maximum_stock - item.current_stock
        reason = "Low Stock" if item.current_stock <= item.minimum_stock else "Approaching Minimum"
        suggestions.append({
            "item": item,
            "current_stock": item.current_stock,
            "minimum_stock": item.minimum_stock,
            "recommended_quantity": recommended,
            "reason": reason
        })
    return suggestions

def get_purchase_recommendations(db: Session):
    provider = get_ai_provider()
    
    # gather context
    ls = get_low_stock(db)["items"]
    ex = get_expiring(db)
    
    context = {
        "low_stock_count": len(ls),
        "expired_count": len(ex["expired_items"]),
        "expiring_soon_count": len(ex["expiring_soon_items"]),
        "low_stock_details": [{"name": i["item"].name, "shortage": i["shortage"]} for i in ls[:10]]
    }
    
    insights = provider.generate_insights({
        "task": "Procurement Recommendation",
        "inventory_context": context
    })
    
    return insights

def create_purchase_order(db: Session, vendor_id: int, total_amount: float):
    po = PurchaseOrder(
        vendor_id=vendor_id,
        order_date=datetime.now(timezone.utc),
        total_amount=total_amount,
        status="Pending"
    )
    db.add(po)
    db.commit()
    db.refresh(po)
    return po
